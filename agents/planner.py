import json
from llm.client import chat_completion
from llm.prompts import PLANNER_SYSTEM
from .schemas import Plan

def planner_agent(task: str) -> Plan:
    user_prompt = f"User task: {task}\nReturn JSON plan only."

    raw = chat_completion(PLANNER_SYSTEM, user_prompt, temperature=0.1)

    try:
        data = json.loads(raw)
    except Exception as e:
        raise ValueError(f"Planner did not return valid JSON.\nRAW:\n{raw}") from e

    return Plan.model_validate(data)
