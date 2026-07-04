import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq
import os
import re

st.set_page_config(page_title="YouTube Transcript ATS", page_icon="📊", layout="centered")
st.title("📊 YouTube Transcript ATS & Analyzer")

# Initialize the lightweight Groq client
# Make sure you added GROQ_API_KEY to your Streamlit Secrets!
if "GROQ_API_KEY" in os.environ:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
elif "groq" in st.secrets:
    client = Groq(api_key=st.secrets["groq"]["GROQ_API_KEY"])
else:
    client = None
    st.warning("Please add your GROQ_API_KEY to Streamlit Secrets.")

# Function to extract Video ID
def get_video_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

video_url = st.text_input("Paste YouTube Video URL:")

if video_url:
    video_id = get_video_id(video_url)
    if video_id:
        try:
            with st.spinner("Fetching transcript..."):
                transcript_list = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id)
                transcript_text = " ".join([item['text'] for item in transcript_list])
            st.success("Transcript fetched successfully!")
            
            user_question = st.text_input("Ask a question about this video or ask to analyze it:")
            
            if user_question and client:
                with st.spinner("Analyzing with Groq AI..."):
                    prompt = f"Context transcript from YouTube video:\n{transcript_text}\n\nUser Request: {user_question}"
                    
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-specdec",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    response = completion.choices[0].message.content
                    st.markdown("### AI Analysis:")
                    st.write(response)
        except Exception as e:
            st.error(f"Could not retrieve transcript. Error: {str(e)}")
    else:
        st.error("Invalid YouTube URL.")
