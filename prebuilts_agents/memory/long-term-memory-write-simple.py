import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langgraph.config import get_store
from langgraph.prebuilt import create_react_agent
from langgraph.store.memory import InMemoryStore
from typing_extensions import TypedDict

load_dotenv()

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("OPEN_API_KEY")
)

store = InMemoryStore()

class UserInfo(TypedDict):
     name: str

@tool
def save_user_info (
        user_info: UserInfo,
        config:RunnableConfig
) -> str:
    """save user info """
    store = get_store()
    user_id = config["configurable"].get("user_id")
    store.put(("users",), user_id, user_info)
    return "Successfully saved user info"


agent = create_react_agent(
    model=model,
    tools=[save_user_info],
    store=store
)

result = agent.invoke(
    {"messages":[{"role":"user","content":"我的名字叫张三"}]},
    config={"configurable":{"user_id":"user_123"}}
)

print(store.get(("users",), "user_123").value)
print("********************")
for msg in result["messages"]:
    if isinstance(msg, AIMessage):
        print(msg.content)

