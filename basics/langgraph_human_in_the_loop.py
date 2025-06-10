import os
from typing import Annotated

import matplotlib.pyplot as plt
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START
from langgraph.graph import add_messages, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import interrupt
from typing_extensions import TypedDict
from matplotlib import image


load_dotenv()

llm = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("OPEN_API_KEY")
)


class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

@tool("human_assistance")
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    human_response = interrupt({"query": query})
    return human_response["data"]

tool = TavilySearch(max_reults=2, tavily_api_key="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")
tools = [tool, human_assistance]
llm_with_tools = llm.bind_tools(tools=tools)

#
def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])

    assert len(message.tool_calls) <= 1
    return {"messages": message}

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
memory = MemorySaver()
graph = graph_builder.compile(checkpointer= memory )
try:
    mermaid_code = graph.get_graph().draw_mermaid_png()
    with open("graph.jpg", "wb") as f:
        f.write(mermaid_code)
    img = image.imread("graph.jpg")
    plt.imshow(img)
    plt.axis('off')
    plt.show()
except Exception as e:
    print(e)


user_input = (
    "Can you look up when LangGraph was released? "
    "When you have the answer, use the human_assistance tool for review."
)
config = {"configurable": {"thread_id": "1"}}

events = graph.stream(
    {"messages": [{"role": "user", "content": user_input}]},
    config,
    stream_mode="values",
)
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()