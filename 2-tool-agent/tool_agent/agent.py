from datetime import datetime
from google.adk.agents import Agent
from google.adk.tools import google_search

def get_current_time() -> dict:
    """A simple tool that returns the current time."""
    return {"current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

root_agent = Agent(
    name="tool_agent",
    model="gemini-2.5-flash",
    description="Agent that uses tools to assist the user.",
    instruction="""
    You are a helpful assistant that can use tools to assist the user.
    Use the following tools to help you:
    - get_current_time: Use this tool to get the current time.
    """,
    tools=[get_current_time],
)