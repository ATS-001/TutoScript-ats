import streamlit as st
import yt_dlp
from groq import Groq
import os

# Use a simple, robust function to fetch transcript
def get_transcript(video_url):
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'skip_download': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        # Prefer manual subtitles, fallback to auto-generated
        subs = info.get('subtitles') or info.get('automatic_captions')
        if 'en' in subs:
            # Logic to extract text from the subtitle format
            return "Transcript text retrieved..." 
    return None

# The rest of your Streamlit UI logic remains clean and simple
st.title("YouTube ATS Analyzer")
# ... (rest of your UI code)
