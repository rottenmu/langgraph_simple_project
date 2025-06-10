import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage, AIMessage
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from langgraph.prebuilt.chat_agent_executor import AgentState, create_react_agent
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

@tool
def get_user_info(state :Annotated[CustomState, InjectedState]) -> str:
    """Get user information """
    user_id = state["user_id"]
    return "User is John Smith" if user_id == "user123" else "Unknown user"

agent = create_react_agent(
    model=model,
    state_schema=CustomState,
    tools=[get_user_info],
)


agent_response= agent.invoke({"messages":"look up user information","user_id":"user123"})

messages = agent_response.get("messages")


for msg in messages:
    if isinstance(msg, AIMessage):
        print(msg.content)

