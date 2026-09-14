from src.orchestrator import Orchestrator


orchestrator = Orchestrator()

question = "What does the annual report say about artificial intelligence?"

result = orchestrator.retrieve(question)

print("\nROUTE:")
print(result["route"])

print("\nCONFIDENCE:")
print(result["confidence"])

print("\nREASON:")
print(result["reason"])

print("\nEVIDENCE:")
for item in result["evidence"][:3]:
    print(item)