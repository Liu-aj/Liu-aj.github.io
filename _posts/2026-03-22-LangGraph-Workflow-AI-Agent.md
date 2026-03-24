---
title: "LangGraph 工作流编排实战：用有向图构建可控的 AI Agent"
date: 2026-03-22 18:00:00 +0800
category: AI
tags: [LangGraph, Agent, Workflow, Python, LLM]
---

## 引言：从"自由推理"到"可控流程"

在 AI Agent 开发中，我们常遇到一个棘手问题：**Agent 能力很强，但行为不可控**。

```python
# 传统的 ReAct Agent
agent = create_react_agent(llm, tools)
response = agent.invoke({"input": "帮我订一张去上海的机票"})

# 问题来了：
# 1. 它可能会先查天气
# 2. 可能会搜索航班
# 3. 可能会直接"假装"订票
# 4. 甚至可能问一些无关的问题
```

这种"自由推理"模式在复杂业务场景中存在明显短板：

| 问题 | 影响 |
|------|------|
| **流程不可控** | 无法保证执行顺序，可能跳过关键步骤 |
| **难以调试** | 每次执行路径可能不同，问题难以复现 |
| **缺乏人工介入点** | 无法在关键决策点暂停等待审批 |
| **并发能力弱** | 难以编排并行任务 |

**LangGraph** 应运而生——它用**有向图（Directed Graph）**的方式，让 Agent 的行为变得可控、可预测、可调试。

---

## 一、StateGraph 核心概念

LangGraph 的核心是 `StateGraph`，它将 Agent 抽象为**状态机 + 有向图**。

### 1.1 三个核心要素

```
┌─────────────────────────────────────────────────────┐
│                    StateGraph                        │
│                                                      │
│   State (状态) ──► Nodes (节点) ──► Edges (边)       │
│                                                      │
│   • State: 跨节点共享的数据容器                       │
│   • Nodes: 执行具体逻辑的函数                         │
│   • Edges: 定义节点间的流转规则                       │
└─────────────────────────────────────────────────────┘
```

### 1.2 一个最简示例

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END

# 1. 定义状态
class AgentState(TypedDict):
    messages: list
    next_action: str

# 2. 定义节点
def think(state: AgentState) -> AgentState:
    """思考节点：分析用户意图"""
    # ... 调用 LLM 进行推理
    return {"next_action": "search"}

def search(state: AgentState) -> AgentState:
    """搜索节点：执行查询"""
    # ... 调用搜索工具
    return {"messages": ["找到 3 个结果"]}

def respond(state: AgentState) -> AgentState:
    """响应节点：生成最终回复"""
    # ... 整理结果返回用户
    return {"messages": ["为您找到了以下结果..."]}

# 3. 构建图
workflow = StateGraph(AgentState)

# 添加节点
workflow.add_node("think", think)
workflow.add_node("search", search)
workflow.add_node("respond", respond)

# 设置入口
workflow.set_entry_point("think")

# 添加边（流转规则）
workflow.add_edge("think", "search")
workflow.add_edge("search", "respond")
workflow.add_edge("respond", END)

# 4. 编译并执行
app = workflow.compile()
result = app.invoke({"messages": [], "next_action": ""})
```

### 1.3 条件分支：让流程更智能

真实场景中，流程往往不是线性的：

```python
def route_after_think(state: AgentState) -> str:
    """根据思考结果决定下一步"""
    if state["next_action"] == "search":
        return "search"
    elif state["next_action"] == "calculate":
        return "calculate"
    else:
        return "respond"

# 添加条件边
workflow.add_conditional_edges(
    "think",
    route_after_think,
    {
        "search": "search",
        "calculate": "calculate",
        "respond": "respond"
    }
)
```

---

## 二、实战：ReAct Agent

ReAct（Reasoning + Acting）是最经典的 Agent 模式。让我们用 LangGraph 重新实现。

### 2.1 架构设计

```
用户输入
    │
    ▼
┌─────────┐
│  THINK   │ ◄───┐
└────┬────┘      │
     │           │
     ▼           │
┌─────────┐      │
│  ACT    │ ─────┘ (循环)
└────┬────┘
     │ (无工具调用)
     ▼
