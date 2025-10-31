import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent

load_dotenv()


# Create a new session service to store state
session_service_stateful = InMemorySessionService()

initial_state = {
    "user_name": "Matthew Fee",
    "user_preferences": """
        I like to play BoardGames, Hike, Camp, and Ski.
        My favorite Food is Asian. 
        My favorite Tv Show is Arrested Development. 
        I am looking for a new job where I can build AI applications.
    """,
}

# Create a new session with initial state
APP_NAME = "Matt Fee"
USER_ID = "matt_fee"
SESSION_ID = str(uuid.uuid4())  
stateful_session = session_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)
print("CREATED NEW SESSION:")
print(f"\tSession ID: {SESSION_ID}")

runner = Runner(
    agent=question_answering_agent,
    app_name=APP_NAME,
    session_service=session_service_stateful,
)

new_message = types.Content(
    role="user", parts=[types.Part(text="What is Matt's favorite Tv Show?")]
)

for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message,
):
    if event.is_final_response():
        if event.response.content and event.content.parts:
            print(f"Final Response: {event.content.parts[0].text}")

print("=== Session Event Exploration ===")
session = session_service_stateful.get_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
)

# Log the final Session state
print("=== FINAL SESSION STATE ===")
for key, value in session.state.items():
    print(f"{key}: {value}")