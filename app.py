# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import json
import os
import faiss
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# ---------------- Load environment variables ----------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")

# ---------------- Initialize embeddings and LLM ----------------
local_embedder = SentenceTransformer("all-MiniLM-L6-v2")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.4,
    google_api_key=GOOGLE_API_KEY
)

# ---------------- Initialize FastAPI ----------------
app = FastAPI(title="Agricultural Advisory API")

# ---------------- Pydantic models ----------------
class AdvisoryRequest(BaseModel):
    farmer_data: Dict[str, Any]
    question: str

# ---------------- Helper functions ----------------
def build_index(context_text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    chunks = splitter.split_text(context_text)
    embeddings = [local_embedder.encode(chunk) for chunk in chunks]
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings).astype("float32"))
    return index, chunks

def retrieve_answer(question: str, index, chunks):
    # Embed query
    query_emb = local_embedder.encode(question)
    D, I = index.search(np.array([query_emb]).astype("float32"), k=1)
    retrieved_chunks = [chunks[i] for i in I[0]]
    context = "\n".join(retrieved_chunks)

    # Build prompt
    prompt_template = ChatPromptTemplate.from_template(
        """
You are an agricultural advisory assistant.
Use the given context to provide polite, friendly, and practical advice for the farmer.
Keep the answer short, clear, and actionable.

Context:
{context}

Farmer's Question: {question}

Advisory:
"""
    )
    prompt = prompt_template.format(context=context, question=question)
    response = llm.predict(prompt)
    return response

# ---------------- API Endpoint ----------------
@app.post("/get-advisory")
def get_advisory(request: AdvisoryRequest):
    try:
        context_text = json.dumps(request.farmer_data, indent=2)
        index, chunks = build_index(context_text)
        answer = retrieve_answer(request.question, index, chunks)
        return {"advisory": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
