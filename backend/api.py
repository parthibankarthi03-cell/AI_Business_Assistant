"""
FastAPI server for AI Business Assistant.
"""

import os
import threading
import webbrowser

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from main import analyze_business

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(title="AI Business Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class BusinessRequest(BaseModel):
    website_url: str
    business_type: str
    google_reviews: str
    competitor_urls: list[str] = []


@app.get("/")
def home():
    return FileResponse(os.path.join(BASE_DIR, "frontend", "index.html"))


@app.post("/analyze")
def analyze(req: BusinessRequest):
    try:
        report = analyze_business(
            website_url=req.website_url,
            business_type=req.business_type,
            google_reviews=req.google_reviews,
            competitor_urls=req.competitor_urls,
        )
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
def startup_event():
    threading.Timer(
        2,
        lambda: webbrowser.open("http://127.0.0.1:8000")
    ).start()