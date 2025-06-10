import os
from typing import Annotated

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.constants import START
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import InjectedState, create_react_agent
from langgraph.types import Command

load_dotenv()

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("OPEN_API_KEY")
)

def create_handoff_tool(*,agent_name: str,description: str | None = None,):
    name = f"transfer_to_{agent_name}"
    description = description or f"transfer_to_{agent_name}"

    @tool(name, description=description)
    def handoff_tool(
            state: Annotated[MessagesState, InjectedState],
            tool_call_id:Annotated[str, InjectedToolCallId]
    ) -> Command:
        tool_message ={
            "role": "tool",
            "content":f"Successfully transferred to {agent_name}",
            "name":name,
            "tool_call_id":tool_call_id
        }

        return Command(
            goto=agent_name,
            update={"messages": state["messages"] + [tool_message]},
            graph=Command.PARENT

        )
    return handoff_tool

#handoffs
transfer_to_hotel_assistant = create_handoff_tool(
    agent_name="hotel_assistant",
    description="Transfer user to the hotel-booking assistant."
)

transfer_to_flight_assistant = create_handoff_tool(
    agent_name="flight_assistant",
    description="Transfer user to the flight-booking assistant."
)

#tools
@tool
def book_hotel(hotel_name: str):
    """Book hotel """
    return f"Successfully booked a stay at {hotel_name}."


@tool
def book_flight(from_airport: str, to_airport: str):
    """book flight"""
    return f"Successfully booked a flight from {from_airport} to {to_airport}."

#agents
flight_assistant = create_react_agent(
    model=model,
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

#graph
multi_agent_graph = (
    StateGraph(MessagesState)
    .add_node(flight_assistant)
    .add_node(hotel_assistant)
    .add_edge(START, "flight_assistant")
    .compile()
)

#Run the multi-agent graph
for chunk in multi_agent_graph.stream(
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
