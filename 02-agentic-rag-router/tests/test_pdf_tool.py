from src.tools.pdf_tool import PDFTool


pdf_tool = PDFTool()

question = "What does Microsoft say about artificial intelligence?"

results = pdf_tool.search(
    question=question,
    top_k=5
)


print("\nQUESTION:")
print(question)

print("\nTOP PDF RESULTS:")

for i, result in enumerate(results, start=1):
    print(f"\nRESULT {i}")
    print(f"Page: {result['page_number']}")
    print(f"Distance: {result['distance']}")
    print("Text:")
    print(result["content"][:500])