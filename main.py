from fastapi import FastAPI
from pydantic import BaseModel
import os
from mistralai import Mistral
import sys
import os
import traceback
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.model import build_chain

app=FastAPI()
class ChatInput(BaseModel):
    query: str
    video_id: str

@app.post("/chat")
async def chat_handler(data: ChatInput):
    try:
        chain = build_chain(data.video_id)
        response = chain.invoke(data.query)
        return {"response": response}
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}