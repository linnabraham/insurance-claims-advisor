import argparse
from pathlib import Path

from .config import PipelineConfig
from .inspect import save_chunks
from .logging_config import setup_logging
from .pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the policy-document ingestion pipeline on a single page."
    )
    parser.add_argument("pdf", help="Path to the input PDF.")
    parser.add_argument(
        "--page", type=int, default=0, help="Page index to process (0-based)."
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=800,
        help="Maximum characters per chunk.",
    )
    parser.add_argument(
        "--column-split",
        type=float,
        default=0.5,
        help="Fraction of page width used as the column split (0.0-1.0).",
    )
    parser.add_argument(
        "--layout",
        choices=["single", "two_column"],
        default="two_column",
        help="Page layout assumption.",
    )
    parser.add_argument(
        "--out", default="chunks.json", help="Path to write the chunks JSON file."
    )
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="If set, render PNG visualizations of headings, paragraphs, and chunks.",
    )
    parser.add_argument(
        "--viz-dir",
        default=".",
        help="Directory to write visualization PNGs into (used only with --visualize).",
    )
    args = parser.parse_args()

    setup_logging(dev=True)

    config = PipelineConfig(
        page_num=args.page,
        layout=args.layout,
        column_split=args.column_split,
        max_chunk_chars=args.max_chars,
    )

    result = run_pipeline(args.pdf, config)
    save_chunks(result.chunks, args.out)

    if args.visualize:
        from .visualize import (
            visualize_chunks,
            visualize_headings,
            visualize_paragraphs,
        )

        viz_dir = Path(args.viz_dir)
        viz_dir.mkdir(parents=True, exist_ok=True)
        visualize_headings(
            result.blocks, result.page_width, result.page_height, viz_dir
        )
        visualize_paragraphs(
            result.paragraphs, result.page_width, result.page_height, viz_dir
        )
        visualize_chunks(
            result.paragraphs,
            result.chunks,
            result.page_width,
            result.page_height,
            viz_dir,
        )


if __name__ == "__main__":
    main()
