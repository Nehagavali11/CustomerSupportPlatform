import pandas as pd
import requests
from textblob import TextBlob
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
# from config import OLLAMA_URL, MODEL_NAME
from textblob import TextBlob
from backend.config import OLLAMA_URL, MODEL_NAME
from typing import Any
# Load embedding model
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# -------- CLEANING --------
def clean_text(text):
    return str(text).lower().strip()

# -------- SENTIMENT --------
def get_sentiment(text: str) -> str:
    blob: Any = TextBlob(text)
    score = blob.sentiment.polarity
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"

# -------- LLM CALL --------
def call_llm(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False   # 🔥 IMPORTANT FIX
            }
        )
        return response.json().get("response", "").strip()
    except Exception as e:
        return "Error"

# -------- CATEGORY --------
def categorize_ticket(text):
    text = text.lower()
    
    if "delivery" in text:
        return "Delivery"
    elif "payment" in text:
        return "Payment"
    elif "refund" in text:
        return "Refund"
    elif "product" in text:
        return "Product"
    else:
        return "Other"

# -------- REPLY --------
def generate_reply(text):
    prompt = f"""
    Write a short polite reply (2 lines max).

    Issue: {text}

    Reply:
    """
    return call_llm(prompt)
# -------- EMBEDDINGS --------
def create_embeddings(texts):
    return embed_model.encode(texts, convert_to_numpy=True)

def build_faiss_index(embeddings):
    embeddings = embeddings.astype('float32')
    
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    
    index.add(embeddings) # type: ignore
    return index
