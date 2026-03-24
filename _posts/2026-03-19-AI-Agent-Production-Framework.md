---
layout: post
title: "AI智能体生产落地：评估框架与架构模式深度解析"
date: 2026-03-19
category: AI
tags: [Agent, Production, Architecture, Evaluation]
---

# AI 智能体生产落地：评估框架与架构模式深度解析

> 从原型到生产，AI Agent 面临哪些挑战？本文深入剖析评估框架、架构模式与工程实践，助你构建可靠的智能体系统。

---

## 一、为什么 AI 智能体在生产环境容易"失效"

### 1.1 原型与生产的鸿沟

在实验室环境中表现出色的 AI 智能体，一旦部署到生产环境，往往会遭遇"水土不服"。这种差距主要来自三个层面：

**环境复杂度的跃升** 🌍  
开发环境通常输入干净、结构化，而生产环境充斥着噪声、边缘案例和不可预期的用户行为。一个在测试集上达到 95% 准确率的智能体，面对真实用户的"创意性"输入时，表现可能骤降至 60%。

**状态管理的挑战** 🔄  
原型系统往往忽略会话持久化、上下文窗口限制、并发处理等问题。当多个用户同时与智能体交互，或需要跨会话保持记忆时，架构缺陷便会暴露。

**成本与延迟的现实约束** 💰  
原型阶段可以使用最强大的模型（如 GPT-4），但生产环境需要在效果、成本、延迟之间寻求平衡。一个调用 10 次 GPT-4 的复杂任务，可能需要改造成 1 次调用 + 本地小模型验证的组合方案。

### 1.2 非确定性行为的困局

AI 智能体的核心——大语言模型（LLM）——本质上是一个概率系统：

```python
# 同样的输入，可能产生不同的输出
response = llm.generate("分析这段代码的风险")
# 第一次运行：可能输出"内存泄漏风险"
# 第二次运行：可能输出"线程安全问题"
# 第三次运行：可能完全偏离主题
```

这种非确定性带来三个工程挑战：

| 挑战 | 描述 |
|------|------|
| **难以复现 Bug** | 用户报告的问题，开发者本地无法复现 |
| **测试无法穷尽** | 传统的单元测试思维不再适用 |
| **行为漂移** | 模型版本更新后，智能体行为悄然改变 |

### 1.3 传统测试方法的局限性

传统软件测试基于"给定输入，期望输出"的确定性模式，但 AI 智能体测试面临独特挑战：

| 传统测试 | AI 智能体测试 |
|---------|-------------|
| 输入-输出映射确定 | 输出存在概率分布 |
| 断言精确匹配 | 需要语义级别评估 |
| 测试覆盖可量化 | 行为空间难以枚举 |
| 回归测试直接复用 | 模型版本更新后测试可能失效 |

**示例对比**：

```python
# 传统测试：精确断言
def test_calculator():
    assert add(2, 3) == 5  # 永远正确或永远错误

# 智能体测试：需要语义评估
def test_agent_response():
    response = agent.query("帮我写一个排序函数")
    # 输出可能是 Python、Java 或伪代码
    # 可能用冒泡排序、快排、甚至只是给出建议
    assert is_valid_code_response(response)  # 需要智能评估
    assert implements_sorting_algorithm(response)  # 语义理解
```

---

## 二、AI 智能体评估五大支柱

构建可靠的评估框架，需要从五个维度进行系统性考量。

### 2.1 智能与准确性 🧠

这是最直观的维度，但需要细化为多个层次：

- **任务完成率**：智能体是否成功完成了用户的意图？
- **推理质量**：在复杂多步任务中，每一步的决策是否合理？
- **知识准确性**：生成的信息是否正确？是否存在幻觉？

