import os
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

GITHUB_API = "https://api.github.com"

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=6))
async def github_search_repos(tool_input: dict) -> dict:
    """
    tool_input:
      {
        "query": "fastapi jwt auth",
        "limit": 5
      }
    """
    query = (tool_input.get("query") or "").strip()
    limit = int(tool_input.get("limit", 5))

    if not query:
        raise ValueError("github.search_repos requires non-empty 'query'.")

    headers = {"Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(
            f"{GITHUB_API}/search/repositories",
            params={"q": query, "sort": "stars", "order": "desc", "per_page": limit},
            headers=headers,
        )
        r.raise_for_status()
        data = r.json()

    results = []
    for repo in data.get("items", []):
        results.append({
            "full_name": repo.get("full_name"),
            "html_url": repo.get("html_url"),
            "description": repo.get("description"),
            "stargazers_count": repo.get("stargazers_count"),
            "language": repo.get("language"),
            "updated_at": repo.get("updated_at"),
            "open_issues_count": repo.get("open_issues_count"),
            "forks_count": repo.get("forks_count"),
        })

    return {"query": query, "results": results}