┌─────────┐
│ RESPOND │
└─────────┘
```

### 2.2 完整实现

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
import operator

# 1. 定义工具
@tool
def search_web(query: str) -> str:
    """搜索网络信息"""
    # 实际实现调用搜索 API
    return f"搜索结果：{query} 相关信息..."

@tool
def calculate(expression: str) -> str:
    """执行数学计算"""
    try:
        result = eval(expression)
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算错误：{e}"

# 2. 定义状态
class ReActState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    should_continue: bool

# 3. 定义节点
def think_node(state: ReActState) -> ReActState:
    """思考节点：决定下一步行动"""
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    llm_with_tools = llm.bind_tools([search_web, calculate])
    
    response = llm_with_tools.invoke(state["messages"])
    
    # 判断是否需要继续
    should_continue = len(response.tool_calls) > 0
    
    return {
        "messages": [response],
        "should_continue": should_continue
    }

def respond_node(state: ReActState) -> ReActState:
    """响应节点：生成最终答案"""
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and not last_message.tool_calls:
        # 已经是最终回复
        return state
    
    # 否则调用 LLM 生成总结
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 4. 构建图
workflow = StateGraph(ReActState)

workflow.add_node("think", think_node)
workflow.add_node("act", ToolNode([search_web, calculate]))
workflow.add_node("respond", respond_node)

workflow.set_entry_point("think")

# 条件边：思考后决定是执行工具还是直接回复
def should_continue(state: ReActState) -> str:
    if state["should_continue"]:
        return "act"
    return "respond"

workflow.add_conditional_edges(
    "think",
    should_continue,
    {"act": "act", "respond": "respond"}
)

# 执行工具后返回思考
workflow.add_edge("act", "think")
workflow.add_edge("respond", END)

# 5. 编译执行
app = workflow.compile()

# 测试
result = app.invoke({
    "messages": [HumanMessage(content="帮我查一下北京的天气，然后计算 25 + 17")],
    "should_continue": False
})

print(result["messages"][-1].content)
```

### 2.3 可视化

```python
from IPython.display import Image, display

# 生成流程图
display(Image(app.get_graph().draw_mermaid_png()))
```

---

## 三、实战：多步审批工作流

企业场景中，关键操作往往需要人工审批。LangGraph 的 `interrupt()` 机制完美解决这个问题。

### 3.1 场景描述

```
用户请求订票
    │
    ▼
┌─────────┐
│ 检查库存 │
└────┬────┘
     │
     ▼
┌─────────┐
│ 价格评估 │
└────┬────┘
     │
     ▼
┌─────────┐     超过预算
│ 预算检查 │ ──────────────►
└────┬────┘                │
     │ (预算内)            │
     ▼                     ▼
┌─────────┐         ┌──────────┐
│ 人工审批 │ ◄──────│ 等待调整 │
└────┬────┘         └──────────┘
     │ (批准)
     ▼
┌─────────┐
│ 执行订票 │
└─────────┘
```

### 3.2 完整实现

```python
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command

# 1. 定义状态
class ApprovalState(TypedDict):
    request: dict
    inventory_check: dict
    price_estimate: dict
    budget_status: str
    approval_status: str
    result: str

# 2. 定义节点
def check_inventory(state: ApprovalState) -> ApprovalState:
    """检查库存"""
    # 模拟库存查询
    request = state["request"]
    inventory = {
        "available": True,
        "seats_left": 15,
        "flight": request.get("flight", "MU1234")
    }
    return {"inventory_check": inventory}

def estimate_price(state: ApprovalState) -> ApprovalState:
    """价格评估"""
    inventory = state["inventory_check"]
    price = {
        "amount": 2500,
        "currency": "CNY",
        "includes_tax": True
    }
    return {"price_estimate": price}

def check_budget(state: ApprovalState) -> Command[Literal["auto_approve", "manual_approval"]]:
    """预算检查"""
    price = state["price_estimate"]["amount"]
    budget_limit = state["request"].get("budget_limit", 2000)
    
    if price <= budget_limit:
        return Command(
            goto="execute_booking",
            update={"budget_status": "within_budget", "approval_status": "auto_approved"}
        )
    else:
        return Command(
            goto="request_approval",
            update={"budget_status": "over_budget"}
        )

def request_approval(state: ApprovalState) -> ApprovalState:
    """请求人工审批"""
    # 关键：使用 interrupt 暂停执行
    user_decision = interrupt({
        "question": f"机票价格 {state['price_estimate']['amount']} 元，超预算，是否批准？",
        "options": ["approve", "reject", "modify"],
        "context": state
    })
    
    # 恢复执行时，user_decision 会包含用户的决定
    if user_decision == "approve":
        return {"approval_status": "approved"}
    elif user_decision == "reject":
        return {"approval_status": "rejected"}
    else:
        return {"approval_status": "pending_modification"}

def execute_booking(state: ApprovalState) -> ApprovalState:
    """执行订票"""
    if state.get("approval_status") == "rejected":
        return {"result": "订票被拒绝"}
    
    # 执行实际订票逻辑
    return {"result": f"成功预订航班 {state['inventory_check']['flight']}"}

# 3. 构建图
workflow = StateGraph(ApprovalState)

workflow.add_node("check_inventory", check_inventory)
workflow.add_node("estimate_price", estimate_price)
workflow.add_node("check_budget", check_budget)
workflow.add_node("request_approval", request_approval)
workflow.add_node("execute_booking", execute_booking)

workflow.set_entry_point("check_inventory")

workflow.add_edge("check_inventory", "estimate_price")
workflow.add_edge("estimate_price", "check_budget")

# 条件路由：check_budget 直接决定下一步
workflow.add_conditional_edges("check_budget", lambda s: s.get("next_node", "execute_booking"))

workflow.add_edge("request_approval", "execute_booking")
workflow.add_edge("execute_booking", END)

# 4. 编译（需要 checkpointer 支持 interrupt）
checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)

# 5. 执行（第一阶段：到 interrupt 点暂停）
config = {"configurable": {"thread_id": "booking-001"}}
state1 = app.invoke(
    {"request": {"flight": "MU1234", "date": "2026-04-01", "budget_limit": 2000}},
    config
)

# 6. 人工审批后恢复执行
state2 = app.invoke(
    Command(resume="approve"),  # 用户批准
    config
)

print(state2["result"])  # 输出：成功预订航班 MU1234
```

