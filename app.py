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

# Indexing
video_id = "3dhcmeOTZ_Q"

try:
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    
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

        # Form retriever
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
        
        # Build prompt template
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

        def format_docs(retrieved_result):
            """Format retrieved documents into context string"""
            context_text = "\n\n".join(doc.page_content for doc in retrieved_result)
            return context_text

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
                            "content": str(input)  # Convert input to string
                        }
                    ],
                    temperature=self.temperature,
                )
                return response.choices[0].message.content

        # Initialize components
        mistral_runnable = MistralRunnable(api_key=api_key)
        parser = StrOutputParser()

        # Creating parallel chains containing retriever and prompts
        parallel_chain = RunnableParallel({
            'context': retriever | RunnableLambda(format_docs),
            'query': RunnablePassthrough()
        })

        # Main chain
        main_chain = parallel_chain | prompt | mistral_runnable | parser

        # Test the chain
        result = main_chain.invoke("What is linear regression?")
        print("Chain Result:")
        print(result)
        
except TranscriptsDisabled:
    print("No caption available for this video")
except Exception as e:
    print(f"An error occurred: {e}")