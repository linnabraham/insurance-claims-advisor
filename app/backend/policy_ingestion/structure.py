from typing import List, Tuple

import numpy as np
import structlog

from .models import Block, Paragraph

logger = structlog.get_logger()


def get_heading_threshold(font_sizes: List[float], percentile: float = 80) -> float:
    if not font_sizes:
        return 0.0
    return float(np.percentile(np.array(font_sizes), percentile))


def mark_headings(blocks: List[Block], threshold: float) -> List[Block]:
    for b in blocks:
        b.is_heading = b.font_size > threshold
    num_headings = sum(1 for b in blocks if b.is_heading)
    logger.info(
        "structure.headings_marked",
        num_headings=num_headings,
        num_blocks=len(blocks),
        threshold=threshold,
    )
    return blocks


def group_paragraphs(
    blocks: List[Block],
    y_thresh: float = 4,
    heading_thresh: float = 15,
) -> List[Paragraph]:
    paragraphs: List[Paragraph] = []
    current: List[Block] = []
    prev_y = None

    for b in blocks:
        if prev_y is None:
            current.append(b)
        else:
            gap = prev_y - b.y1
            effective_thresh = heading_thresh if current[-1].is_heading else y_thresh

            if gap < effective_thresh:
                current.append(b)
            else:
                paragraphs.append(Paragraph(blocks=current))
                current = [b]

        prev_y = b.y0

    if current:
        paragraphs.append(Paragraph(blocks=current))

    logger.info("structure.paragraphs_grouped", num_paragraphs=len(paragraphs))
    return paragraphs


def assign_sections(paragraphs: List[Paragraph]) -> List[Tuple[str, Paragraph]]:
    sectioned: List[Tuple[str, Paragraph]] = []
    current_section = "Unknown"

    for para in paragraphs:
        text = " ".join(b.text for b in para.blocks)

        if any(b.is_heading for b in para.blocks):
            current_section = text.strip()

        sectioned.append((current_section, para))

    logger.info("structure.sections_assigned", num_paragraphs=len(sectioned))
    return sectioned