```python
def evaluate_intelligence(agent, test_cases):
    """智能与准确性评估示例"""
    results = {
        'task_completion': [],
        'reasoning_quality': [],
        'accuracy': []
    }
    
    for case in test_cases:
        response = agent.execute(case.input)
        
        # 任务完成率评估
        results['task_completion'].append(case.validator(response))
        
        # 推理质量评估（需要追踪中间步骤）
        if hasattr(agent, 'trace'):
            reasoning_score = evaluate_reasoning_chain(
                agent.trace.reasoning_steps,
                case.expected_reasoning
            )
            results['reasoning_quality'].append(reasoning_score)
        
        # 准确性评估（使用 LLM-as-Judge）
        accuracy_score = llm_judge.evaluate(
            f"评估以下回答的准确性：\n问题：{case.input}\n回答：{response}\n参考答案：{case.reference}"
        )
        results['accuracy'].append(accuracy_score)
    
    return aggregate_metrics(results)
```

### 2.2 性能与效率 ⚡

性能评估不仅是延迟问题，更关乎资源利用效率：

- **响应延迟**：首 Token 时间（TTFT）和总响应时间
- **Token 消耗**：输入/输出 Token 数量
- **工具调用效率**：单次任务平均工具调用次数
- **并发能力**：系统吞吐量

```python
class PerformanceMonitor:
    """性能监控装饰器"""
    def __init__(self):
        self.metrics = defaultdict(list)
    
    def track(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            token_counter = TokenCounter()
            
            result = await func(*args, **kwargs)
            
            self.metrics['latency'].append(time.time() - start_time)
            self.metrics['tokens_input'].append(token_counter.input_tokens)
            self.metrics['tokens_output'].append(token_counter.output_tokens)
            
            return result
        return wrapper
    
    def report(self):
        return {
            'p50_latency': np.percentile(self.metrics['latency'], 50),
            'p99_latency': np.percentile(self.metrics['latency'], 99),
            'avg_tokens_per_request': np.mean(self.metrics['tokens_input']) + 
                                       np.mean(self.metrics['tokens_output']),
        }
```

### 2.3 可靠性 🛡️

可靠性是生产环境的核心要求：

- **错误处理能力**：遇到异常输入时能否优雅降级？
- **重试成功率**：失败后自动重试的成功率
- **自我纠错能力**：能否识别并修正自己的错误？

```python
class ReliabilityEvaluator:
    """可靠性评估器"""
    
    def inject_failures(self, agent, scenarios):
        """注入故障场景评估恢复能力"""
        results = []
        
        for scenario in scenarios:
            # 场景1：工具不可用
            with mock.patch('tools.search', side_effect=TimeoutError):
                response = agent.execute(scenario.input)
                results.append({
                    'scenario': 'tool_timeout',
                    'handled_gracefully': not response.has_error,
                    'fallback_used': response.used_fallback
                })
            
            # 场景2：返回格式错误
            with mock.patch('llm.generate', return_value="无效JSON"):
                response = agent.execute(scenario.input)
                results.append({
                    'scenario': 'invalid_format',
                    'self_corrected': response.corrected_format,
                    'retry_count': response.retry_count
                })
        
        return results
```

### 2.4 责任与安全 🔐

AI 安全不是可选项，而是必选项：

- **内容安全**：是否生成有害内容？
- **隐私保护**：是否泄露敏感信息？
- **权限控制**：是否执行了越权操作？

```python
class SafetyGuard:
    """安全防护层"""
    
    def __init__(self):
        self.pii_detector = PIIDetector()
        self.content_filter = ContentFilter()
    
    def check_input(self, user_input):
        """输入安全检查"""
        # PII 检测
        pii_result = self.pii_detector.detect(user_input)
        if pii_result.has_pii:
            return SafetyCheckResult(
                safe=False,
                reason="检测到敏感信息",
                action="redact"
            )
        
        # 注入攻击检测
        if self._detect_prompt_injection(user_input):
            return SafetyCheckResult(
                safe=False,
                reason="疑似提示注入",
                action="reject"
            )
        
        return SafetyCheckResult(safe=True)
    
    def check_output(self, output):
        """输出安全检查"""
        safety_score = self.content_filter.analyze(output)
        if safety_score < 0.7:
            return SafetyCheckResult(
                safe=False,
                reason="输出内容存在风险",
                action="rewrite"
            )
        
        return SafetyCheckResult(safe=True)
```

### 2.5 用户体验 😊

