"""Central configuration for the profile matching RAG system."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent

RESUMES_DIR = Path(os.getenv("RESUMES_DIR", PROJECT_ROOT / "resumes"))
JOB_DESCRIPTIONS_DIR = Path(
    os.getenv("JOB_DESCRIPTIONS_DIR", PROJECT_ROOT / "job_descriptions")
)
CHROMA_PERSIST_DIR = Path(
    os.getenv("CHROMA_PERSIST_DIR", PROJECT_ROOT / "data" / "chroma_db")
)

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "chroma").lower()
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SUPPORTED_RESUME_EXTENSIONS = {".txt", ".pdf", ".docx", ".md"}
MAX_FILE_SIZE_MB = 10
CHUNK_SIZE = 512
CHUNK_OVERLAP = 64
TOP_K = 10
COLLECTION_NAME = "resumes"
