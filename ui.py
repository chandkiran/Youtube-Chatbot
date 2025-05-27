import streamlit as st
import requests

st.title("YouTube Chatbot")
video_id = st.text_input("Enter YouTube Video ID")
question = st.text_input("Ask a question about the video")
payload = {
    "video_id": video_id,
    "query": question
}
if st.button("Ask"):
    if video_id and question:
        with st.spinner("Getting answer..."):
            print(f"Video ID: {video_id}, Question: {question}")
            try:
                res = requests.post(
                    "http://localhost:8000/chat",
                    json=payload,
                )
                print(res.text)
                print(f"Response Status Code: {res.status_code}")
                if res.status_code == 200:
                    data = res.json()
                    if "answer" in data:
                        st.success(data["answer"])
                    else:
                        st.error(data["error"])
                else:
                    st.error("Failed to connect to backend.")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter both video ID and question.")
