#!/usr/bin/env python3
"""
pdf_to_md.py — Converts a PDF (e.g. a CV) to clean Markdown.

Usage:
    python3 pdf_to_md.py input.pdf
    python3 pdf_to_md.py input.pdf -o output.md
    python3 pdf_to_md.py input.pdf --stdout
"""

import argparse
import re
import sys
from pathlib import Path


def extract_text_blocks(pdf_path: Path) -> list[dict]:
    """Extract text blocks with font size metadata using pdfplumber."""
    try:
        import pdfplumber
    except ImportError:
        print("ERROR: pdfplumber not installed. Run: pip install pdfplumber", file=sys.stderr)
        sys.exit(1)

    blocks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words(
                extra_attrs=["size", "fontname"],
                use_text_flow=True,
            )
            if not words:
                continue

            current_line = []
            current_y = None
            current_size = None

            for word in words:
                y = round(word["top"], 1)
                size = round(word.get("size", 10), 1)

                if current_y is None:
                    current_y = y
                    current_size = size

                # New line when vertical position changes significantly
                if abs(y - current_y) > 3:
                    if current_line:
                        blocks.append({
                            "text": " ".join(current_line),
                            "size": current_size,
                            "y": current_y,
                        })
                    current_line = [word["text"]]
                    current_y = y
                    current_size = size
                else:
                    current_line.append(word["text"])

            if current_line:
                blocks.append({
                    "text": " ".join(current_line),
                    "size": current_size,
                    "y": current_y,
                })

    return blocks


def classify_block(text: str, size: float, all_sizes: list[float]) -> str:
    """Classify a text block as h1, h2, h3, or paragraph based on font size."""
    if not all_sizes:
        return "paragraph"

    max_size = max(all_sizes)
    median_size = sorted(all_sizes)[len(all_sizes) // 2]

    # Heuristic thresholds relative to the document's font range
    if size >= max_size * 0.92:
        return "h1"
    elif size >= median_size * 1.25:
        return "h2"
    elif size >= median_size * 1.10:
        return "h3"
    return "paragraph"


def blocks_to_markdown(blocks: list[dict]) -> str:
    """Convert classified blocks to Markdown text."""
    all_sizes = [b["size"] for b in blocks if b["size"]]
    lines = []
    prev_type = None

    for block in blocks:
        text = block["text"].strip()
        if not text:
            continue

        block_type = classify_block(text, block["size"], all_sizes)

        # Add spacing between sections
        if prev_type and block_type != prev_type:
            lines.append("")

        if block_type == "h1":
            lines.append(f"# {text}")
        elif block_type == "h2":
            lines.append(f"## {text}")
        elif block_type == "h3":
            lines.append(f"### {text}")
        else:
            # Detect bullet-like lines
            if re.match(r"^[•·▪▸‣◦➤\-–—]\s", text):
                text = re.sub(r"^[•·▪▸‣◦➤\-–—]\s*", "- ", text)
            lines.append(text)

        prev_type = block_type

    # Clean up: collapse 3+ consecutive blank lines into 2
    output = "\n".join(lines)
    output = re.sub(r"\n{3,}", "\n\n", output)
    return output.strip()


def convert(pdf_path: Path) -> str:
    blocks = extract_text_blocks(pdf_path)
    return blocks_to_markdown(blocks)


def main():
    parser = argparse.ArgumentParser(description="Convert a PDF to Markdown.")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Output .md file (default: same name as input)")
    parser.add_argument("--stdout", action="store_true", help="Print Markdown to stdout instead of writing a file")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"ERROR: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    md_content = convert(args.input)

    if args.stdout:
        print(md_content)
        return

    output_path = args.output or args.input.with_suffix(".md")
    output_path.write_text(md_content, encoding="utf-8")
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
