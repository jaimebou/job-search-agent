#!/usr/bin/env python3
"""
md_to_pdf.py — Converts a Markdown file (CV, cover letter) to a clean PDF.

Usage:
    python3 md_to_pdf.py input.md
    python3 md_to_pdf.py input.md -o output.pdf
    python3 md_to_pdf.py input.md --theme letter   # 'cv' (default) or 'letter'
"""

import argparse
import sys
from pathlib import Path

# ──────────────────────────────────────────────
# CSS Themes
# ──────────────────────────────────────────────

CV_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.55;
    color: #1a1a1a;
    background: white;
    padding: 28mm 22mm 24mm 22mm;
    max-width: 800px;
    margin: 0 auto;
}

/* Name (H1) */
h1 {
    font-size: 24pt;
    font-weight: 600;
    color: #111;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
}

/* Section headers (H2) */
h2 {
    font-size: 11pt;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #444;
    margin-top: 22px;
    margin-bottom: 8px;
    padding-bottom: 4px;
    border-bottom: 1.5px solid #ddd;
}

/* Role / company subheaders (H3) */
h3 {
    font-size: 10.5pt;
    font-weight: 600;
    color: #222;
    margin-top: 12px;
    margin-bottom: 2px;
}

p {
    margin-bottom: 6px;
    color: #333;
}

ul {
    margin: 6px 0 10px 18px;
}

li {
    margin-bottom: 3px;
    color: #333;
}

/* Contact line (italics under H1) */
h1 + p em, h1 + p a {
    color: #555;
    font-size: 9.5pt;
    text-decoration: none;
}

a {
    color: #2563eb;
    text-decoration: none;
}

strong {
    font-weight: 600;
    color: #111;
}

em {
    font-style: italic;
    color: #555;
}

hr {
    border: none;
    border-top: 1px solid #e5e5e5;
    margin: 16px 0;
}

@page {
    size: A4;
    margin: 20mm 18mm;
}
"""

HARVARD_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Times New Roman', Georgia, 'Garamond', serif;
    font-size: 10pt;
    line-height: 1.35;
    color: #1a1a1a;
    background: white;
    padding: 14mm 16mm 12mm 16mm;
    max-width: 800px;
    margin: 0 auto;
}

/* Name (H1) */
h1 {
    font-size: 20pt;
    font-weight: 700;
    color: #111;
    margin-bottom: 3px;
}

/* Section headers (H2) */
h2 {
    font-size: 10.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: #222;
    margin-top: 10px;
    margin-bottom: 4px;
    padding-bottom: 2px;
    border-bottom: 1px solid #999;
}

/* Role / company subheaders (H3) */
h3 {
    font-size: 10pt;
    font-weight: 700;
    color: #111;
    margin-top: 6px;
    margin-bottom: 1px;
}

p {
    margin-bottom: 4px;
    color: #222;
}

ul {
    margin: 3px 0 6px 16px;
}

li {
    margin-bottom: 1px;
    color: #222;
}

/* Contact line (paragraph right under H1) */
h1 + p {
    color: #444;
    font-size: 9.5pt;
    margin-bottom: 6px;
}

a {
    color: #1a1a1a;
    text-decoration: none;
}

strong {
    font-weight: 700;
    color: #111;
}

em {
    font-style: italic;
    color: #444;
}

hr {
    border: none;
    border-top: 1px solid #999;
    margin: 6px 0;
}

@page {
    size: A4;
    margin: 12mm 14mm;
}
"""

LETTER_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.7;
    color: #1a1a1a;
    background: white;
    padding: 30mm 26mm 28mm 26mm;
    max-width: 800px;
    margin: 0 auto;
}

h1 {
    font-size: 14pt;
    font-weight: 600;
    color: #111;
    margin-bottom: 6px;
}

h2 {
    font-size: 11pt;
    font-weight: 600;
    color: #333;
    margin-top: 24px;
    margin-bottom: 8px;
}

p {
    margin-bottom: 12px;
    color: #222;
}

a {
    color: #2563eb;
    text-decoration: none;
}

strong {
    font-weight: 600;
}

em {
    font-style: italic;
    color: #555;
}

@page {
    size: A4;
    margin: 22mm 20mm;
}
"""


def convert(md_path: Path, output_path: Path, theme: str = "cv") -> None:
    try:
        import markdown
    except ImportError:
        print("ERROR: markdown not installed. Run: pip install markdown", file=sys.stderr)
        sys.exit(1)

    try:
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
    except ImportError:
        print("ERROR: weasyprint not installed. Run: pip install weasyprint", file=sys.stderr)
        sys.exit(1)

    md_text = md_path.read_text(encoding="utf-8")

    html_body = markdown.markdown(
        md_text,
        extensions=["extra", "smarty", "toc"],
    )

    css_content = {"cv": CV_CSS, "harvard": HARVARD_CSS, "letter": LETTER_CSS}[theme]

    full_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <style>{css_content}</style>
</head>
<body>
{html_body}
</body>
</html>"""

    font_config = FontConfiguration()
    css = CSS(string=css_content, font_config=font_config)
    HTML(string=full_html, base_url=str(md_path.parent)).write_pdf(
        str(output_path),
        font_config=font_config,
    )

    print(f"Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert Markdown (CV/cover letter) to PDF.")
    parser.add_argument("input", type=Path, help="Input .md file")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Output .pdf file")
    parser.add_argument(
        "--theme",
        choices=["cv", "harvard", "letter"],
        default="cv",
        help="Visual theme: 'cv' (compact, sans-serif), 'harvard' (serif, conservative, 2-page), or 'letter' (spacious prose). Default: cv",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"ERROR: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    output_path = args.output or args.input.with_suffix(".pdf")
    convert(args.input, output_path, theme=args.theme)


if __name__ == "__main__":
    main()
