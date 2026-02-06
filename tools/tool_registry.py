from typing import Dict, Any, Callable, Awaitable
from .github_tool import github_search_repos
from .weather_tool import weather_current_by_city

ToolFn = Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]

TOOLS: Dict[str, ToolFn] = {
    "github.search_repos": github_search_repos,
    "weather.current_by_city": weather_current_by_city,
}
