import structlog

from .chunk import chunk_sections
from .config import PipelineConfig
from .extract import extract_blocks_with_fonts
from .layout import order_blocks
from .models import PipelineResult
from .structure import (
    assign_sections,
    get_heading_threshold,
    group_paragraphs,
    mark_headings,
)

logger = structlog.get_logger()


def run_pipeline(path: str, config: PipelineConfig) -> PipelineResult:
    logger.info("pipeline.start", file=path, page=config.page_num)

    blocks, font_sizes, pw, ph = extract_blocks_with_fonts(path, config.page_num)

    threshold = get_heading_threshold(font_sizes, config.heading_percentile)
    blocks = mark_headings(blocks, threshold)

    ordered = order_blocks(blocks, config)
    paragraphs = group_paragraphs(
        ordered,
        y_thresh=config.y_threshold,
        heading_thresh=config.heading_y_threshold,
    )

    sectioned = assign_sections(paragraphs)
    chunks = chunk_sections(sectioned, max_chars=config.max_chunk_chars)

    logger.info("pipeline.complete", num_chunks=len(chunks))

    return PipelineResult(
        blocks=blocks,
        paragraphs=paragraphs,
        sectioned=sectioned,
        chunks=chunks,
        page_width=pw,
        page_height=ph,
    )
