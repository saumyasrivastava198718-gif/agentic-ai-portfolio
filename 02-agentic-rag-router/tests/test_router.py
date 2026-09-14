from src.router import Router


router = Router()

questions = [
    "What does the annual report say about artificial intelligence?",
    "What is Microsoft's latest AI announcement?",
    "How has Microsoft's AI strategy changed since the report?"
]

for question in questions:
    decision = router.route(question)

    print("\nQUESTION:")
    print(question)

    print("ROUTE:")
    print(decision.route)

    print("CONFIDENCE:")
    print(decision.confidence)

    print("REASON:")
    print(decision.reason)