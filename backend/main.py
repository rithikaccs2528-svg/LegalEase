from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import (
    COMPANY_NAME,
    COMPANY_TAGLINE
)

from backend.routes import router


app = FastAPI(

    title=COMPANY_NAME,

    description=COMPANY_TAGLINE,

    version="1.0.0"
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"],
)


app.include_router(router)


@app.get("/")
def root():

    return {

        "app": COMPANY_NAME,

        "message": "LegalEase backend is running.",

        "docs": "/docs"
    }


@app.get("/health")
def health():

    return {

        "status": "ok"
    }