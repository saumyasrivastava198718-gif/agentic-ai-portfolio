from src.retrieval import Retriever


retriever = Retriever()

question = "What does Microsoft say about artificial intelligence?"

results = retriever.retrieve(
    question,
    top_k=5
)

print("\nQUESTION:")
print(question)

for i, result in enumerate(results, start=1):
    print(f"\n--- RESULT {i} ---")
    print("Page:", result["page_number"])
    print(result["text"][:700])