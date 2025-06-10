import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph_swarm import create_swarm, create_handoff_tool


def book_hotel(hotel_name: str):
    """Book a hotel"""
    print(f"Successfully booked a stay at {hotel_name}.")
    return f"Successfully booked a stay at {hotel_name}."

def book_flight(from_airport: str, to_airport: str):
    """Book a flight"""
    print(f"Successfully booked a flight from {from_airport} to {to_airport}.")
    return f"Successfully booked a flight from {from_airport} to {to_airport}."

transfer_to_hotel_assistant = create_handoff_tool(
    agent_name="hotel_assistant",
    description="Transfer user to the hotel-booking assistant.",
)
transfer_to_flight_assistant = create_handoff_tool(
    agent_name="flight_assistant",
    description="Transfer user to the flight-booking assistant.",
)

load_dotenv()

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("OPEN_API_KEY")
)

flight_assistant = create_react_agent(
    model= model,
    tools=[book_flight, transfer_to_hotel_assistant],
    prompt="You are a flight booking assistant",
    name="flight_assistant"
)
hotel_assistant = create_react_agent(
    model=model,
    tools=[book_hotel, transfer_to_flight_assistant],
    prompt="You are a hotel booking assistant",
    name="hotel_assistant"
)

swarm = create_swarm(
    agents=[flight_assistant, hotel_assistant],
    default_active_agent="flight_assistant"
).compile()

# for chunk in swarm.stream(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "book a flight from BOS to JFK and a stay at McKittrick Hotel"
#             }
#         ]
#     }
# ):
#     print(chunk)
#     print("\n")
