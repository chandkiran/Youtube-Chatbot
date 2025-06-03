The YouTube Chatbot is a web-based AI application that allows users to ask questions about the content of YouTube videos by simply providing a link. It uses FastAPI for backend services, Streamlit for a clean user interface, and Mistral AI to answer questions based on the video’s transcript. YouTube Chatbot with FastAPI, Streamlit & Mistral AI

---


##  Features
- Accepts YouTube video URLs via a user-friendly Streamlit UI.
- Extracts video transcripts using `youtube-transcript-api`.
- Splits and embeds transcript using HuggingFace sentence transformers.
- Stores and retrieves relevant content using FAISS vector store.
- Uses a custom prompt to ask questions and answer using Mistral AI.
- Responds via FastAPI endpoint with error handling and graceful fallback.
---

## Installation 
1. Clone the Repository

git clone https://github.com/yourusername/youtube-chatbot-mistral.git
'''bash
cd youtube-chatbot-mistral

2.Create and activate a virtual environment
'''bash
python -m venv venv
venv\Scripts\activate

3.Install dependencies
'''bash
pip install -r requirements.txt
---
## Run FastAPI Backend
'''bash
uvicorn main:app --reload

## Run Streamlit Frontend
'''bash
streamlit run ui.py
---
## Example usage
a.Request Body:
'''bash
{
  "query": "What is linear regression?",
  "video_id": "dQw4w9WgXcQ"
}

b.Response:
'''bash
{
  "response": "Linear regression is ..."
}
---
## Screenshots
![image](https://github.com/user-attachments/assets/9da6f70d-254c-48b8-afaf-1867252c9be1)

  
