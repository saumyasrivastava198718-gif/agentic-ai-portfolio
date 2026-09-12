from src.ingestion import extract_text_from_pdf
from src.chunking import chunk_pages


pdf_path = "data/documents/microsoft_2025_annual_report.pdf"

pages = extract_text_from_pdf(pdf_path)

print(f"Total pages extracted: {len(pages)}")


chunks = chunk_pages(
    pages,
    chunk_size=1000,
    chunk_overlap=200
)

print(f"Total chunks created: {len(chunks)}")


print("\n--- FIRST CHUNK ---\n")
print(chunks[0]["text"])

print("\n--- CHUNK METADATA ---")
print("Chunk ID:", chunks[0]["chunk_id"])
print("Page number:", chunks[0]["page_number"])