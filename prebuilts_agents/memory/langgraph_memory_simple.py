import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage
from langchain_core.messages.utils import count_tokens_approximately, trim_messages
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from typing import Any

load_dotenv()

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("OPEN_API_KEY")
)
memory = InMemorySaver()
# summarization_node = SummarizationNode(
#     token_counter=count_tokens_approximately,
#     model=model,
#     max_tokens=384,
#     max_summary_tokens=128,
#     output_messages_key="llm_input_messages",
# )

class State(AgentState):
    context: dict[str, Any]


def pre_model_hook(state):
    trimmed_message = trim_messages(
        state["messages"],
        strategy="last",
        max_tokens=384,
        token_counter=count_tokens_approximately,
        start_on= "human",
        end_on = ("human","tools")
    )
    return {"llm_input_messages": trimmed_message}

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}"


config = {"configurable": {"thread_id": "abc123"}}

agent = create_react_agent(
    model=model,
    pre_model_hook=pre_model_hook,
    checkpointer=memory,
    tools=[get_weather],
    state_schema=State,
)
Hangzhou_response = agent.invoke(
    {"messages": [{"role": "user", "content": "What is the weather in Hangzhou"}]},
    config=config
)
for msg in Hangzhou_response["messages"]:
    if isinstance(msg, AIMessage):
        print(msg.content)
