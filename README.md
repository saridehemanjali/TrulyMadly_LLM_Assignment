AI Operations Assistant

An AI-powered assistant that takes a natural-language task, breaks it into steps, calls real APIs, and returns a structured answer — all running locally.

This project demonstrates agent-based reasoning using three agents:

Planner – understands the user request and creates a step-by-step plan

Executor – executes the plan and calls real APIs (GitHub, Weather, etc.)

Verifier – checks results, fixes missing data, and formats the final output

The system uses an LLM for reasoning (not monolithic prompts) and integrates multiple real-world APIs with proper error handling and retries.

Tech Stack

Python

LLM (OpenAI / Groq)

GitHub API

Weather API

Multi-agent architecture

Project Structure
ai_ops_assistant/
│── agents/
│── tools/
│── llm/
│── main.py
│── requirements.txt
│── .env.example
│── README.md

How to Run
pip install -r requirements.txt
cp .env.example .env
python main.py "Get weather in Bangalore and find top Python repos"

Highlights

Real API integrations

Planner → Executor → Verifier flow

Structured JSON planning

Runs locally on localhost / CLI