### 3.3 关键点解析

| 特性 | 说明 |
|------|------|
| `interrupt()` | 暂停执行，等待外部输入 |
| `Command(resume=...)` | 恢复执行，传入用户决策 |
| `checkpointer` | 持久化状态，支持断点续传 |
| `thread_id` | 区分不同的执行实例 |

---

## 四、实战：并行子任务编排

复杂任务往往可以拆解为多个并行子任务，LangGraph 通过**分叉-合并**模式支持。

### 4.1 架构设计

```
                用户请求
                    │
                    ▼
              ┌─────────┐
              │  分析   │
              └────┬────┘
                   │
         ┌─────────┼─────────┐
         │         │         │
         ▼         ▼         ▼
    ┌────────┐ ┌────────┐ ┌────────┐
    │ 搜索   │ │ 计算   │ │ 翻译   │
    └────┬───┘ └────┬───┘ └────┬───┘
         │         │         │
         └─────────┼─────────┘
                   │
                   ▼
              ┌─────────┐
              │  合并   │
              └────┬────┘
                   │
                   ▼
              ┌─────────┐
              │  总结   │
              └─────────┘
```

### 4.2 完整实现

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
import asyncio

# 1. 定义状态
class ParallelState(TypedDict):
    query: str
    search_result: str
    calculate_result: str
    translate_result: str
    final_summary: str

# 2. 定义节点
async def analyze_query(state: ParallelState) -> ParallelState:
    """分析查询，确定需要执行的任务"""
    return state  # 实际可做意图识别

async def search_task(state: ParallelState) -> ParallelState:
    """搜索任务（模拟）"""
    await asyncio.sleep(1)  # 模拟耗时操作
    return {"search_result": f"搜索 '{state['query']}' 的结果"}

async def calculate_task(state: ParallelState) -> ParallelState:
    """计算任务（模拟）"""
    await asyncio.sleep(0.5)
    return {"calculate_result": "计算结果: 42"}

async def translate_task(state: ParallelState) -> ParallelState:
    """翻译任务（模拟）"""
    await asyncio.sleep(0.8)
    return {"translate_result": f"Translation of '{state['query']}'"}

async def merge_results(state: ParallelState) -> ParallelState:
    """合并并行结果"""
    return state

async def summarize(state: ParallelState) -> ParallelState:
    """生成最终总结"""
    summary = f"""
    搜索结果：{state.get('search_result', '无')}
    计算结果：{state.get('calculate_result', '无')}
    翻译结果：{state.get('translate_result', '无')}
    """
    return {"final_summary": summary.strip()}

# 3. 构建图
workflow = StateGraph(ParallelState)

workflow.add_node("analyze", analyze_query)
workflow.add_node("search", search_task)
workflow.add_node("calculate", calculate_task)
workflow.add_node("translate", translate_task)
workflow.add_node("merge", merge_results)
workflow.add_node("summarize", summarize)

workflow.set_entry_point("analyze")

# 分叉：从 analyze 分出三个并行任务
workflow.add_edge("analyze", "search")
workflow.add_edge("analyze", "calculate")
workflow.add_edge("analyze", "translate")

# 合并：三个任务都完成后进入 merge
workflow.add_edge("search", "merge")
workflow.add_edge("calculate", "merge")
workflow.add_edge("translate", "merge")

workflow.add_edge("merge", "summarize")
workflow.add_edge("summarize", END)

# 4. 编译执行
app = workflow.compile()

# 异步执行
async def main():
    result = await app.ainvoke({"query": "AI 技术趋势"})
    print(result["final_summary"])

asyncio.run(main())
```

### 4.3 性能对比

| 模式 | 执行时间 | 说明 |
|------|---------|------|
| 串行执行 | 2.3 秒 | 三个任务依次执行 |
| 并行执行 | 1.0 秒 | 自动识别最长路径 |

---

## 五、生产部署

将 LangGraph 应用部署到生产环境，需要考虑持久化、监控、扩展性。

### 5.1 持久化：PostgreSQL Checkpointer

```python
from langgraph.checkpoint.postgres import PostgresSaver

