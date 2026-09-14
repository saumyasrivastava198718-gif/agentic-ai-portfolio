from ddgs import DDGS


class WebTool:
    def search(self, question: str, top_k: int = 5):
        evidence = []

        try:
            results = DDGS().text(
                query=question,
                max_results=top_k
            )

            for result in results:
                evidence.append(
                    {
                        "content": result.get("body", ""),
                        "source_type": "web",
                        "source_name": result.get(
                            "title",
                            "Web result"
                        ),
                        "url": result.get("href")
                    }
                )

        except Exception as error:
            print(
                f"\nWeb search failed: "
                f"{type(error).__name__}: {error}\n"
            )

        return evidence