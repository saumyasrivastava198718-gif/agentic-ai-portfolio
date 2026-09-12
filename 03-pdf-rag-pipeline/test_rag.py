from src.rag import RAGPipeline


# Create the complete RAG system
rag = RAGPipeline()

# Ask a question about our Microsoft PDF
question = "What does Microsoft say about artificial intelligence?"

# Retrieve evidence + generate answer
result = rag.answer_question(
    question,
    top_k=5
)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(result["answer"])

print("\nSOURCE PAGES:")
print(result["sources"])