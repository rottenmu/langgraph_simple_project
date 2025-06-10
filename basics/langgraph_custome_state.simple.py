import os
from typing import Annotated

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool, InjectedToolCallId, Tool
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START
from langgraph.graph import add_messages, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import interrupt, Command
from typing_extensions import TypedDict

load_dotenv()

llm = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("OPEN_API_KEY")
)

class State(TypedDict):
    messages:Annotated[list, add_messages]
    name: str
    birthday: str

@tool
def human_assistance(
    name: str, birthday: str, tool_call_id: Annotated[str, InjectedToolCallId]
) -> str:
    """Request assistance from a human."""
    human_response = interrupt(
        {
            "question": "Is this correct?",
            "name": name,
            "birthday": birthday,
        },
    )
    if human_response.get("correct", "").lower().startswith("y"):
        verified_name = name
        verified_birthday = birthday
        response = "Correct"
    else:
        verified_name = human_response.get("name",name)
        verified_birthday = human_response.get("birthday",birthday)
        response = f"Mode a correction:{human_response}"

    state_update= {
        "name":verified_name,
        "birthday":verified_birthday,
        "messages":[ToolMessage(response,tool_call_id=tool_call_id)],
    }
    return Command(update=state_update)

tool = TavilySearch(max_reults=2, tavily_api_key="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")
tools = [tool, human_assistance]
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])

    assert len(message.tool_calls) <= 1
    return {"messages": message}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
memory = MemorySaver()
graph = graph_builder.compile(checkpointer= memory )

# user_input = (
#     "你能查一下LangGraph发布的时间吗?",
#     "当您得到答案时，使用human_assistance工具进行检查."
# )

user_input = (
    "Can you look up when LangGraph was released? "
    "When you have the answer, use the human_assistance tool for review."
)

human_command = Command(
    resume={"name":"LangGraph","birthday":"Jan 17, 2024"}
)

events = graph.stream(
    {"messages":[{"role":"user", "content": user_input}]},
    config={"configurable":{"thread_id":"abc123"}},
    stream_mode="values"
)

for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()

human_command = Command(
    resume={
        "name": "LangGraph",
        "birthday": "Jan 17, 2024",
    },
)
config={"configurable":{"thread_id":"abc123"}}
events = graph.stream(human_command, config, stream_mode="values")
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()

