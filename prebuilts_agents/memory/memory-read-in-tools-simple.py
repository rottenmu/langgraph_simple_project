import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage
from langgraph.prebuilt import InjectedState, create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from typing_extensions import Annotated

load_dotenv()

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("OPEN_API_KEY")
)


class CustomState(AgentState):
    user_id:str

def get_user_info(state: Annotated[CustomState,InjectedState]) -> str:
    """look up user info"""
    user_id = state["user_id"]
    return "User is John Smith" if user_id == "user123" else "Unknown"


agent = create_react_agent(
    model=model,
    tools=[get_user_info],
    state_schema=CustomState
)

agent_result = agent.invoke({"messages":" look up user information", "user_id":"user123"})

for msg in agent_result["messages"]:
    if isinstance(msg, AIMessage):
        print(msg.content)

