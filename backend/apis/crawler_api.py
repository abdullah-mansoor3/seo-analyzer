from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from urllib.parse import urlparse
import os

from backend.crawler import crawl_site, save_results 

router = APIRouter()

class CrawlRequest(BaseModel):
    url: HttpUrl

@router.post("/crawl/")
def crawl_website(request: CrawlRequest):
    try:
        url = str(request.url)
        results = crawl_site(url)
        domain = urlparse(url).netloc
        save_results(results, domain)
        return {
            "status": "success",
            "pages_crawled": len(results),
            "saved_to": f"data/sites/{domain}/crawl.json"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to crawl site: {str(e)}")
