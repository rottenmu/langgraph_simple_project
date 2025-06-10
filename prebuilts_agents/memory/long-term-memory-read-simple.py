import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langgraph.config import get_store
from langgraph.prebuilt import create_react_agent
from langgraph.store.memory import InMemoryStore

load_dotenv()

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("OPEN_API_KEY")
)

store = InMemoryStore()

store.put(
    ("users",),
    "user_123",
    {
        "user_name":"John smith",
        "language":"English"
    }
)

@tool
def get_user_info(config:RunnableConfig) -> str:
    """ Look up user info """
    store = get_store()
    user_id = config["configurable"].get("user_id")
    user_info = store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Unknown user"



agent = create_react_agent(
    model=model,
    tools=[get_user_info],
    store=store
)

result = agent.invoke(
    {"messages":[{"role":"user","content":"look up user information"}]},
    config= {"configurable":{"user_id":"user_123"}},
)

for msg in result["messages"]:
    if isinstance(msg, AIMessage):
        print(msg.content)