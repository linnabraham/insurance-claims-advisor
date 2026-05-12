import json
from typing import List

import structlog

from .models import Chunk

logger = structlog.get_logger()


def save_chunks(chunks: List[Chunk], path: str) -> None:
    payload = [{"section": c.section, "text": c.text} for c in chunks]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    logger.info("inspect.saved", file=path, count=len(chunks))
