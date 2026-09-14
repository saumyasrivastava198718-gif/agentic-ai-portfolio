from src.orchestrator import Orchestrator


orchestrator = Orchestrator()

question = (
    "What does the Microsoft annual report "
    "say about artificial intelligence?"
)

result = orchestrator.answer(question)


print("\n==============================")
print("ROUTE")
print("==============================")
print(result["route"])


print("\n==============================")
print("CONFIDENCE")
print("==============================")
print(result["confidence"])


print("\n==============================")
print("ROUTING REASON")
print("==============================")
print(result["reason"])


print("\n==============================")
print("FINAL ANSWER")
print("==============================")
print(result["answer"])


print("\n==============================")
print("SOURCES")
print("==============================")


for item in result["evidence"][:5]:

    if item["source_type"] == "pdf":

        print(
            f"PDF page: "
            f"{item.get('page_number')}"
        )

    else:

        print(
            f"{item.get('source_name')} - "
            f"{item.get('url')}"
        )