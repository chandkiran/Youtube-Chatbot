import streamlit as st
import requests

st.title("🎥 YouTube Chatbot")

video_id = st.text_input("Enter YouTube Video ID")
question = st.text_input("Ask a question about the video")

if st.button("Ask"):
    if video_id and question:
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
