# pip install -qU "langchain[anthropic]" to call the model
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

#添加内存
memory = InMemorySaver()

load_dotenv()

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("OPEN_API_KEY")
)
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"他总是晴天在 {city}!"

class WeatherResponse(BaseModel):
    conditions: str

agent = create_react_agent(
    model= model,
    tools=[get_weather],
    checkpointer=memory
)

agent.get_graph().draw_png()
config = {"configurable":{"thread_id":"abc123"}}

# Run the agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "杭州的天气怎么样呢"}]},
    config=config
)

print(result)
