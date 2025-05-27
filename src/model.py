import os
from mistralai import Mistral
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda, Runnable
from langchain_core.output_parsers import StrOutputParser
from typing import Any, Optional

load_dotenv()

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

# Custom Mistral Runnable (Fixed version)
class MistralRunnable(Runnable):
    def __init__(self, api_key: str, model: str = "mistral-large-latest", temperature: float = 0.1):
        self.client = Mistral(api_key=api_key)
        self.model = model
        self.temperature = temperature

    def invoke(self, input: Any, config: Optional[dict] = None) -> str:
        response = self.client.chat.complete(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": str(input)
                }
            ],
            temperature=self.temperature,
        )
        return response.choices[0].message.content


def build_chain(video_id: str) -> Runnable:
    """Builds the main chain for a given video ID."""
    try:
        # Get transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript = " ".join(chunk["text"] for chunk in transcript_list)

        # Split transcript into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(transcript)

        # Embedding
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_store = FAISS.from_texts(chunks, embeddings)

        # Retriever
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

        # Prompt Template
        prompt = PromptTemplate(
            template=""" 
                You are a helpful assistant.
                Answer only from the provided transcript context.
                If the context is insufficient, say "I don't know."

                Context: {context} 
                Question: {query}
            """,
            input_variables=["context", "query"]
        )

        # Format retrieved docs
        def format_docs(retrieved_result):
            return "\n\n".join(doc.page_content for doc in retrieved_result)

        # Chain components
        mistral_runnable = MistralRunnable(api_key=api_key)
        parser = StrOutputParser()

        parallel_chain = RunnableParallel({
            'context': retriever | RunnableLambda(format_docs),
            'query': RunnablePassthrough()
        })

        main_chain = parallel_chain | prompt | mistral_runnable | parser

        # Test the chain
        result = main_chain.invoke("What is linear regression?")
        print(f"Test Result: {result}")

        return main_chain

    except TranscriptsDisabled:
        raise ValueError("Transcripts are disabled for this video.")
    except Exception as e:
        raise e
