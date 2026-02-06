from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal

ToolName = Literal["github.search_repos", "weather.current_by_city"]

class PlanStep(BaseModel):
    id: str = Field(..., description="Unique step id like step_1")
    action: str = Field(..., description="What to do in this step")
    tool: Optional[ToolName] = Field(None, description="Tool to call, if any")
    tool_input: Optional[Dict[str, Any]] = Field(None, description="Tool input JSON")
    save_as: Optional[str] = Field(None, description="Memory key for tool output")

class Plan(BaseModel):
    task: str
    steps: List[PlanStep]
    final_output_format: Literal["json", "markdown"] = "json"
