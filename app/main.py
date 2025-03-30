# Typical FastAPI main.py
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    # This is crucial - must listen on 0.0.0.0, not localhost/127.0.0.1
    uvicorn.run(app, host="0.0.0.0", port=8000)