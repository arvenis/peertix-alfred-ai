import json
import os
import requests
from crewai_tools import BaseTool


class InstagramAPITool(BaseTool):
    name: str = "Instagram API Tool"
    description: str = "This tool allows you to search for instagram post about a given topic and return relevant"

    def search_instagram(self, query):
        query = f"site:instagram.com {query}"
        return InstagramAPITool.search(query)

    # todo: this is basicially crewai's SerperDevTool(), might be better to use the built in instead of crafting it
    def search(query, n_results=5):
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {"X-API-KEY": os.environ["SERPER_API_KEY"], "content-type": "application/json"}
        response = requests.request("POST", url, headers=headers, data=payload)
        results = response.json()["organic"]
        stirng = []
        for result in results[:n_results]:
            try:
                stirng.append(
                    "\n".join(
                        [
                            f"Title: {result['title']}",
                            f"Link: {result['link']}",
                            f"Snippet: {result['snippet']}",
                            "\n-----------------",
                        ]
                    )
                )
            except KeyError:
                next

        content = "\n".join(stirng)
        return f"\nSearch result: {content}\n"

    def _run(self, artist_name: str) -> str:
        return ""
