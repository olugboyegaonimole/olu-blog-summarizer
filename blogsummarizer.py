from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import requests
from newspaper import Article

app = FastAPI()

class URLInput(BaseModel):
    url: HttpUrl  # Ensures valid URL input

@app.post("/summarize/")
def summarize_blog(data: URLInput):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        
        response = requests.get(str(data.url), headers=headers, timeout=10)

        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to fetch webpage (Status {response.status_code})")

        # Process article content
        article = Article(str(data.url))
        article.set_html(response.text)
        article.parse()
        article.nlp()

        if not article.summary:
            raise HTTPException(status_code=400, detail="Failed to generate a summary.")

        return {"summary": article.summary}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Request error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