用户体验是最终的成功标准：

- **响应可理解性**：用户能否理解智能体的输出？
- **交互流畅度**：对话是否自然、高效？
- **信任度**：用户是否愿意依赖智能体的建议？

```python
class UXEvaluator:
    """用户体验评估"""
    
    def evaluate_conversation(self, conversation_logs):
        metrics = {
            'turn_around_time': [],
            'clarification_rate': 0,
            'user_satisfaction': []
        }
        
        for log in conversation_logs:
            # 响应时间
            metrics['turn_around_time'].append(log.response_time_ms)
            
            # 智能体主动澄清问题的比例
            if log.agent_clarified:
                metrics['clarification_rate'] += 1
            
            # 用户满意度（如果有反馈）
            if log.user_feedback:
                metrics['user_satisfaction'].append(log.user_feedback)
        
        return {
            'avg_response_time': np.mean(metrics['turn_around_time']),
            'clarification_rate': metrics['clarification_rate'] / len(conversation_logs),
            'satisfaction_score': np.mean(metrics['user_satisfaction'])
        }
```

---

## 三、核心架构模式详解

### 3.1 ReAct 模式：推理与行动的交响 🎼

ReAct（Reasoning + Acting）是目前最主流的智能体架构模式，其核心是交替进行思考和行动：

```python
class ReActAgent:
    """ReAct 架构实现"""
    
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.max_iterations = 10
    
    def run(self, query):
        trace = []
        
        for i in range(self.max_iterations):
            # Thought: 推理下一步
            thought = self._think(query, trace)
            trace.append(('Thought', thought))
            
            # 判断是否可以给出最终答案
            if 'Final Answer:' in thought:
                return self._extract_final_answer(thought)
            
            # Action: 选择并执行工具
            action, action_input = self._parse_action(thought)
            if action in self.tools:
                observation = self.tools[action].run(action_input)
                trace.append(('Action', f"{action}({action_input})"))
                trace.append(('Observation', observation))
            
            # 如果推理陷入循环，强制退出
            if self._is_stuck(trace):
                return self._fallback_answer(query, trace)
        
        return "抱歉，我无法在有限的步骤内完成任务。"
    
    def _think(self, query, trace):
        """生成下一步思考"""
        prompt = self._build_prompt(query, trace)
        return self.llm.generate(prompt)
    
    def _build_prompt(self, query, trace):
        """构建 ReAct Prompt"""
        history = "\n".join([f"{step[0]}: {step[1]}" for step in trace])
        
        return f"""Answer the following question using the ReAct framework.

Question: {query}

{history}

Available Tools:
{self._format_tools()}

Follow this format:
Thought: [your reasoning]
Action: [tool name]
Action Input: [tool input]
OR
Thought: [your reasoning]
Final Answer: [your answer to the question]

Begin:

Thought:"""
```

**ReAct 模式的优缺点**：

| 优点 | 缺点 |
|-----|------|
| 可解释性强，每步决策可见 | Token 消耗较大 |
| 灵活，可动态调整策略 | 可能陷入推理循环 |
| 容易集成各种工具 | 推理质量依赖 LLM 能力 |

### 3.2 工具调用与函数封装 🔧

现代 LLM 原生支持 Function Calling，这比 ReAct 的文本解析更可靠：

```python
from pydantic import BaseModel, Field
from typing import Literal

class WeatherInput(BaseModel):
    """天气查询工具参数"""
    city: str = Field(description="城市名称")
    unit: Literal["celsius", "fahrenheit"] = Field(default="celsius")

class ToolRegistry:
    """工具注册中心"""
    
    def __init__(self):
        self.tools = {}
        self.schemas = []
    
    def register(self, name: str, description: str, 
                 input_model: type[BaseModel], handler: Callable):
        """注册工具"""
        self.tools[name] = {
            'handler': handler,
            'input_model': input_model
        }
        
        # 生成 OpenAI Function Calling 格式的 Schema
        self.schemas.append({
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": input_model.model_json_schema()
            }
        })
    
    def execute(self, name: str, arguments: dict):
        """执行工具调用"""
        if name not in self.tools:
            raise ToolNotFoundError(f"Tool {name} not found")
        
        tool = self.tools[name]
        validated_input = tool['input_model'](**arguments)
        return tool['handler'](validated_input)


# 使用示例
registry = ToolRegistry()

def get_weather(input: WeatherInput) -> dict:
    return {"city": input.city, "temp": 25, "condition": "sunny"}

registry.register(
    name="get_weather",
    description="查询指定城市的天气信息",
    input_model=WeatherInput,
    handler=get_weather
)

# LLM 调用
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "北京今天天气怎么样？"}],
    tools=registry.schemas,
    tool_choice="auto"
)

# 处理工具调用
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        result = registry.execute(
            tool_call.function.name,
            json.loads(tool_call.function.arguments)
        )
```

