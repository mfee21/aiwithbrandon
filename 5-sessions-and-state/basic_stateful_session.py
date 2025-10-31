import uuid
import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent

load_dotenv()

async def main():
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
    stateful_session = await session_service_stateful.create_session(  # Await the async method
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
        session_id=SESSION_ID,
    )
    print("CREATED NEW SESSION:")
    print(f"\tSession ID: {SESSION_ID}")

    runner = Runner(
        app_name=APP_NAME,
        agent=question_answering_agent,
        session_service=session_service_stateful,
    )

    new_message = types.Content(
        parts=[types.Part(text="What is Matt's favorite Tv Show?")], role="user"
    )

    for event in runner.run(  # Use regular `for` loop if `runner.run` is not asynchronous
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                print(f"Final Response: {event.content.parts[0].text}")

    print("==== Session Event Exploration ====")
    session = await session_service_stateful.get_session(  # Await the async method
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    # Log final Session state
    print("=== Final Session State ===")
    for key, value in session.state.items():
        print(f"{key}: {value}")

# Run the main function
asyncio.run(main())