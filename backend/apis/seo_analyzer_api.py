from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from urllib.parse import urlparse

from backend.crawler import crawl_site
from backend.rules_engine import run_rules_checks
from backend.report_generator import generate_report

router = APIRouter()

DEFAULT_QUERY = (
    "Analyse this website's SEO in depth. For every page you have data on, "
    "list the specific issues, explain why each matters, and give an exact "
    "actionable fix. Prioritise by traffic impact. End with an overall score "
    "out of 10 and a summary paragraph."
)


class AnalyzeRequest(BaseModel):
    url: HttpUrl
    query: str = DEFAULT_QUERY


@router.post("/analyze")
def analyze_site(request: AnalyzeRequest):
    try:
        url = str(request.url)

        # 1. Crawl site
        pages = crawl_site(url)
        if not pages:
            raise HTTPException(status_code=400, detail="No pages could be crawled from this URL.")

        # 2. Rule-based SEO checks
        rules = run_rules_checks(pages)

        # 3. Build knowledge base + RAG analysis via Groq
        report = generate_report(pages, rules, request.query)

        return {
            "status": "success",
            "pages_crawled": len(pages),
            "report": report,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SEO analysis failed: {str(e)}")
