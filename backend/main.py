from fastapi import FastAPI
from dotenv import load_dotenv
from backend.apis.seo_analyzer_api import router as crawler_router
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()

@app.get('/')
def read_root():
    return {'message': 'SEO Analyzer API'}

app.include_router(crawler_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
