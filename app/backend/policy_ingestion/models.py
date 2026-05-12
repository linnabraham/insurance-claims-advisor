from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Block:
    text: str
    x0: float
    y0: float
    x1: float
    y1: float
    font_size: float
    page_width: float
    page_height: float
    is_heading: bool = False


@dataclass
class Paragraph:
    blocks: List[Block]


@dataclass
class Chunk:
    text: str
    section: str


@dataclass
class PipelineResult:
    blocks: List[Block]
    paragraphs: List[Paragraph]
    sectioned: List[Tuple[str, Paragraph]]
    chunks: List[Chunk]
    page_width: float
    page_height: float