**工具设计最佳实践**：

1. **单一职责**：每个工具只做一件事
2. **幂等性**：相同输入产生相同输出
3. **超时控制**：所有外部调用必须设置超时
4. **错误处理**：返回结构化错误信息，而非抛异常

### 3.3 多智能体协作模式 🤝

复杂任务往往需要多个专业智能体协作完成：

```python
from enum import Enum
from typing import Protocol

class AgentRole(Enum):
    PLANNER = "planner"      # 规划者：分解任务
    EXECUTOR = "executor"    # 执行者：执行子任务
    REVIEWER = "reviewer"    # 审核者：检查结果
    COORDINATOR = "coordinator"  # 协调者：管理流程

class Agent(Protocol):
    role: AgentRole
    def can_handle(self, task: str) -> bool: ...
    async def execute(self, task: str, context: dict) -> str: ...

class MultiAgentOrchestrator:
    """多智能体协调器"""
    
    def __init__(self):
        self.agents: dict[AgentRole, list[Agent]] = defaultdict(list)
        self.message_bus = MessageBus()
    
    def register_agent(self, agent: Agent):
        self.agents[agent.role].append(agent)
    
    async def run(self, task: str):
        # 1. 规划阶段
        plan = await self._plan(task)
        
        # 2. 执行阶段
        results = []
        for subtask in plan.subtasks:
            executor = self._select_executor(subtask)
            result = await executor.execute(subtask, {"plan": plan})
            results.append(result)
        
        # 3. 审核阶段
        review = await self._review(results)
        
        # 4. 整合阶段
        final_result = await self._integrate(results, review)
        
        return final_result
    
    async def _plan(self, task: str) -> Plan:
        planner = self.agents[AgentRole.PLANNER][0]
        plan_str = await planner.execute(f"请将以下任务分解为子任务：{task}", {})
        return self._parse_plan(plan_str)
    
    def _select_executor(self, subtask: str) -> Agent:
        for agent in self.agents[AgentRole.EXECUTOR]:
            if agent.can_handle(subtask):
                return agent
        return self.agents[AgentRole.EXECUTOR][0]
    
    async def _review(self, results: list[str]) -> ReviewResult:
        reviewer = self.agents[AgentRole.REVIEWER][0]
        return await reviewer.execute(f"请审核以下执行结果：{results}", {})


# 具体智能体实现示例
class CodeWriterAgent(Agent):
    """代码编写智能体"""
    role = AgentRole.EXECUTOR
    
    def can_handle(self, task: str) -> bool:
        keywords = ["编写代码", "实现函数", "写一个"]
        return any(kw in task for kw in keywords)
    
    async def execute(self, task: str, context: dict) -> str:
        return await self.llm.generate(
            f"作为代码专家，{task}\n要求：输出可执行的代码，包含注释。"
        )
```

**协作模式对比**：

| 模式 | 适用场景 | 复杂度 | 效率 |
|-----|---------|-------|------|
| 顺序协作 | 流水线任务 | 低 | 中 |
| 层级协作 | 需要规划的任务 | 中 | 高 |
| 对等协作 | 需要多角度分析 | 高 | 低 |
| 混合模式 | 复杂综合任务 | 高 | 中 |

---

## 四、实战：构建评估管道

### 4.1 LLM-as-a-Judge 评分方法 📊

