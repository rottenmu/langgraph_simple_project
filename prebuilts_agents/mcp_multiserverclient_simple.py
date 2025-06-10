import os

from dotenv import load_dotenv
from langchain.agents import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("OPEN_API_KEY")
)
client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            "args": ["mcp_stdio_serve_simple.py"],
            "transport": "stdio"
        },
        "weather": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http",
        }
    }
)

async def run ():
    tools = await client.get_tools()
    agent = create_react_agent(model,tools)
    agent_response= agent.invoke()