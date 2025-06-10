import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.config import get_stream_writer
from langgraph.prebuilt import create_react_agent

load_dotenv()

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("OPEN_API_KEY")
)
tool = TavilySearch(max_result=2 ,tavily_api_key="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")


def get_weather(city: str) ->str:
    """获取提供城市的天气预报"""
    writer = get_stream_writer()
    writer(f"查询这个城市的数据:{city}")
    return f"它总是在{city}晴天"

# def get_weather(city: str) -> str:
#     """Get weather for a given city."""
#     writer = get_stream_writer()
#     # stream any arbitrary data
#     writer(f"Looking up data for city: {city}")
#     return f"It's always sunny in {city}!"

agent = create_react_agent(
    model=model,
    tools=[get_weather]
)

# for chunk in agent.stream(
#         {"messages":[{"role":"user","content":"杭州今天的天气怎么样呢"}]},
#     stream_mode="updates"
# ):

# for token, metadata in agent.stream(
#         {"messages":[{"role":"user","content":"杭州今天的天气怎么样呢"}]},
#     stream_mode="messages"
# ):

for stream_mode, chunk in agent.stream(
        {"messages":[{"role":"user","content":"杭州今天的天气怎么样呢"}]},
    stream_mode=["update","messages","custom"]
):
    print(chunk)
    # print("Token", token)
    # print("Metadata", metadata)
    print("\n")