让 LLM 评估 LLM 的输出，是目前最实用的评估方法：

```python
from pydantic import BaseModel

class EvaluationResult(BaseModel):
    score: float  # 0-1
    reasoning: str
    issues: list[str]

class LLMJudge:
    """LLM 评判器"""
    
    def __init__(self, judge_model: str = "gpt-4"):
        self.judge_model = judge_model
    
    def evaluate_response(self, query: str, response: str,
                          criteria: list[str], reference: str = None) -> EvaluationResult:
        
        prompt = f"""你是一个专业的评估者。请根据以下标准评估智能体的回答。

**用户问题**：{query}

**智能体回答**：{response}

{"**参考答案**：" + reference if reference else ""}

**评估标准**：
{self._format_criteria(criteria)}

请输出 JSON 格式的评估结果：
{{
    "score": <0-1之间的分数>,
    "reasoning": "<评分理由>",
    "issues": ["<问题1>", "<问题2>", ...]
}}
"""
        
        result = self.llm.generate(prompt, response_format="json")
        return EvaluationResult(**json.loads(result))
    
    def _format_criteria(self, criteria: list[str]) -> str:
        return "\n".join([f"- {c}" for c in criteria])


# 使用示例
judge = LLMJudge()
result = judge.evaluate_response(
    query="如何实现一个简单的 LRU 缓存？",
    response="可以使用 Python 的 OrderedDict 来实现...",
    criteria=["代码是否正确实现 LRU 逻辑", "解释是否清晰易懂", "是否考虑了边界情况"],
    reference="LRU 缓存的核心是..."
)

print(f"得分：{result.score}")
print(f"问题：{result.issues}")
```

**评判维度设计**：

```python
EVALUATION_DIMENSIONS = {
    "correctness": {
        "description": "答案的正确性",
        "criteria": ["事实陈述是否准确", "逻辑推理是否正确", "结论是否合理"]
    },
    "completeness": {
        "description": "答案的完整性",
        "criteria": ["是否回答了问题的所有方面", "是否遗漏重要信息"]
    },
    "clarity": {
        "description": "答案的清晰度",
        "criteria": ["语言表达是否清晰", "结构是否合理", "是否有不必要的冗余"]
    },
    "safety": {
        "description": "答案的安全性",
        "criteria": ["是否包含有害内容", "是否尊重隐私", "是否遵守伦理准则"]
    }
}
```

### 4.2 基于追踪的行为分析 🔍

记录智能体的完整执行轨迹，是深度分析的基础：

```python
import json
from datetime import datetime
from typing import Any
from dataclasses import dataclass, field, asdict

@dataclass
class TraceStep:
    """执行轨迹步骤"""
    timestamp: str
    step_type: str  # thought, action, observation, output
    content: Any
    metadata: dict = field(default_factory=dict)
    latency_ms: float = 0

class AgentTracer:
    """智能体执行追踪器"""
    
    def __init__(self):
        self.trace: list[TraceStep] = []
        self.start_time = datetime.now()
    
    def record_thought(self, thought: str, metadata: dict = None):
        self.trace.append(TraceStep(
            timestamp=datetime.now().isoformat(),
            step_type="thought",
            content=thought,
            metadata=metadata or {}
        ))
    
    def record_action(self, tool: str, args: dict, latency: float):
        self.trace.append(TraceStep(
            timestamp=datetime.now().isoformat(),
            step_type="action",
            content={"tool": tool, "args": args},
            latency_ms=latency
        ))
    
    def record_observation(self, result: Any, latency: float):
        self.trace.append(TraceStep(
            timestamp=datetime.now().isoformat(),
            step_type="observation",
            content=result,
            latency_ms=latency
        ))
    
    def export(self) -> str:
        return json.dumps([asdict(step) for step in self.trace], 
                         ensure_ascii=False, indent=2)


class TraceAnalyzer:
    """轨迹分析器"""
    
    def analyze(self, trace: list[dict]) -> dict:
        return {
            "total_steps": len(trace),
            "action_count": self._count_type(trace, "action"),
            "avg_latency": self._avg_latency(trace),
            "tool_usage": self._tool_usage(trace),
            "thought_patterns": self._analyze_thoughts(trace),
            "error_indicators": self._find_errors(trace)
        }
    
    def _count_type(self, trace: list, step_type: str) -> int:
        return sum(1 for step in trace if step["step_type"] == step_type)
    
    def _avg_latency(self, trace: list) -> float:
        latencies = [step["latency_ms"] for step in trace if step["latency_ms"]]
        return sum(latencies) / len(latencies) if latencies else 0
    
    def _tool_usage(self, trace: list) -> dict:
        usage = defaultdict(int)
        for step in trace:
            if step["step_type"] == "action":
                tool = step["content"].get("tool", "unknown")
                usage[tool] += 1
        return dict(usage)
    
    def _find_errors(self, trace: list) -> list:
        errors = []
        for i, step in enumerate(trace):
            if step["step_type"] == "observation":
                if isinstance(step["content"], dict):
                    if step["content"].get("error"):
                        errors.append({
                            "step_index": i,
                            "error": step["content"]["error"],
                            "context": trace[max(0, i-2):i+1]
                        })
        return errors
```

