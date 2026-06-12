import os
from datetime import datetime
from google import genai
import json

from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GIMINI_API_KEY"))

#Doesn't understand this for now.
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs.json")


# Tools

def reply_to_customer(ticket, category,draft, reason):
    log(ticket,category,"reply_to_customer",draft,reason)
    return f"\n{draft} "

def escalate_to_human(ticket,category,draft,reason):
    log(ticket,category,"escalate_to_human",draft,reason)
    return f"Ticket esacalated to Human Agent.\nDraft handed off:\n{draft}"

def close_ticket(ticket,category,draft,reason):
    log(ticket,category,"close_ticket",draft,reason)
    return f"Ticket Closed.\nFinal message:\n{draft}"

def log(ticket: str,category: str,tool:str,draft: str,reason: str):
    entry = {
        "timestamp" : datetime.now().isoformat(),
        "ticket" : ticket,
        "category" : category,
        "tool_used" : tool,
        "reason" : reason,
        "draft" : draft
    }

    logs = []

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE,'r') as f:
            logs = json.load(f)
    logs.append(entry)
    with open(LOG_FILE,'w') as f:
        json.dump(logs,f,indent=2)

def ask_for_more():
    pass

# Agent

tool_map = {
    "reply_to_customer" : reply_to_customer,
    "escalate_to_human" : escalate_to_human,
    "close_ticket" : close_ticket,
    "ask_for_more" : ask_for_more
}


def run_agent(ticket:str):
    history = f"Customer: {ticket}"
    while True:
        prompt = f"""
        You are a customer support agent. Analyze the ticket below and respond ONLY with a JSON object, no markdown, no backticks.
        You can only reply, escalate, or close tickets. You cannot process refunds, access accounts, or take any real actions. Never promise something you cannot do.
        
        Conversation : 
        {history}

        Your response must follow this exact format:
    {{
    "category": "billing | shipping | technical | general",
    "tool": "reply_to_customer | escalate_to_human | close_ticket | ask_for_more",
    "draft": "the message to send to the customer",
    "reason": "why you chose this tool"
    }}
        """
        responce = client.models.generate_content(
            model="models/gemini-3.1-flash-lite-preview",
            contents=prompt
        )

        raw = responce.text.strip()
        decision = json.loads(raw)

        print(decision['draft'])
        if decision['tool'] == 'ask_for_more':
            follow_up = input("You: ")
            history += f"\nAgent: {decision['draft']} \nCustomer: {follow_up}"
            continue

        tool = tool_map[decision['tool']]

        result = tool(
            ticket= ticket,
            category= decision['category'],
            draft= decision['draft'],
            reason= decision['reason']
        )
        
        break

if __name__ == '__main__':
    ticket = input("Enter Customer Ticket: ")
    run_agent(ticket)