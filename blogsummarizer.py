from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
import requests
from newspaper import Article
import logging
import nltk


nltk.download('punkt')


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can restrict it to specific URLs later)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class URLInput(BaseModel):
    url: HttpUrl  # Validates the input is a proper URL


@app.get("/", include_in_schema=False)
@app.head("/", include_in_schema=False)
def read_root():
    return {"message": "Welcome to the Blog Summarizer API!"}



logger = logging.getLogger(__name__)

@app.post("/summarize/")
def summarize_blog(data: URLInput):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

        response = requests.get(str(data.url), headers=headers, timeout=10)

        if response.status_code != 200:
            logger.error(f"Failed to fetch {data.url}: {response.status_code}")
            raise HTTPException(status_code=400, detail="Failed to fetch webpage.")

        article = Article(str(data.url))
        article.download()
        article.parse()
        article.nlp()

        if not article.summary:
            logger.error(f"Failed to summarize: {data.url}")
            raise HTTPException(status_code=400, detail="Failed to generate a summary.")

        return {"summary": article.summary}

    except Exception as e:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

