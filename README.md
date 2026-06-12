# Support Ticket Agent

An AI-powered customer support agent built from scratch using Python and the Gemini API. This is part of my learning journey as a self-taught AI developer working toward becoming an AI Agent Developer.

## Background

This project was built without any agent frameworks — just Python and the Gemini API. The goal was to understand how agents work at a fundamental level before using tools like LangChain to abstract the complexity away. A LangChain version of this agent is planned as the next iteration.

## What the agent does

The agent reads a customer support ticket, holds a multi-turn conversation if it needs more information, then makes a final decision on how to handle it.

```
Customer sends ticket
  ↓
Agent classifies it (billing, shipping, technical, general)
  ↓
Agent chooses a tool:
  → reply_to_customer   — drafts and sends a response
  → escalate_to_human   — hands off to a human agent
  → close_ticket        — closes resolved or spam tickets
  → ask_for_more        — asks a follow-up question (no log, keeps conversation going)
  ↓
Final decision gets logged to logs.json
```

## What I learned building this

- How to structure an agent loop from scratch without a framework
- How to use the model's JSON output to make real decisions in code (tool routing)
- The difference between tools that feed information back to the model vs tools that just execute a decision

## Stack

- Python
- Gemini API (`google-genai`)

## Setup

1. Clone the repo
2. Install dependencies:
```bash
pip install google-genai python-dotenv
```
3. Create a `.env` file:
```
GOOGLE_API_KEY=your_key_here
```
4. Run the agent:
```bash
python agent.py
```

## Author

Saad — self-taught AI developer based in Agadir, Morocco  
GitHub: [github.com/Saadbihmid](https://github.com/Saadbihmid)
