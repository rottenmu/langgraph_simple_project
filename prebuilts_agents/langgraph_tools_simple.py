import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool


load_dotenv()

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("OPEN_API_KEY")
)
# @tool(return_direct=True)
# def multiply(a: int, b: int) -> int:
#     """ 两数相乘 """
#     return  a * b

@tool(return_direct=True)
def greet(user_name: str) -> int:
    """Greet user."""
    return f"Hello {user_name}!"

tools = [greet]

agent = create_react_agent(
    model=model.bind_tools(tools=tools, tool_choice="greet"),
    tools=tools
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Hi, I am Bob"}]}
)

print(result)

# @tool
# def greet(user_name:str):
#     """greet User """
#     return f"Hello {user_name}!"
#
# tools = [greet]
# agent = create_react_agent(
#     model=model.bind_tools(tools=tools, tool_choice={"type":"tool","name":"greet"}),
#     tools=tools
# )
#
# print(agent.invoke( {"messages": [{"role": "user", "content": "Hi, I am Bob"}]}))

#print(agent.invoke({"messages":[{"role":"user","content":"what's 4 * 7 ?"}]}))