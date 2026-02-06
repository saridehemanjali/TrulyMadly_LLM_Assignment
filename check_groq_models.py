import os
from dotenv import load_dotenv
import httpx

load_dotenv(override=True)

BASE_URL = os.getenv("OPENAI_BASE_URL", "").rstrip("/")
KEY = os.getenv("OPENAI_API_KEY", "")

if not BASE_URL or not KEY:
    raise SystemExit("Missing OPENAI_BASE_URL or OPENAI_API_KEY in .env")

url = f"{BASE_URL}/models"
headers = {"Authorization": f"Bearer {KEY}"}

with httpx.Client(timeout=30) as client:
    r = client.get(url, headers=headers)
    print("Status:", r.status_code)
    data = r.json()

    print("\nAvailable models:\n")
    for m in data.get("data", []):
        print(m["id"])
