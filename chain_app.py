import os
from mistralai import Mistral
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_community.vectorstores import FAISS

load_dotenv()

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

# Indexing
video_id = "3dhcmeOTZ_Q"

try:
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    
except TranscriptsDisabled:
    print("No caption available for this video")


    