### 4.3 可复现测试工具 🧪

构建可复现的测试套件，关键在于控制随机性：

```python
import hashlib
import json
from typing import Callable

class ReproducibleTestCase:
    """可复现测试用例"""
    
    def __init__(self, input: str, expected_intent: str = None,
                 validation_func: Callable = None, seed: int = None):
        self.input = input
        self.expected_intent = expected_intent
        self.validation_func = validation_func
        self.seed = seed or self._generate_seed(input)
    
    def _generate_seed(self, input: str) -> int:
        return int(hashlib.md5(input.encode()).hexdigest(), 16) % (2**32)
    
    def run(self, agent, temperature: float = 0) -> dict:
        agent.set_seed(self.seed)
        
        original_temp = agent.temperature
        agent.temperature = temperature
        
        try:
            response = agent.run(self.input)
            result = {
                "input": self.input,
                "output": response,
                "seed": self.seed,
                "passed": True
            }
            
            if self.validation_func:
                result["passed"] = self.validation_func(response)
            
            return result
        finally:
            agent.temperature = original_temp


class AgentTestSuite:
    """智能体测试套件"""
    
    def __init__(self, agent):
        self.agent = agent
        self.test_cases: list[ReproducibleTestCase] = []
        self.baseline_results: dict = {}
    
    def add_test(self, test_case: ReproducibleTestCase):
        self.test_cases.append(test_case)
    
    def load_baseline(self, baseline_path: str):
        with open(baseline_path) as f:
            self.baseline_results = json.load(f)
    
    def run_all(self) -> dict:
        results = []
        passed = 0
        
        for test in self.test_cases:
            result = test.run(self.agent)
            results.append(result)
            if result["passed"]:
                passed += 1
        
        return {
            "total": len(self.test_cases),
            "passed": passed,
            "pass_rate": passed / len(self.test_cases),
            "results": results
        }
    
    def compare_with_baseline(self, current_results: dict) -> dict:
        comparisons = []
        
        for current in current_results["results"]:
            test_id = str(current["seed"])
            if test_id in self.baseline_results:
                baseline = self.baseline_results[test_id]
                comparisons.append({
                    "test_id": test_id,
                    "input": current["input"],
                    "baseline_output": baseline["output"],
                    "current_output": current["output"],
                    "output_changed": current["output"] != baseline["output"],
                    "status_changed": baseline["passed"] != current["passed"]
                })
        
        return comparisons
```

---

## 五、生产环境最佳实践

### 5.1 数据脱敏与隐私保护 🔒

智能体处理用户输入时，必须考虑数据隐私：

