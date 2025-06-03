A conversational AI system that allows users to ask questions about a YouTube video. The chatbot extracts the transcript of the video, embeds it, and responds intelligently using a Large Language Model (LLM) from Mistral AI.
Features
- Accepts YouTube video URLs via a user-friendly Streamlit UI.
- Extracts video transcripts using `youtube-transcript-api`.
- Splits and embeds transcript using HuggingFace sentence transformers.
- Stores and retrieves relevant content using FAISS vector store.
- Uses a custom prompt to ask questions and answer using Mistral AI.
- Responds via FastAPI endpoint with error handling and graceful fallback.
