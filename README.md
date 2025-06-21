# LangGraph 简单项目文档

## 项目概述
`langgraph_simple_project` 是一个基于 LangGraph 框架构建的演示项目，展示了多智能体协作、内存管理、工具调用和自定义状态处理等核心功能。项目结合了 `langchain` 库和 `qwen-plus` 模型进行开发。

## 项目结构
 ```
langgraph_simple_project/
├── basics/
│ ├── langgraph_addMemory.py
│ ├── langgraph_chatbot_simple.py
│ ├── langgraph_custome_state.simple.py
│ ├── langgraph_custom_state_2_simple.py
│ └── langgraph_human_in_the_loop.py
├── prebuilts_agents/
│ ├── evals/
│ │ └── langgraph_evals_simple.py
│ ├── memory/
│ │ ├── langgraph_memory_simple.py
│ │ ├── long-term-memory-read-simple.py
│ │ ├── long-term-memory-write-simple.py
│ │ └── memory-write-in-tools-simple.py
│ └── multi_agent/
│ ├── multi_agent_handoff_simple.py
│ ├── multi_agent_swarm2_simple.py
│ ├── multi_agent_swarm_simple.py
│ ├── multi_agent_supervisor2_simple.py
│ └── multi_agent_supervisor_simple.py
├── .env
├── .idea/
│ └── misc.xml
├── .gitignore
├── langgraph.json
├── pyproject.toml
└── requirements.txt
 ```

## 环境配置

### 依赖安装
使用 Poetry 进行依赖管理：
```bash
poetry install
环境变量配置
.env 文件配置：

plaintext
复制
OPEN_API_KEY=sk-xxx
LANGSMITH_API_KEY=lsv2_sxxx
PYTHON_VERSION=3.11
核心功能模块
1. 多智能体协作
​文件位置:
 ```
prebuilts_agents/multi_agent/multi_agent_handoff_simple.py
prebuilts_agents/multi_agent/multi_agent_swarm_simple.py
prebuilts_agents/multi_agent/multi_agent_supervisor_simple.py
 ```
​功能描述:

创建航班预订和酒店预订智能体
实现智能体间的任务切换和协作
处理包含多个子任务的用户请求
​代码示例:

 ```python
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
 ```
2. 内存管理
​文件位置:

prebuilts_agents/memory/long-term-memory-read-simple.py
prebuilts_agents/memory/long-term-memory-write-simple.py
​功能描述:

使用 InMemoryStore 实现长期内存读写
存储和查询用户信息
​代码示例:

python
 ```
@tool
def save_user_info(user_info: UserInfo, config:RunnableConfig) -> str:
    """save user info """
    store = get_store()
    user_id = config["configurable"].get("user_id")
    store.put(("users",), user_id, user_info)
    return "Successfully saved user info"
 ```    
3. 工具调用
​文件位置:
 ```
prebuilts_agents/langgraph_tools_simple.py
 ```
​功能描述:

定义自定义工具（如问候工具）
直接返回工具调用结果
​代码示例:

python
 ```
@tool(return_direct=True)
def greet(user_name: str) -> int:
    """Greet user."""
    return f"Hello {user_name}!"
 ```
4. 自定义状态处理
​文件位置:
 ```
basics/langgraph_custome_state.simple.py
basics/langgraph_custom_state_2_simple.py
 ```
​功能描述:

定义包含用户信息的自定义状态类
实现状态更新和验证机制
​代码示例:

python
 ```
class State(TypedDict):
    messages: Annotated[list, add_messages]
    name: str
    birthday: str

@tool
def human_assistance(
    name: str, 
    birthday: str, 
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> str:
    """Request assistance from a human."""
    human_response = interrupt({
        "question": "Is this correct?",
        "name": name,
        "birthday": birthday,
    })
 ```
运行示例
多智能体协作
 ```
python prebuilts_agents/multi_agent/multi_agent_handoff_simple.py
 ```
内存读写

 ```
python prebuilts_agents/memory/long-term-memory-read-simple.py
 ```
工具调用
 ```
python prebuilts_agents/langgraph_tools_simple.py
 ```

技术栈
 ```
LangGraph 框架
LangChain 库
Qwen-plus 模型
Poetry 依赖管理
Python 3.11
 ```
