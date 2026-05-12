from pathlib import Path
from typing import List

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import structlog

from .models import Block, Chunk, Paragraph

logger = structlog.get_logger()


def visualize_headings(
    blocks: List[Block],
    page_width: float,
    page_height: float,
    out_dir: Path,
) -> Path:
    fig, ax = plt.subplots(figsize=(8, 10))

    for b in blocks:
        color = "red" if b.is_heading else "black"
        rect = patches.Rectangle(
            (b.x0, b.y0),
            b.x1 - b.x0,
            b.y1 - b.y0,
            linewidth=1,
            edgecolor=color,
            facecolor="none",
        )
        ax.add_patch(rect)

    ax.set_xlim(0, page_width)
    ax.set_ylim(0, page_height)
    ax.set_title("Headings in RED")

    out_path = out_dir / "headings.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("visualize.headings_saved", file=str(out_path))
    return out_path


def visualize_paragraphs(
    paragraphs: List[Paragraph],
    page_width: float,
    page_height: float,
    out_dir: Path,
) -> Path:
    fig, ax = plt.subplots(figsize=(8, 10))

    for i, para in enumerate(paragraphs):
        color = plt.cm.tab10(i % 10)

        for b in para.blocks:
            rect = patches.Rectangle(
                (b.x0, b.y0),
                b.x1 - b.x0,
                b.y1 - b.y0,
                linewidth=1,
                edgecolor=color,
                facecolor="none",
            )
            ax.add_patch(rect)

        b0 = para.blocks[0]
        ax.text(b0.x0, b0.y1, f"P{i}", fontsize=10)

    ax.set_xlim(0, page_width)
    ax.set_ylim(0, page_height)
    ax.set_title("Paragraph grouping")

    out_path = out_dir / "paragraphs.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("visualize.paragraphs_saved", file=str(out_path))
    return out_path


def visualize_chunks(
    paragraphs: List[Paragraph],
    chunks: List[Chunk],
    page_width: float,
    page_height: float,
    out_dir: Path,
) -> Path:
    fig, ax = plt.subplots(figsize=(8, 10))

    para_to_chunk: List[int] = []
    idx = 0

    for para in paragraphs:
        para_text = " ".join(b.text for b in para.blocks)

        if idx >= len(chunks):
            break

        if para_text in chunks[idx].text:
            para_to_chunk.append(idx)
        else:
            idx += 1
            para_to_chunk.append(idx)

    for para, chunk_id in zip(paragraphs, para_to_chunk):
        color = plt.cm.Set2(chunk_id % 8)

        for b in para.blocks:
            rect = patches.Rectangle(
                (b.x0, b.y0),
                b.x1 - b.x0,
                b.y1 - b.y0,
                linewidth=1,
                edgecolor=color,
                facecolor="none",
            )
            ax.add_patch(rect)

    ax.set_xlim(0, page_width)
    ax.set_ylim(0, page_height)
    ax.set_title("Chunk grouping")

    out_path = out_dir / "chunks.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("visualize.chunks_saved", file=str(out_path))
    return out_path