```python
import re
from typing import Optional

class DataAnonymizer:
    """数据脱敏处理器"""
    
    def __init__(self):
        self.patterns = {
            "phone": (r'1[3-9]\d{9}', self._mask_phone),
            "email": (r'[\w.-]+@[\w.-]+\.\w+', self._mask_email),
            "id_card": (r'\d{17}[\dXx]', self._mask_id_card),
            "bank_card": (r'\d{16,19}', self._mask_bank_card),
            "ip_address": (r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', self._mask_ip),
        }
        self.mapping = {}
    
    def anonymize(self, text: str) -> tuple[str, dict]:
        result = text
        self.mapping = {}
        
        for pattern_name, (pattern, mask_func) in self.patterns.items():
            result = re.sub(pattern, 
                           lambda m: self._replace(m, pattern_name, mask_func),
                           result)
        
        return result, self.mapping
    
    def _replace(self, match, pattern_name: str, mask_func) -> str:
        original = match.group()
        masked = mask_func(original)
        key = f"<{pattern_name}_{len(self.mapping)}>"
        self.mapping[key] = original
        return masked
    
    def _mask_phone(self, phone: str) -> str:
        return phone[:3] + "****" + phone[-4:]
    
    def _mask_email(self, email: str) -> str:
        parts = email.split("@")
        return parts[0][:2] + "***@" + parts[1]
    
    def _mask_id_card(self, id_card: str) -> str:
        return id_card[:6] + "********" + id_card[-4:]
    
    def _mask_bank_card(self, card: str) -> str:
        return "****" + card[-4:]
    
    def _mask_ip(self, ip: str) -> str:
        parts = ip.split(".")
        return f"{parts[0]}.{parts[1]}.***.***"
    
    def restore(self, text: str, mapping: dict) -> str:
        result = text
        for key, original in mapping.items():
            result = result.replace(key, original)
        return result


# 使用示例
anonymizer = DataAnonymizer()

user_input = "我的手机号是 13812345678，邮箱是 test@example.com"
anonymized, mapping = anonymizer.anonymize(user_input)
# 输出: "我的手机号是 138****5678，邮箱是 te***@example.com"

response = llm.generate(anonymized)
restored = anonymizer.restore(response, mapping)
```

### 5.2 持续监控与迭代优化 📈

生产环境需要全方位的监控体系：

```python
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import prometheus_client as prom

# Prometheus 指标
REQUEST_COUNT = prom.Counter(
    'agent_requests_total', 'Total agent requests',
    ['agent_name', 'status']
)

REQUEST_LATENCY = prom.Histogram(
    'agent_request_latency_seconds', 'Request latency in seconds',
    ['agent_name']
)

TOOL_CALLS = prom.Counter(
    'agent_tool_calls_total', 'Tool call counts',
    ['tool_name', 'status']
)

TOKEN_USAGE = prom.Counter(
    'agent_token_usage_total', 'Token usage counts',
    ['agent_name', 'type']
)

@dataclass
class AgentMetrics:
    """智能体运行指标"""
    request_id: str
    agent_name: str
    start_time: datetime
    end_time: datetime = None
    status: str = "pending"
    latency_ms: float = 0
    token_input: int = 0
    token_output: int = 0
    tool_calls: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    user_feedback: int = None

class MetricsCollector:
    """指标收集器"""
    
    def __init__(self):
        self.metrics_store: list[AgentMetrics] = []
    
    def start_request(self, request_id: str, agent_name: str) -> AgentMetrics:
        metrics = AgentMetrics(
            request_id=request_id,
            agent_name=agent_name,
            start_time=datetime.now()
        )
        self.metrics_store.append(metrics)
        return metrics
    
    def end_request(self, metrics: AgentMetrics, status: str):
        metrics.end_time = datetime.now()
        metrics.status = status
        metrics.latency_ms = (metrics.end_time - metrics.start_time).total_seconds() * 1000
        
        REQUEST_COUNT.labels(agent_name=metrics.agent_name, status=status).inc()
        REQUEST_LATENCY.labels(agent_name=metrics.agent_name).observe(metrics.latency_ms / 1000)
        TOKEN_USAGE.labels(agent_name=metrics.agent_name, type="input").inc(metrics.token_input)
        TOKEN_USAGE.labels(agent_name=metrics.agent_name, type="output").inc(metrics.token_output)
    
    def record_tool_call(self, metrics: AgentMetrics, tool_name: str, status: str):
        metrics.tool_calls.append({"tool": tool_name, "status": status, "timestamp": datetime.now().isoformat()})
        TOOL_CALLS.labels(tool_name=tool_name, status=status).inc()
    
    def get_aggregated_stats(self, agent_name: str, time_range: tuple) -> dict:
        start, end = time_range
        filtered = [m for m in self.metrics_store if m.agent_name == agent_name and start <= m.start_time <= end]
        
        return {
            "total_requests": len(filtered),
            "success_rate": sum(1 for m in filtered if m.status == "success") / len(filtered),
            "avg_latency_ms": sum(m.latency_ms for m in filtered) / len(filtered),
            "total_tokens": sum(m.token_input + m.token_output for m in filtered),
            "tool_usage": self._aggregate_tool_usage(filtered),
            "error_distribution": self._aggregate_errors(filtered)
        }
```

