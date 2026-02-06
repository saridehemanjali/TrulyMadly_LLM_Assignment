import json
from typing import Dict, Any, Tuple, List
from llm.client import chat_completion
from llm.prompts import VERIFIER_SYSTEM

def verifier_agent(
    task: str,
    plan_dict: Dict[str, Any],
    tool_outputs: Dict[str, Any]
) -> Tuple[str, Dict[str, Any], List[str]]:
    payload = {
        "task": task,
        "plan": plan_dict,
        "tool_outputs": tool_outputs
    }

    raw = chat_completion(VERIFIER_SYSTEM, json.dumps(payload), temperature=0.1)

    try:
        data = json.loads(raw)
    except Exception as e:
        return "ok", {
            "summary": "Verifier returned invalid JSON; returning best-effort output.",
            "task": task,
            "tool_outputs": tool_outputs
        }, [f"Verifier JSON parse error: {str(e)}"]

    status = data.get("status", "ok")
    if status == "retry":
        return "retry", data, data.get("notes", [])
    return "ok", data.get("final_answer", {}), data.get("notes", [])
