from dataclasses import dataclass


@dataclass
class PipelineConfig:
    page_num: int = 0
    layout: str = "two_column"
    column_split: float = 0.5
    y_threshold: float = 4
    heading_y_threshold: float = 15
    heading_percentile: float = 80
    max_chunk_chars: int = 800