### 5.3 版本管理与回滚策略 🔄

智能体的版本管理比传统软件更复杂，需要同时管理代码、Prompt 和模型版本：

```python
from dataclasses import dataclass
from typing import Optional
import yaml

@dataclass
class AgentVersion:
    """智能体版本定义"""
    version_id: str
    code_version: str
    prompt_version: str
    model_version: str
    config: dict
    created_at: str
    description: str

class VersionManager:
    """版本管理器"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.versions: dict[str, AgentVersion] = {}
        self.current_version: Optional[str] = None
        self.load_versions()
    
    def load_versions(self):
        version_file = f"agents/{self.agent_name}/versions.yaml"
        try:
            with open(version_file) as f:
                data = yaml.safe_load(f)
                for v in data.get("versions", []):
                    version = AgentVersion(**v)
                    self.versions[version.version_id] = version
                self.current_version = data.get("current_version")
        except FileNotFoundError:
            pass
    
    def create_version(self, code_version: str, prompt_version: str,
                       model_version: str, config: dict, description: str) -> AgentVersion:
        version_id = f"v{len(self.versions) + 1}"
        
        version = AgentVersion(
            version_id=version_id,
            code_version=code_version,
            prompt_version=prompt_version,
            model_version=model_version,
            config=config,
            created_at=datetime.now().isoformat(),
            description=description
        )
        
        self.versions[version_id] = version
        self._save_versions()
        return version
    
    def rollback(self, version_id: str) -> bool:
        if version_id not in self.versions:
            return False
        
        target = self.versions[version_id]
        self._checkout_code(target.code_version)
        self._load_prompt(target.prompt_version)
        self._update_model_config(target.model_version)
        self.current_version = version_id
        self._save_versions()
        return True
    
    def canary_deploy(self, new_version: str, traffic_percent: float):
        """金丝雀发布：部分用户使用新版本"""
        pass
    
    def _save_versions(self):
        version_file = f"agents/{self.agent_name}/versions.yaml"
        data = {
            "current_version": self.current_version,
            "versions": [{
                "version_id": v.version_id,
                "code_version": v.code_version,
                "prompt_version": v.prompt_version,
                "model_version": v.model_version,
                "config": v.config,
                "created_at": v.created_at,
                "description": v.description
            } for v in self.versions.values()]
        }
        
        with open(version_file, 'w') as f:
            yaml.dump(data, f)
```

---

## 总结 🎯

AI 智能体从原型到生产的跨越，需要在以下方面持续投入：

| 方向 | 关键要点 |
|------|----------|
| **评估体系** | 建立覆盖智能、性能、可靠性、安全、体验的五维评估框架 |
| **架构设计** | 选择合适的模式（ReAct、工具调用、多智能体），权衡复杂度与灵活性 |
| **工程实践** | 构建可复现的测试管道，实施全面监控，建立版本管理机制 |
| **安全合规** | 数据脱敏、隐私保护、内容安全，一个都不能少 |

> 💡 **生产级智能体不是"训练"出来的，而是"工程化"打磨出来的。**

希望本文的框架和代码示例，能帮助你在智能体落地之路上少走弯路。

---

*本文首发于 [技术博客]，欢迎交流讨论。代码示例已上传 GitHub：[链接]*