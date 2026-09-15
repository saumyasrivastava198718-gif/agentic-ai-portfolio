from ddgs import DDGS


class WebSearchTool:
    """Searches the public web and returns normalized results."""

    def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[dict]:
        """Search the web for a query."""

        try:
            raw_results = DDGS().text(
                query=query,
                max_results=max_results,
            )

            results = []

            for item in raw_results:
                results.append(
                    {
                        "title": item.get("title", ""),
                        "url": item.get("href", ""),
                        "snippet": item.get("body", ""),
                    }
                )

            return results

        except Exception as exc:
            print(f"Web search failed: {exc}")
            return []