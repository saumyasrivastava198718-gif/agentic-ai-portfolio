import pymupdf


def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """
    Extract text from a PDF page by page.

    Returns:
        List of dictionaries containing page number and text.
    """

    document = pymupdf.open(pdf_path)

    pages = []

    try:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text")

            pages.append(
                {
                    "page_number": page_number,
                    "text": text,
                }
            )
    finally:
        document.close()

    return pages