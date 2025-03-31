# In your FastAPI app's main.py
import logging
from fastapi import FastAPI, Request

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Outgoing response: Status {response.status_code}")
    return response

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"status": "ok"}

@app.get("/health")
def health():
    logger.info("Health check endpoint called")
    return {"status": "healthy"}
