import os 
import random
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(
    model="openai/gpt-5-mini-2025-08-07",
    api_key=os.getenv("OPENAI_API_KEY"),
)

def get_dad_joke():
    """A simple tool that returns a dad joke."""
    jokes = ["Why did the chicken cross the road? To get to the other side!",
        "What do you call a belt made of watches? A waist of time.",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",]
    return random.choice(jokes)

root_agent = Agent(
    name="dad_joke_agent",
    model=model,
    description="Agent that tells dad jokes.",
    instruction="""
    You are a dad joke telling agent.
    Only use the following tool to help you:
    - get_dad_joke: Use this tool to get a dad joke.
    """,
    tools=[get_dad_joke],
)