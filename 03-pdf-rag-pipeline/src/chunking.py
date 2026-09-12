def chunk_pages(
    pages,
    chunk_size=1000,
    chunk_overlap=200
):
    """
    Split page text into overlapping chunks.

    Args:
        pages: List of page dictionaries.
        chunk_size: Maximum number of characters per chunk.
        chunk_overlap: Number of overlapping characters.

    Returns:
        List of chunk dictionaries.
    """

    chunks = []

    for page in pages:
        text = page["text"]
        page_number = page["page_number"]

        start = 0
        chunk_id = 0

        while start < len(text):
            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "chunk_id": f"page_{page_number}_chunk_{chunk_id}",
                    "page_number": page_number,
                    "text": chunk_text
                })

            chunk_id += 1

            start += chunk_size - chunk_overlap

    return chunks