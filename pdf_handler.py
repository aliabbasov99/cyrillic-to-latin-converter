"""
PDF processing module.

Uses PyMuPDF (fitz) to:
  1. Open a PDF file
  2. Extract text spans from every page
  3. Transliterate Cyrillic → Latin using converter.convert_text()
  4. Re-insert the transliterated text while preserving layout,
     font size, color, and positioning
  5. Save as a new PDF
"""

import os
import fitz  # PyMuPDF
from converter import convert_text


def process_pdf(input_path: str, output_path: str | None = None) -> str:
    """
    Convert all Cyrillic text in a PDF to Latin script.

    Args:
        input_path:  Path to the source PDF file.
        output_path: Where to save the result. If None, auto-generates
                     a path like ``original_latin.pdf``.

    Returns:
        The absolute path of the generated output file.
    """
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_latin{ext}"

    doc = fitz.open(input_path)

    for page in doc:
        # Get all text with detailed span info
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]

        for block in blocks:
            if block.get("type") != 0:  # skip image blocks
                continue

            for line in block["lines"]:
                for span in line["spans"]:
                    original = span["text"]
                    converted = convert_text(original)

                    if converted == original:
                        continue  # nothing changed, skip

                    # Erase original text by drawing a white rectangle
                    rect = fitz.Rect(span["bbox"])
                    page.add_redact_annot(rect)

        # Apply all redactions (removes old text)
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

        # Second pass: re-insert converted text
        blocks = fitz.open(input_path)[page.number].get_text(
            "dict", flags=fitz.TEXT_PRESERVE_WHITESPACE
        )["blocks"]

        for block in blocks:
            if block.get("type") != 0:
                continue

            for line in block["lines"]:
                for span in line["spans"]:
                    original = span["text"]
                    converted = convert_text(original)

                    if not converted.strip():
                        continue

                    rect = fitz.Rect(span["bbox"])
                    fontsize = span["size"]
                    color = _int_to_rgb(span["color"])

                    # Choose a font that supports Azerbaijani characters
                    # fitz built-in "helv" (Helvetica) is safe for Latin
                    page.insert_textbox(
                        rect,
                        converted,
                        fontsize=fontsize,
                        fontname="helv",
                        color=color,
                        align=fitz.TEXT_ALIGN_LEFT,
                    )

    doc.save(output_path, garbage=4, deflate=True)
    doc.close()

    return os.path.abspath(output_path)


def _int_to_rgb(color_int: int) -> tuple[float, float, float]:
    """Convert an integer color (0xRRGGBB) to (r, g, b) floats in [0,1]."""
    r = ((color_int >> 16) & 0xFF) / 255.0
    g = ((color_int >> 8) & 0xFF) / 255.0
    b = (color_int & 0xFF) / 255.0
    return (r, g, b)
