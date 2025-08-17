from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from urllib.parse import urlparse
import os

# Import project modules
from backend.crawler import crawl_site, save_results
from backend.rules_engine import run_quick_checks
from backend.embeddings import embed_documents, build_faiss_index
from backend.rag_engine import rag_query
from backend.report_generator import generate_report

router = APIRouter()

class AnalyzeRequest(BaseModel):
    url: HttpUrl
    query: str = "Give me details suggestions for improving SEO for the site. I'm giving you the metadata. Give me in depth details on exactly what to improve and in what page."


@router.post("/analyze/")
def analyze_site(request: AnalyzeRequest):
    try:
        url = str(request.url)
        domain = urlparse(url).netloc

        # 1. Crawl site
        pages = crawl_site(url)
        if not pages:
            raise HTTPException(status_code=400, detail="No pages crawled")

        # 2. Run rules engine checks
        quick_checks = run_quick_checks(pages)

        # 3. Prepare docs (pages + quick checks)
        documents = []
        for p in pages:
            documents.append({"source": p["url"], "text": p["content"]})
        documents.append({"source": "rules_engine", "text": str(quick_checks)})

        # 4. Build embeddings + FAISS index
        embeddings, index = build_faiss_index(documents)

        # 5. Run RAG query
        rag_output = rag_query(request.query, embeddings, index, documents)

        # 6. Generate SEO report
        report = generate_report(pages, quick_checks, rag_output)

        return {
            "status": "success",
            "pages_crawled": len(pages),
            "quick_checks": quick_checks,
            "rag_output": rag_output,
            "report": report,
            "saved_to": f"data/sites/{domain}/crawl.json"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SEO analysis failed: {str(e)}")
