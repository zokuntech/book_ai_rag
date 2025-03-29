from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="RAG API")

class Query(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"message": "Welcome to RAG API."}

@app.post("/query")
async def query(query: Query):
    # Placeholder for RAG implementation
    return {"response": f"Received querys a: {query.text}"}