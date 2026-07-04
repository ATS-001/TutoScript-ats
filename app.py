import os
import streamlit as st
from langchain_groq import GroqEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from pytube import YouTube
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    CouldNotRetrieveTranscript
)
from dotenv import load_dotenv

# Load keys
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Set Page Config for a wider interface (crucial for side-by-side view)
st.set_page_config(page_title="AI-Powered Tutor", layout="wide")

# CSS to inject for hiding the Streamlit Toolbar, Header, and Footer completely AND customizing the theme colors
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display: none !important;}
    div[data-testid="stToolbar"] {display: none !important;}
    
    /* 🎨 CUSTOM THEME OVERRIDES */
    /* 1. Main Background Color */
    .stApp {
        background-color: #0B0E14 !important;
    }
    
    /* 2. System Config & Credits Expanders/Cards Background */
    div[data-testid="stExpander"] {
        background-color: #151B26 !important;
        border: 1px solid #222C3D !important;
        border-radius: 8px !important;
    }
    
    /* 3. Text inputs and Chat Inputs Background */
    div[data-testid="stTextInputRootElement"] > div {
        background-color: #151B26 !important;
        border: 1px solid #222C3D !important;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Initialize Session States
if "messages" not in st.session_state:
    st.session_state.messages = []
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "current_video" not in st.session_state:
    st.session_state.current_video = None

from urllib.parse import urlparse, parse_qs

def get_youtube_transcript(url):
    try:
        # Perfectly clean Python method to extract video ID without regex or breaking syntax
        video_id = None
        parsed_url = urlparse(url)
        
        if parsed_url.hostname == 'youtu.be':
            video_id = parsed_url.path[1:]
        elif parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
            if parsed_url.path == '/watch':
                video_id = parse_qs(parsed_url.query).get('v', [None])[0]
            elif parsed_url.path.startswith(('/embed/', '/v/')):
                video_id = parsed_url.path.split('/')[2]
                
        if not video_id:
            st.error("Could not parse YouTube Video ID from URL.")
            return ""

        api = YouTubeTranscriptApi()
        transcript_data = api.fetch(video_id)
        text = " ".join([item.text for item in transcript_data])
        return text
    except TranscriptsDisabled:
        st.error("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        st.error("No transcript found for this video.")
    except VideoUnavailable:
        st.error("This video is unavailable.")
    except CouldNotRetrieveTranscript:
        st.error("Could not retrieve transcript. YouTube might be blocking the cloud server's IP. Try a different video link!")
    except Exception as e:
        st.error(f"Unexpected error getting transcript: {e}")
    return ""
    
def save_transcript_to_file(text, filename="transcript.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

# This callback safely drops the input field out of memory during state transitions
def reset_all_states():
    st.session_state.messages = []
    st.session_state.qa_chain = None
    st.session_state.current_video = None
    if "video_input" in st.session_state:
        st.session_state.video_input = ""

# Main Title App Interface — Completely Unified Monospace Typography
st.markdown(
    """
    <div style="text-align: left; margin-bottom: 20px; font-family: 'Courier New', Courier, monospace;">
        <h1 style="font-family: 'Courier New', Courier, monospace; font-weight: 800; letter-spacing: -1px; margin-bottom: 0px;">
            TUTOSCRIPT <span style="font-size: 24px;">⚡</span>
        </h1>
        <p style="color: #888888; font-size: 14px; margin-top: 2px; margin-bottom: 15px;">
            [ ENGINE: GROQ_LLM // STATUS: ACTIVE ]
        </p>
        <p style="font-size: 16px; color: #E0E0E0;">
            Deconstruct video tutorials and query the script in real-time.
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Layout Row: System Configuration & Credits Metadata Cards
meta_col1, meta_col2 = st.columns(2)

with meta_col1:
    with st.expander("ℹ️ System Configuration", expanded=False):
        st.markdown(
            """
            **Architecture:** Retrieval-Augmented Generation (RAG)  
            **LLM Pipeline:** Llama 3.3 70B via Groq Cloud API  
            **Embeddings Engine:** HuggingFace `all-MiniLM-L6-v2` (Local)  
            **Vector Store:** FAISS Database Indexer
            """
        )

with meta_col2:
    with st.expander("🛠️ Credits Registry", expanded=False):
        st.markdown("**Creator / Engineer:** Aaron Thalakkottor Sooraj")
        st.link_button("📁 TutoScript", "https://github.com/ATS-001/TutoScript-ats", use_container_width=False)
        st.markdown(
            """
            **Project Baseline:** Day 5 of Projectathon conducted by μLearn LBSITW, AI x DS (1st July 2026)  
            **Presented By:** Darshana D Devi, AI & ML IG LEAD, µLearn LBSITW
            """
        )

st.write("---")

# Create main Layout Columns (Left side input/video, Right side Chatbot)
col1, col2 = st.columns([1, 1], gap="large")
with col1:
    st.subheader("📺 Video Configuration")
    video_url = st.text_input("Enter YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...", key="video_input")
    
    # 💡 Smart Fallback UI Element
    manual_transcript = st.text_area("OR Paste Transcript Manually (Fallback)", placeholder="If automatic fetching is blocked, open the video on YouTube, click 'Show Transcript', and copy-paste the text here...", height=120)
    
    btn_col1, btn_col2 = st.columns([1, 1])
    
    with btn_col1:
        process_clicked = st.button("Process Video", use_container_width=True)
    with btn_col2:
        st.button("Clear Conversation", use_container_width=True, on_click=reset_all_states)

    if process_clicked:
        if not video_url and not manual_transcript:
            st.error("Please enter a YouTube URL or paste a transcript manually!")
        else:
            with st.spinner("Processing text and generating embeddings..."):
                transcript_text = ""
                
                # 1. Attempt automatic fetch if URL is given
                if video_url:
                    transcript_text = get_youtube_transcript(video_url)
                
                # 2. Fall back to manual paste if fetch failed or wasn't attempted
                if not transcript_text and manual_transcript:
                    st.info("Using manually provided transcript text.")
                    transcript_text = manual_transcript
                    
                if transcript_text:
                    save_transcript_to_file(transcript_text)
                    loader = TextLoader("transcript.txt", encoding="utf-8")
                    documents = loader.load()
                    
                    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                    docs = splitter.split_documents(documents)
                    
                    embeddings = GroqEmbeddings(model="text-embedding-ada-002") 
# Or use another Groq-supported embedding model like "llama-3.1-8b-instant" if preferred
                    vectorstore = FAISS.from_documents(docs, embeddings)
                    retriever = vectorstore.as_retriever()
                    
                    groq_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)
                    
                    system_prompt = (
                        "Use the following pieces of retrieved context to answer the question. "
                        "If you don't know the answer, say that you don't know.\n\n"
                        "Context:\n{context}"
                    )
                    prompt = ChatPromptTemplate.from_messages([
                        ("system", system_prompt),
                        ("human", "{input}"),
                    ])
                    
                    def format_docs(docs_list):
                        return "\n\n".join(doc.page_content for doc in docs_list)
                    
                    st.session_state.qa_chain = (
                        {"context": retriever | format_docs, "input": RunnablePassthrough()}
                        | prompt
                        | groq_llm
                        | StrOutputParser()
                    )
                    
                    st.session_state.current_video = video_url if video_url else None
                    st.success("Transcript processed successfully! Ask your questions on the right panel.")

with col2:
    st.subheader("💬 Interactive Assistant")
    
    if st.session_state.qa_chain is None:
        st.info("Please enter and process a YouTube video to initialize the chat instance.")
    else:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if user_question := st.chat_input("Ask a question about this video..."):
            with st.chat_message("user"):
                st.markdown(user_question)
            st.session_state.messages.append({"role": "user", "content": user_question})

            with st.chat_message("assistant"):
                with st.spinner("Groq is thinking..."):
                    # Direct invocation of the LCEL engine
                    answer = st.session_state.qa_chain.invoke(user_question)
                    st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

# Footnote Signature Row
st.write("---")
st.markdown(
    """
    <div style="text-align: center; color: gray; font-size: 14px;">
        Aaron Thalakkottor Sooraj <br>
        Designed & Developed by ATS-PDZ • © Since 2023
    </div>
    """, 
    unsafe_allow_html=True
)
