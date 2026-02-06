import os
from openai import OpenAI

def get_llm_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").strip()
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in environment (.env).")
    return OpenAI(api_key=api_key, base_url=base_url)

def chat_completion(system: str, user: str, temperature: float = 0.2) -> str:
    client = get_llm_client()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()

    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return resp.choices[0].message.content or ""
