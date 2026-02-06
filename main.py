from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from agents.planner import planner_agent
from agents.executor import executor_agent
from agents.verifier import verifier_agent
from tools.tool_registry import TOOLS

# IMPORTANT: prefer .env over any system environment variables
load_dotenv(override=True)

app = FastAPI(title="TrulyMadly GenAI Assignment - AI Ops Assistant", version="1.0.0")


class RunRequest(BaseModel):
    task: str


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
      <head>
        <title>AI Ops Assistant</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body style="font-family: Arial; max-width: 900px; margin: 26px auto; padding: 0 14px;">
        <h2>AI Ops Assistant (Planner → Executor → Verifier)</h2>
        <p>Runs locally. Output includes plan + tool outputs + final answer.</p>

        <div style="background:#f5f5f5; padding:12px; border-radius:8px;">
          <b>Example prompts:</b>
          <ul>
            <li>Find top 5 GitHub repos for "fastapi jwt auth" and summarize best choice.</li>
            <li>What's the weather in Mumbai right now?</li>
            <li>Find top 5 repos for "react markdown editor" and also check weather in Bangalore.</li>
          </ul>
        </div>

        <textarea id="task" rows="4" style="width:100%; margin-top:12px;" placeholder="Type your task here..."></textarea><br/><br/>
        <button onclick="runTask()" style="padding:10px 14px; cursor:pointer;">Run</button>
        <pre id="out" style="margin-top:16px; background:#111; color:#0f0; padding:12px; border-radius:8px; overflow:auto; min-height:220px;"></pre>

        <script>
          async function runTask(){
            const task = document.getElementById('task').value;
            const out = document.getElementById('out');
            out.textContent = "Running...";
            try {
              const res = await fetch('/run', {
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body: JSON.stringify({task})
              });
              const data = await res.json();
              out.textContent = JSON.stringify(data, null, 2);
            } catch (e) {
              out.textContent = "Request failed: " + e;
            }
          }
        </script>
      </body>
    </html>
    """


@app.post("/run")
async def run(req: RunRequest):
    task = (req.task or "").strip()
    if not task:
        return {"error": "Task is empty. Please enter a task and try again."}

    # 1) Planner -> JSON plan
    try:
        plan = planner_agent(task)
    except Exception as e:
        return {
            "task": task,
            "error": "Planner failed (LLM auth/config/timeout). Check .env values for OPENAI_API_KEY / OPENAI_BASE_URL / OPENAI_MODEL.",
            "details": str(e),
        }

    # 2) Executor -> tool outputs
    try:
        tool_outputs = await executor_agent(plan)
    except Exception as e:
        return {
            "task": task,
            "plan": plan.model_dump(),
            "error": "Executor failed while calling tools/APIs.",
            "details": str(e),
        }

    # 3) Verifier -> validate + retry missing calls ONCE
    try:
        status, verifier_data, notes = verifier_agent(task, plan.model_dump(), tool_outputs)
    except Exception as e:
        return {
            "task": task,
            "plan": plan.model_dump(),
            "tool_outputs": tool_outputs,
            "error": "Verifier failed while validating results.",
            "details": str(e),
        }

    if status == "retry":
        missing_calls = verifier_data.get("missing_calls", [])
        notes = (notes or []) + verifier_data.get("notes", [])

        for call in missing_calls:
            tool = call.get("tool")
            tool_input = call.get("tool_input", {})
            save_as = call.get("save_as", tool)

            tool_fn = TOOLS.get(tool)
            if tool_fn:
                try:
                    tool_outputs[save_as] = await tool_fn(tool_input)
                except Exception as e:
                    tool_outputs[save_as] = {"error": str(e), "tool": tool}
            else:
                tool_outputs[save_as] = {"error": "Unknown tool", "tool": tool}

        # Verify again after retry
        try:
            _, final_answer, notes2 = verifier_agent(task, plan.model_dump(), tool_outputs)
        except Exception as e:
            return {
                "task": task,
                "plan": plan.model_dump(),
                "tool_outputs": tool_outputs,
                "error": "Verifier failed after retry.",
                "details": str(e),
                "verifier_notes": notes,
            }

        return {
            "task": task,
            "plan": plan.model_dump(),
            "tool_outputs": tool_outputs,
            "final_answer": final_answer,
            "verifier_notes": notes + (notes2 or []),
        }

    return {
        "task": task,
        "plan": plan.model_dump(),
        "tool_outputs": tool_outputs,
        "final_answer": verifier_data,
        "verifier_notes": notes,
    }