# 使用 PostgreSQL 存储状态
checkpointer = PostgresSaver(
    connection_string="postgresql://user:pass@localhost/langgraph"
)

app = workflow.compile(checkpointer=checkpointer)

# 每个会话使用唯一 thread_id
config = {"configurable": {"thread_id": "user-session-12345"}}
result = app.invoke(input_state, config)

# 恢复中断的会话
history = app.get_state(config)
print(history.values)  # 查看当前状态
```

### 5.2 监控：集成 LangSmith

```python
import os

os.environ["LANGSMITH_API_KEY"] = "your-api-key"
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "production-agent"

# 自动追踪每次执行
result = app.invoke({"input": "..."})

# 在 LangSmith 中查看：
# - 执行路径
# - 每个节点的输入输出
# - LLM 调用详情
# - 耗时分析
```

### 5.3 API 服务化

```python
from fastapi import FastAPI
from pydantic import BaseModel

app_fastapi = FastAPI()

class ChatRequest(BaseModel):
    message: str
    thread_id: str

@app_fastapi.post("/chat")
async def chat(request: ChatRequest):
    config = {"configurable": {"thread_id": request.thread_id}}
    
    result = app.invoke(
        {"messages": [HumanMessage(content=request.message)]},
        config
    )
    
    return {"response": result["messages"][-1].content}

# 部署：uvicorn main:app --host 0.0.0.0 --port 8000
```

### 5.4 断点续传示例

```python
# 场景：审批流程中途暂停，用户稍后继续

# 第一天：启动流程
app.invoke({"request": {...}}, {"thread_id": "approval-001"})
# 在 request_approval 节点暂停

# 第二天：查看状态
state = app.get_state({"thread_id": "approval-001"})
print(state.next)  # 输出：['request_approval']

# 用户批准后继续
app.invoke(
    Command(resume="approve"),
    {"thread_id": "approval-001"}
)
```

---

## 六、最佳实践与避坑指南

### 6.1 状态设计原则

```python
# ❌ 错误：状态过于复杂
class BadState(TypedDict):
    entire_conversation_history: list[dict]  # 太大
    ui_state: dict  # 不应该放在 Agent 状态
    cache: dict  # 用 checkpointer 而非状态

# ✅ 正确：精简状态
class GoodState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    current_step: str
    user_preferences: dict
```

### 6.2 循环检测

```python
# 设置最大迭代次数，防止死循环
MAX_ITERATIONS = 10

def check_loop(state: LoopState) -> str:
    iteration = state.get("iteration", 0) + 1
    
    if iteration >= MAX_ITERATIONS:
        return "max_iterations_reached"
    
    return state["next_action"]

workflow.add_conditional_edges(
    "think",
    check_loop,
    {
        "act": "act",
        "respond": "respond",
        "max_iterations_reached": "emergency_stop"
    }
)
```

### 6.3 错误处理

```python
def safe_node(state: State) -> State:
    try:
        # 执行可能失败的操作
        result = risky_operation(state)
        return {"result": result, "error": None}
    except Exception as e:
        # 记录错误，不中断流程
        return {"result": None, "error": str(e)}

# 后续节点可以根据 error 字段决定行为
def handle_result(state: State) -> State:
    if state.get("error"):
        # 降级处理
        return fallback_response(state)
    return normal_response(state)
```

---

## 总结

LangGraph 通过**状态图**的方式，解决了 Agent 开发中的核心痛点：

| 问题 | LangGraph 方案 |
|------|----------------|
| 流程不可控 | 显式定义节点和边 |
| 难以调试 | 可视化 + LangSmith 追踪 |
| 缺乏人工介入 | `interrupt()` 暂停机制 |
| 并发能力弱 | 原生支持并行分支 |

**适用场景**：
- 需要严格审批流程的业务（金融、医疗）
- 多步骤可编排的任务（数据分析流水线）
- 需要人工介入的半自动化流程

**不适用场景**：
- 简单的单轮问答
- 无需控制流程的创意写作
- 完全确定性的脚本任务

LangGraph 不是银弹，但在需要**可控、可预测、可调试**的 Agent 场景中，它是目前最优解之一。

---

## 参考资料

- [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
- [LangSmith 监控平台](https://www.langchain.com/langsmith)
- [LangGraph Examples](https://github.com/langchain-ai/langgraph/tree/main/examples)

---

> 💡 **作者注**：本文基于 LangGraph 2026 版本编写，主要特性包括 Command API、interrupt() 等。生产环境建议配合 LangSmith 使用，获得完整的可观测性。

*本文首发于 [L先生的博客](https://liu-aj.github.io)，转载请注明出处。*