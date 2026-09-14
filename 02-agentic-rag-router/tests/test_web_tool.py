from src.tools.web_tool import WebTool


web_tool = WebTool()

question = "Microsoft latest artificial intelligence announcement"

results = web_tool.search(
    question=question,
    top_k=3
)

print("\nQUESTION:")
print(question)

print("\nWEB RESULTS:")

for i, result in enumerate(results, start=1):
    print(f"\nRESULT {i}")
    print("Source:", result["source_name"])
    print("URL:", result["url"])
    print("Content:")
    print(result["content"][:400])