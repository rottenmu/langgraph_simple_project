import os
from http.client import responses

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.errors import GraphRecursionError
from langgraph.prebuilt import create_react_agent


load_dotenv()

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("OPEN_API_KEY")
)

tool = TavilySearch(max_result=2 ,tavily_api_key="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")

tools = [tool]

max_iteration = 3
agent = create_react_agent(
    model= model,
    tools=tools,
)

# for chunk in agent.stream(
#     {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
#     stream_mode="updates"
# ):
#     print(chunk)

for chunk in agent.stream(
        {"messages":[{"role":"user","content":"杭州今天的天气怎么样"}]},
        stream_mode="updates"
):
    print(chunk)
recursion_limit = 2 * max_iteration + 1
try:
    responses = agent.invoke(
        {"messages":[{"role":"user","content":"请介绍 langgraph框架"}]},
        {"recursion_limit": recursion_limit}
    )

except GraphRecursionError as e:
    print("Agent stopped due to max iteration")

