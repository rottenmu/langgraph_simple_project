import os
from typing import TypedDict, Annotated

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.runnables.graph import MermaidDrawMethod
from langchain_core.tools import tool
from langgraph.constants import START, END
from langgraph.graph import MessagesState, add_messages, StateGraph
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor


@tool
def book_hotel(hotel_name: str):
    """Book hotel """
    return f"Successfully booked a stay at {hotel_name}"


@tool
def book_flight(from_airport: str, to_airport: str):
    """book flight"""
    return f"Successfully booked a flight from {from_airport} to {to_airport}"


load_dotenv()

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("OPEN_API_KEY")
)

flight_assistant = create_react_agent(
    model=model,
    tools=[book_flight],
    prompt=
    "You are a flight booking assistant"
    "For current events, use flight_assistant.",

    name="flight_assistant"
)

hotel_assistant = create_react_agent(
    model=model,
    tools=[book_hotel],
    prompt="You are a hotel booking assistant",
    name="hotel_assistant"
)

class State(TypedDict):
    messages: Annotated[list, add_messages]

supervisor = create_supervisor(
    agents=[flight_assistant, hotel_assistant],
    model=model,
    prompt=(
        "You manage a hotel booking assistant and a"
        "flight booking assistant. Assign work to them."
    )
).compile()

img = supervisor.get_graph().draw_mermaid_png(
            draw_method=MermaidDrawMethod.API,
        )
with open("graph.png", "wb") as f:
    f.write(img)
    f.close()


for chunk in supervisor.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": "book a flight from BOS to JFK and a stay at McKittrick Hotel"
            }
        ]
    }
):
    print(chunk)
    print("\n")