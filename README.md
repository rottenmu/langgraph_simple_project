LangGraph 简单项目介绍
一、项目概述
本项目 langgraph_simple_project 主要围绕 LangGraph 构建，展示了多种基于 LangGraph 的应用场景，包括多智能体协作、内存管理、工具调用、自定义状态处理等功能。项目使用了 langchain 库，结合 qwen-plus 模型进行开发。
二、项目结构
plaintext
langgraph_simple_project/
├── basics/
│   ├── langgraph_addMemory.py
│   ├── langgraph_chatbot_simple.py
│   ├── langgraph_custome_state.simple.py
│   ├── langgraph_custom_state_2_simple.py
│   └── langgraph_human_in_the_loop.py
├── prebuilts_agents/
│   ├── evals/
│   │   └── langgraph_evals_simple.py
│   ├── memory/
│   │   ├── langgraph_memory_simple.py
│   │   ├── long-term-memory-read-simple.py
│   │   ├── long-term-memory-write-simple.py
│   │   └── memory-write-in-tools-simple.py
│   ├── multi_agent/
│   │   ├── multi_agent_handoff_simple.py
│   │   ├── multi_agent_swarm2_simple.py
│   │   ├── multi_agent_swarm_simple.py
│   │   ├── multi_agent_supervisor2_simple.py
│   │   └── multi_agent_supervisor_simple.py
│   ├── langgraph_context_using_config_simple.py
│   ├── langgraph_context_using_state_simple.py
│   ├── langgraph_first.py
│   ├── langgraph_model_simple.py
│   ├── langgraph_streaming_simple.py
│   ├── langgraph_tools_simple.py
│   ├── mcp_http_serve_simple.py
│   └── mcp_multiserverclient_simple.py
├── .env
├── .idea/
│   ├── .gitignore
│   └── misc.xml
├── langgraph.json
├── pyproject.toml
└── requirements.txt
三、环境配置
1. 依赖安装
项目的依赖管理主要通过 pyproject.toml 文件，需要使用 Poetry 进行安装：

bash
poetry install
2. 环境变量配置
在 .env 文件中配置必要的环境变量：

plaintext
OPEN_API_KEY=sk-xxx
LANGSMITH_API_KEY=lsv2_sxxx
PYTHON_VERSION=3.11
四、核心功能模块
1. 多智能体协作
多智能体切换与任务分配
文件：prebuilts_agents/multi_agent/multi_agent_handoff_simple.py、prebuilts_agents/multi_agent/multi_agent_swarm_simple.py、prebuilts_agents/multi_agent/multi_agent_supervisor_simple.py
功能：创建了航班预订和酒店预订两个智能体，通过工具实现智能体之间的切换和任务分配。例如，用户需求包含航班和酒店预订时，智能体可以协作完成任务。
代码示例
python
运行
# multi_agent_handoff_simple.py
transfer_to_hotel_assistant = create_handoff_tool(
    agent_name="hotel_assistant",
    description="Transfer user to the hotel-booking assistant."
)

flight_assistant = create_react_agent(
    model=model,
    tools=[book_flight, transfer_to_hotel_assistant],
    prompt="You are a flight booking assistant",
    name="flight_assistant"
)
2. 内存管理
长期内存读写
文件：prebuilts_agents/memory/long-term-memory-read-simple.py、prebuilts_agents/memory/long-term-memory-write-simple.py
功能：使用 InMemoryStore 实现长期内存的读写操作，例如保存和查询用户信息。
代码示例
python
运行
# long-term-memory-write-simple.py
@tool
def save_user_info (
        user_info: UserInfo,
        config:RunnableConfig
) -> str:
    """save user info """
    store = get_store()
    user_id = config["configurable"].get("user_id")
    store.put(("users",), user_id, user_info)
    return "Successfully saved user info"
3. 工具调用
自定义工具
文件：prebuilts_agents/langgraph_tools_simple.py
功能：定义了自定义工具，如 greet 工具，用于向用户打招呼。
代码示例
python
运行
# langgraph_tools_simple.py
@tool(return_direct=True)
def greet(user_name: str) -> int:
    """Greet user."""
    return f"Hello {user_name}!"
4. 自定义状态处理
自定义状态类
文件：basics/langgraph_custome_state.simple.py、basics/langgraph_custom_state_2_simple.py
功能：定义了自定义状态类，包含用户的姓名和生日等信息，并通过工具进行状态更新和验证。
代码示例
python
运行
# langgraph_custome_state.simple.py
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
    # ...
五、运行示例
1. 多智能体协作示例
bash
python prebuilts_agents/multi_agent/multi_agent_handoff_simple.py
2. 内存读写示例
bash
python prebuilts_agents/memory/long-term-memory-read-simple.py

3. 工具调用示例
bash
python prebuilts_agents/langgraph_tools_simple.py
