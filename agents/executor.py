from typing import Dict, Any
from .schemas import Plan
from tools.tool_registry import TOOLS

async def executor_agent(plan: Plan) -> Dict[str, Any]:
    memory: Dict[str, Any] = {}

    for step in plan.steps:
        if step.tool is None:
            continue

        tool_fn = TOOLS.get(step.tool)
        key = step.save_as or step.id

        if not tool_fn:
            memory[key] = {"error": f"Unknown tool: {step.tool}"}
            continue

        try:
            memory[key] = await tool_fn(step.tool_input or {})
        except Exception as e:
            memory[key] = {"error": str(e), "tool": step.tool}

    return memory
