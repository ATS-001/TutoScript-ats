import streamlit as st
import yt_dlp
from groq import Groq
import os

st.title("YouTube ATS Analyzer")

# Force these to show up immediately
video_url = st.text_input("Paste YouTube Video URL:")
user_question = st.text_input("Ask a question about this video:")

if st.button("Analyze"):
    if video_url:
        st.write(f"Analyzing: {video_url}")
        # Your extraction/Groq logic goes here
    else:
        st.warning("Please paste a URL first.")
