import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState


load_dotenv()

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("OPEN_API_KEY")
)

@tool
def get_user_info(config :RunnableConfig):
    """Get user information"""
    user_id = config["configurable"].get("user_id")
    return "User is John Smith," if user_id == "user123" else "Unknown user"


agent = create_react_agent(
    model= model,
    tools=[get_user_info],
)

agent_response =agent.invoke(
    {"messages":[{"role":"user", "content":"look up user information"}]},

    config={"configurable": {"user_id": "user1234"}}
)

print(agent_response)


