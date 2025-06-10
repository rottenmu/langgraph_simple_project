import os
from typing import Annotated

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import ToolMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import InjectedState, create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.types import Command

load_dotenv()

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("OPEN_API_KEY")
)


class CustomState(AgentState):
    user_name: str

def update_user_info(
        tool_call_id: Annotated[str, InjectedToolCallId],
        config: RunnableConfig
) -> Command:
    """Look up and update user information """
    user_id = config["configurable"].get("user_id")
    name = "John Smith" if user_id =="user_123" else "Unknown user"
    return Command(update={
        "user_name":name,
        "messages":[
            ToolMessage(
                "successfully looked up user information",
                tool_call_id=tool_call_id
            )
        ]
    })

def greet (
        state:Annotated[CustomState, InjectedState]
) -> str:
    """一旦你找到了用户的信息，就用这个来问候他们"""
    user_name = state["user_name"]
    return f"Hello {user_name}!"



agent = create_react_agent(
    model=model,
    tools=[update_user_info, greet],
    state_schema=CustomState,
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "greet the user"}]},
    config={"configurable": {"user_id": "user_123"}}
)

for msg in result["messages"]:
    if isinstance(msg, AIMessage):
        print(msg.content)
