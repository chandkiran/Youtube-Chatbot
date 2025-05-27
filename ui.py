import streamlit as st
import requests
import re

def extract_video_id(url):
    """Extracts video ID from a full YouTube URL."""
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    return match.group(1) if match else None

st.title("🎥 YouTube Chatbot")

video_url = st.text_input("Enter the youtube video URL")
question = st.text_input("Ask a question about the video")

if st.button("Ask"):
    if video_url and question:
        video_id = extract_video_id(video_url)
        with st.spinner("Getting answer..."):
            try:
                res = requests.post(
                    "http://localhost:8000/chat",
                    json={"video_id": video_id, "query": question}
                )
                if res.status_code == 200:
                    data = res.json()
                    if "response" in data:
                        st.markdown(f"**Answer:** {data['response']}")
                    elif "error" in data:
                        st.error(f"❌ Error: {data['error']}")
                    else:
                        st.error("Unexpected response format.")
                else:
                    st.error("❌ Failed to connect to backend.")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter both video ID and question.")
