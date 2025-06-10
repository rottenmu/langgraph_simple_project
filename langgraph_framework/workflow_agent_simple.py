import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from matplotlib import pyplot as plt, image as mpimg
from typing_extensions import TypedDict

#create LLM
load_dotenv()

llm = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("OPEN_API_KEY")
)
#
class State(TypedDict):
    topic: str
    joke: str
    improved_joke :str
    final_joke: str

def generic_joke(state: State):
    """First LLM call to generate initial joke """
    topic = state["topic"]
    msg = llm.invoke(f"Write a short joke about {topic}")

    return {"joke": msg.content}


def check_punchline(state: State):
    """Gate function to check if the joke has a punchline"""
    if "?" in state["joke"]  or "!" in state["joke"]:
        return "Pass"

    return "Fail"

def improve_joke(state:State):
    """Second LLM call to improve the joke"""
    msg = llm.invoke(f"Make this joke funnier by adding wordplay: {state['joke']}")
    return {"improved_joke": msg.content}

def polish_joke(state:State):
    """Third LLM call for final polish"""
    msg = llm.invoke(f"Add a surprising twist to this joke: {state['improved_joke']}")
    return {"final_joke": msg.content}

workflow = StateGraph(State)
workflow.add_node("generic_joke",generic_joke)
workflow.add_node("improve_joke",improve_joke)
workflow.add_node("polish_joke",polish_joke)

#add edge
workflow.add_edge(START, "generic_joke")
edges = workflow.add_conditional_edges("generic_joke", check_punchline, {"Fail": "improve_joke", "Pass": END})

workflow.add_edge("improve_joke", "polish_joke")
workflow.add_edge("polish_joke", END)
chain = workflow.compile()

try:
     mermaid_code = chain.get_graph().draw_mermaid_png()
     with open("graph.jpg", "wb") as f:
         f.write(mermaid_code)

     img = mpimg.imread("graph.jpg")
     plt.imshow(img)
     plt.axis('off')
     plt.show()
except Exception as e:
    print(e)

state = chain.invoke({"topic": "cats"})
print("Initial joke:")
print(state["joke"])
print("\n--- --- ---\n")

if "improved_joke" in state:
    print("Improved joke:")
    print(state["improved_joke"])
    print("\n--- --- ---\n")

    print("Final joke:")
    print(state["final_joke"])
else:
    print("Joke failed quality gate - no punchline detected!")