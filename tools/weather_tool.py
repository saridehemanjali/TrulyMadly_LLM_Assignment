import os
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

OPENWEATHER_API = "https://api.openweathermap.org/data/2.5/weather"

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=6))
async def weather_current_by_city(tool_input: dict) -> dict:
    """
    tool_input:
      {
        "city": "Mumbai",
        "units": "metric"
      }
    """
    api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing OPENWEATHER_API_KEY in environment (.env).")

    city = (tool_input.get("city") or "").strip()
    units = (tool_input.get("units") or "metric").strip()

    if not city:
        raise ValueError("weather.current_by_city requires non-empty 'city'.")

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(
            OPENWEATHER_API,
            params={"q": city, "appid": api_key, "units": units},
        )
        r.raise_for_status()
        data = r.json()

    weather_arr = data.get("weather", []) or [{}]
    main = data.get("main", {}) or {}
    wind = data.get("wind", {}) or {}

    return {
        "city": city,
        "weather": (weather_arr[0].get("description") if weather_arr else None),
        "temp": main.get("temp"),
        "feels_like": main.get("feels_like"),
        "humidity": main.get("humidity"),
        "wind_speed": wind.get("speed"),
    }
