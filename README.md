
# YouTube Chatbot

The YouTube Chatbot is a web-based AI application that allows users to ask questions about the content of YouTube videos by simply providing a link. It uses FastAPI for backend services, Streamlit for a clean user interface, and Mistral AI to answer questions based on the video’s transcript.

---

##  Features

- Accepts YouTube video URLs via a user-friendly Streamlit UI.
- Extracts video transcripts using `youtube-transcript-api`.
- Splits and embeds transcript using HuggingFace sentence transformers.
- Stores and retrieves relevant content using FAISS vector store.
- Uses a custom prompt to ask questions and answer using Mistral AI.
- Responds via FastAPI endpoint with error handling and graceful fallback.

---

## 📁 Project Structure

```plaintext
youtube-chatbot-mistral/
├── app/
│   ├── model.py          #llm model
│  
├── ui.py                 # Streamlit frontend
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
├── .gitignore
└── main.py               # Fast API

```

---

## Installation 

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/youtube-chatbot-mistral.git
cd youtube-chatbot-mistral
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

##  Run the Application

### 1. Run the FastAPI Backend

```bash
uvicorn app.main:app --reload
```

### 2. Run the Streamlit Frontend

```bash
streamlit run ui.py
```

---

##  Example Usage

**Request Body**:

```json
{
  "query": "What is linear regression?",
  "video_id": "dQw4w9WgXcQ"
}
```

**Response**:

```json
{
  "response": "Linear regression is ..."
}
```

---

## Screenshot of UI

![screenshot](https://github.com/user-attachments/assets/9da6f70d-254c-48b8-afaf-1867252c9be1)

---

##  License

This project is licensed under the MIT License.
