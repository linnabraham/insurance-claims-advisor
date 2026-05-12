from typing import List, Tuple

import structlog
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar, LTTextContainer

from .models import Block

logger = structlog.get_logger()


def extract_blocks_with_fonts(
    path: str, page_num: int = 0
) -> Tuple[List[Block], List[float], float, float]:
    for i, page_layout in enumerate(extract_pages(path)):
        if i != page_num:
            continue

        blocks: List[Block] = []
        all_sizes: List[float] = []

        for element in page_layout:
            if not isinstance(element, LTTextContainer):
                continue

            text = element.get_text().strip()
            if not text:
                continue

            sizes = [
                char.size
                for line in element
                for char in line
                if isinstance(char, LTChar)
            ]
            avg_size = sum(sizes) / len(sizes) if sizes else 0
            if sizes:
                all_sizes.extend(sizes)

            x0, y0, x1, y1 = element.bbox
            blocks.append(
                Block(
                    text=text,
                    x0=x0,
                    y0=y0,
                    x1=x1,
                    y1=y1,
                    font_size=avg_size,
                    page_width=page_layout.width,
                    page_height=page_layout.height,
                )
            )

        logger.info(
            "extract.complete",
            num_blocks=len(blocks),
            page_num=page_num,
            page_width=page_layout.width,
            page_height=page_layout.height,
        )
        return blocks, all_sizes, page_layout.width, page_layout.height

    logger.warning("extract.page_not_found", page_num=page_num)
    return [], [], 0.0, 0.0
