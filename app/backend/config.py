"""Backend configuration sourced from environment / .env."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _resolve(path_str: str) -> Path:
    """Resolve relative paths against the repo root, leave absolute paths alone."""
    p = Path(path_str)
    return p if p.is_absolute() else REPO_ROOT / p


CHROMA_PERSIST_DIR = _resolve(os.getenv("CHROMA_PERSIST_DIR", "data/chroma"))
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
