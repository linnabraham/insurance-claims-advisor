from typing import List

import structlog

from .config import PipelineConfig
from .models import Block

logger = structlog.get_logger()


def order_blocks(blocks: List[Block], config: PipelineConfig) -> List[Block]:
    if not blocks:
        logger.info("layout.ordered", num_blocks=0, layout=config.layout)
        return []

    if config.layout == "single":
        ordered = sorted(blocks, key=lambda b: (-b.y1, b.x0))

    elif config.layout == "two_column":
        page_width = blocks[0].page_width
        split_x = config.column_split * page_width

        left = [b for b in blocks if b.x0 < split_x]
        right = [b for b in blocks if b.x0 >= split_x]

        left = sorted(left, key=lambda b: (-b.y1, b.x0))
        right = sorted(right, key=lambda b: (-b.y1, b.x0))

        ordered = left + right

    else:
        ordered = blocks

    logger.info("layout.ordered", num_blocks=len(ordered), layout=config.layout)
    return ordered
