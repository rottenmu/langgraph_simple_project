import os
from typing import Annotated

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import add_messages, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict
from matplotlib import image as mpimg, pyplot as plt

memory =InMemorySaver()

tool = TavilySearch(max_reults=2, tavily_api_key="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")
tools = [tool]

load_dotenv()

load_dotenv()

llm = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("OPEN_API_KEY")
)
llm_with_tool = llm.bind_tools(tools=tools)

class State (TypedDict):
    messages:Annotated[list, add_messages]

graph_builder = StateGraph(State)

def chatbot(state:State):
    return {"messages":[llm_with_tool.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools= [tool])
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
)

graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")
graph = graph_builder.compile(checkpointer=memory)

try:
     mermaid_code = graph.get_graph().draw_mermaid_png()
     with open("graph.jpg", "wb") as f:
         f.write(mermaid_code)

     img = mpimg.imread("graph.jpg")
     plt.imshow(img)
     plt.axis('off')
     plt.show()
except Exception as e:
    print(e)
