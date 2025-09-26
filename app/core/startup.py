from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.service.ml.sentiment import SentimentPipeline

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    SentimentPipeline.get_pipeline()
    print("Sentiment pipeline loaded and ready!")
    yield
    # Shutdown code
    SentimentPipeline.cleanup()
    print("Sentiment pipeline unloaded.")