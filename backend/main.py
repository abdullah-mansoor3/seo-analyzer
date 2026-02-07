from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from backend.apis.seo_analyzer_api import router as seo_router

load_dotenv()

app = FastAPI(title="SEO Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(seo_router)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "SEO Analyzer API"}
