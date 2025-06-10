import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from mcp import StdioServerParameters, stdio_client, ClientSession
from mcp.client.streamable_http import streamablehttp_client

server_parameter = StdioServerParameters(
    command="python",
    args=["mcp_stdio_serve_simple.py"]
)

load_dotenv()

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("OPEN_API_KEY")
)


# async def runStdio_client():
#     async with stdio_client(server_parameter) as (read, write):
#         async with ClientSession(read, write) as session:
#             # initialize the connection
#             await session.initialize()
#             tools = await load_mcp_tools(session)
#             agent = create_react_agent(model, tools)
#             agent_response = agent.invoke({"messages": "what's (3 + 5) x 12?"})
#             print(agent_response)

async def call_streamable_http():
    async with streamablehttp_client("http://127.0.0.1:8000/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:
            # initialize the connection
            await session.initialize()
            tools = await  load_mcp_tools(session)
            agent = create_react_agent(model=model, tools=tools)
            agent_response = agent.invoke({"messages":"杭州的天气怎么样"})
            print(agent_response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(call_streamable_http())