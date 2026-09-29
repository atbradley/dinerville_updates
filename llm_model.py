import os

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = os.getenv("OLLAMA_MODEL")
uri_base = os.getenv("OLLAMA_BASE_URL")
api_key = os.getenv("OLLAMA_API_KEY")

def get_llm():
    return ChatOpenAI(
        model_name=model, 
        base_url=uri_base, 
        api_key=api_key,
    )