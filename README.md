# GenAI Assignment — TrulyMadly  
## AI Ops Assistant (Multi-Agent System)

This project implements a **production-ready, multi-agent AI Operations Assistant** as part of the TrulyMadly GenAI Intern assignment.

The system decomposes a user task into a structured plan, executes real API calls, verifies completeness, and produces a final answer — all running locally with a single command.

---

## 🚀 Key Features

- **Multi-Agent Architecture**
  - Planner Agent (LLM-based structured planning)
  - Executor Agent (real API execution)
  - Verifier Agent (validates outputs and retries missing steps once)
- **Structured LLM Outputs** (JSON plans)
- **Integration with Real Third-Party APIs**
- **End-to-End Execution (no hardcoded responses)**
- **Runs locally with one command**

---

## 🧠 Architecture Overview

**Flow:**

User Task
↓
Planner Agent (LLM → JSON Plan)
↓
Executor Agent (API Calls)
↓
Verifier Agent (Validate / Retry)
↓
Final Answer


### Agents

| Agent | Responsibility |
|-----|---------------|
| Planner | Uses an LLM to generate a strict JSON execution plan |
| Executor | Executes each plan step using registered tools (APIs) |
| Verifier | Ensures task completeness and retries missing calls once |

---

## 🔌 Integrated APIs

1. **Groq LLM API**
   - Used by Planner Agent
   - Structured reasoning & planning
   - Model: `llama-3.3-70b-versatile`

2. **OpenWeatherMap API**
   - Fetches real-time weather data
   - Tool: `weather.current_by_city`

3. **GitHub Search API**
   - Searches top repositories by keyword
   - Tool: `github.search_repos`

---

## 📁 Project Structure

trulymadly/
│
├── agents/
│ ├── planner.py
│ ├── executor.py
│ ├── verifier.py
│ ├── schemas.py
│
├── tools/
│ ├── github_tool.py
│ ├── weather_tool.py
│ ├── tool_registry.py
│
├── llm/
│ ├── client.py
│ ├── prompts.py
│
├── main.py
├── requirements.txt
├── .env.example
├── README.md


---

## ⚙️ Setup Instructions (Localhost)

### 1️⃣ Prerequisites
- Python **3.10+**
- Internet connection (for APIs)

---

### 2️⃣ Clone Repository
```bash
git clone <your-github-repo-url>
cd trulymadly
3️⃣ Create Virtual Environment
python -m venv .venv
Activate it:

Windows

.venv\Scripts\activate
Mac/Linux

source .venv/bin/activate
4️⃣ Install Dependencies
pip install -r requirements.txt
5️⃣ Environment Variables
Create a .env file (do NOT commit this):

OPENAI_API_KEY=gsk_your_groq_api_key
OPENAI_BASE_URL=https://api.groq.com/openai/v1
OPENAI_MODEL=llama-3.3-70b-versatile

OPENWEATHER_API_KEY=your_openweather_api_key
GITHUB_TOKEN=your_github_token_optional
Where to get API keys:
Groq: https://console.groq.com/

OpenWeather: https://openweathermap.org/api

GitHub Token (optional but recommended): https://github.com/settings/tokens

▶️ Running the Project
Run with one command:

uvicorn main:app --reload
Then open in browser:

http://localhost:8000
🧪 Example Prompts (Test These)
Weather Only

What's the weather in Mumbai right now?
GitHub Search

Find top 5 GitHub repos for "fastapi jwt auth" and summarize best choice.
Multi-Tool Task

Find top 5 repos for "react markdown editor" and also check weather in Bangalore.
Another Weather Check

What's the current weather in Delhi?
✅ Sample Successful Output
{
  "task": "What's the weather in Mumbai right now?",
  "plan": {...},
  "tool_outputs": {...},
  "final_answer": {
    "city": "Mumbai",
    "weather": "smoke",
    "temperature": 30.99,
    "humidity": 40
  },
  "verifier_notes": [
    "Current weather in Mumbai is provided as requested."
  ]
}
⚠️ Known Limitations / Tradeoffs
Single-turn execution (no conversation memory)

Verifier retries only once to prevent infinite loops

No authentication or user sessions (out of scope)

UI is intentionally minimal (focus on backend logic)

🛡️ Security Notes
.env is excluded via .gitignore

API keys are never hardcoded

.env.example is provided for setup reference



