import os
from mistralai import Mistral
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
load_dotenv()

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

# Indexing
video_id = "LPZh9BOjkQs"

try:
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
    
except TranscriptsDisabled:
    print("No caption available for this video")


    # Text splitting into smaller chunks
if transcript_list:
        # Joining transcript text into single string
        transcript = " ".join(chunk["text"] for chunk in transcript_list)
        # Splitting the transcript into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(transcript)

        # Embedding
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_store = FAISS.from_texts(chunks, embeddings)

        # Save the vector store
        # print(vector_store.index_to_docstore_id)

        # Form retriever and passing query to it
        # Retriever formed using vector store and searching on basis of similarity and returning top four similar chunks

        retriever = vector_store.as_retriever(search_type="similarity",search_kwargs={"k": 4})
        retriever_result=retriever.invoke("What is the video about?")
        print(retriever_result)
