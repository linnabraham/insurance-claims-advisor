from typing import List, Tuple

import structlog

from .models import Chunk, Paragraph

logger = structlog.get_logger()


def chunk_sections(
    sectioned: List[Tuple[str, Paragraph]], max_chars: int = 800
) -> List[Chunk]:
    chunks: List[Chunk] = []
    current_text = ""
    current_section: str | None = None

    for section, para in sectioned:
        para_text = " ".join(b.text.replace("\n", " ") for b in para.blocks)

        if current_section != section:
            if current_text:
                chunks.append(
                    Chunk(text=current_text.strip(), section=current_section or "")
                )
            current_text = ""
            current_section = section

        if len(current_text) + len(para_text) < max_chars:
            current_text += "\n" + para_text
        else:
            chunks.append(
                Chunk(text=current_text.strip(), section=current_section or "")
            )
            current_text = para_text

    if current_text:
        chunks.append(Chunk(text=current_text.strip(), section=current_section or ""))

    logger.info("chunk.complete", num_chunks=len(chunks), max_chars=max_chars)
    return chunks
