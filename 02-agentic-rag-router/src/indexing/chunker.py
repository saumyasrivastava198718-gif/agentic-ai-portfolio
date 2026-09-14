def chunk_pages(
    pages,
    chunk_size: int = 1000,
    overlap: int = 150
):
    chunks = []

    chunk_id = 0

    for page in pages:
        text = page["text"]
        page_number = page["page_number"]

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "chunk_id": f"chunk-{chunk_id}",
                        "page_number": page_number,
                        "text": chunk_text
                    }
                )

                chunk_id += 1

            start += chunk_size - overlap

    return chunks