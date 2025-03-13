from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
import requests
from newspaper import Article

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

@app.post("/summarize/")
def summarize_blog(data: URLInput):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        
        # Fetch HTML manually
        response = requests.get(str(data.url), headers=headers, timeout=10)

        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to fetch webpage (Status {response.status_code})")

        # Process article content
        article = Article(str(data.url))
        article.download()  # Manually fetch content
        article.parse()
        article.nlp()

        if not article.summary:
            raise HTTPException(status_code=400, detail="Failed to generate a summary.")

        return {"summary": article.summary}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Request error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
