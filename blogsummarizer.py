from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from newspaper import Article  # Better text extraction

app = FastAPI()

class URLInput(BaseModel):
    url: str

@app.post("/summarize/")
def summarize_blog(data: URLInput):
    try:
        # Load and parse article using Newspaper3k
        article = Article(data.url)
        article.download()
        article.parse()

        if not article.text:
            raise HTTPException(status_code=400, detail="No readable content found on the page")

        # Generate a summary
        article.nlp()
        summarized_text = article.summary

        return {"summary": summarized_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

