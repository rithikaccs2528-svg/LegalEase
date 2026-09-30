import os
from pathlib import Path

from dotenv import load_dotenv # type: ignore


ROOT_DIR = Path(__file__).resolve().parents[1]

# Load .env from project root
load_dotenv(ROOT_DIR / ".env")


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
).strip()


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
).strip()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).strip()


COMPANY_NAME = os.getenv(
    "COMPANY_NAME",
    "LegalEase"
).strip()


COMPANY_TAGLINE = os.getenv(
    "COMPANY_TAGLINE",
    "AI-Powered Legal Document Generator"
).strip()


def demo_mode_enabled() -> bool:
    value = os.getenv(
        "DEMO_MODE",
        "true"
    ).strip().lower()

    return value in {
        "1",
        "true",
        "yes",
        "on"
    }