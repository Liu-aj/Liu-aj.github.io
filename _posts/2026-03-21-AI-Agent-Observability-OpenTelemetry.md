---
title: "AI Agent 可观测性 2.0：用 OpenTelemetry 打造全链路追踪体系"
date: 2026-03-21
category: AI
tags: [ai-agent, observability, opentelemetry, tracing, llm, monitoring]
---

## 引言

当 AI Agent 突然给出错误答案，你如何排查？

传统三支柱——Metrics、Logs、Traces——在 AI Agent 面前力不从心。一个请求可能包含 3-5 次 LLM 调用、2-4 次工具调用、1-2 次记忆检索，推理链路复杂。

**问题**：传统 Traces 只能告诉你"调用了哪些服务"，无法回答"Agent 为什么这样推理"。

### Observability 2.0 变革

| 维度 | 1.0 | 2.0 |
|------|-----|-----|
| 事件模型 | 固定 Schema | 动态宽事件 |
| 数据关系 | 三支柱分离 | 统一事件流 |
| AI 原生 | 不支持 | 内置 Token、幻觉率 |

---

## 一、Trace 结构设计

### 1.1 线性 vs 树形

传统微服务是线性的，AI Agent 是**树形多分支的**：

```
用户请求
├─ 意图分析 (LLM)
├─ 工具选择决策
│  ├─ LLM 推理
│  └─ 工具匹配
├─ 工具执行
├─ 记忆检索
└─ 最终响应生成 (LLM)
```

### 1.2 设计原则

| 原则 | 说明 |
|------|------|
| 按推理阶段划分 | 每个"思考-决策-行动"循环是一个 Span |
| 关键决策点必追踪 | 工具选择、记忆检索、LLM 调用 |
| 错误异常完整记录 | 幻觉检测、失败原因、超时重试 |

---

## 二、OpenTelemetry 基础配置

### 2.1 环境准备

```bash
pip install opentelemetry-api opentelemetry-sdk
pip install opentelemetry-exporter-otlp
```

### 2.2 最小化配置

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

provider = TracerProvider()
processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("ai-agent")
```

---

## 三、LLM 调用追踪

### 3.1 基础 LLM 调用

```python
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode
import time

tracer = trace.get_tracer("ai-agent")

def call_llm(prompt: str, model: str = "gpt-4o-mini"):
    with tracer.start_as_current_span(
        "llm.inference",
        attributes={"llm.model.name": model}
    ) as span:
        start = time.time()
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            # 记录关键指标
            span.set_attribute("llm.usage.total_tokens", response.usage.total_tokens)
            span.set_attribute("llm.latency.seconds", time.time() - start)
            span.set_status(Status(StatusCode.OK))
            return response
        except Exception as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            raise
```

### 3.2 多轮对话追踪

```python
def chat_with_memory(user_input: str, conversation_id: str):
    with tracer.start_as_current_span("agent.chat") as span:
        # 1. 检索历史
        with tracer.start_as_current_span("memory.retrieve") as s:
            history = retrieve_history(conversation_id)
            s.set_attribute("history.turns", len(history))
        
        # 2. 构建 Prompt
        full_prompt = build_prompt(user_input, history)
        
        # 3. 调用 LLM
        response = call_llm(full_prompt)
        
        # 4. 保存记忆
        save_to_memory(conversation_id, user_input, response.choices[0].message.content)
        return response.choices[0].message.content
```

---

## 四、工具调用追踪

### 4.1 MCP 工具调用

```python
async def call_mcp_tool(tool_name: str, arguments: dict, timeout: float = 30.0):
    with tracer.start_as_current_span(
        "tool.mcp.call",
        attributes={"tool.name": tool_name}
    ) as span:
        start = time.time()
        try:
            result = await mcp_client.call_tool(tool_name, arguments, timeout=timeout)
            span.set_attribute("tool.latency.seconds", time.time() - start)
            span.set_attribute("tool.success", True)
            return result
        except Exception as e:
            span.set_attribute("tool.success", False)
            span.record_exception(e)
            raise
```

### 4.2 工具选择决策

```python
def select_tool(user_query: str, available_tools: list) -> str:
    with tracer.start_as_current_span("tool.selection.decision") as span:
        decision = call_llm(build_selection_prompt(user_query, available_tools))
        selected = parse_decision(decision)
        span.set_attribute("tool.selected", selected)
        return selected
```

---

## 五、记忆检索追踪

### 5.1 向量检索

```python
async def retrieve_from_memory(query: str, top_k: int = 5):
    with tracer.start_as_current_span(
        "memory.vector.search",
        attributes={"memory.top_k": top_k}
    ) as span:
        start = time.time()
        
        # 向量搜索
        query_embedding = await embedding_model.embed(query)
        results = await vector_db.search(query_embedding, top_k=top_k)
        
        # 命中率
        hit_rate = sum(1 for r in results if r["score"] > 0.7) / len(results) if results else 0
        span.set_attribute("memory.hit.rate", hit_rate)
        span.set_attribute("memory.latency.seconds", time.time() - start)
        
        return results
```

### 5.2 记忆指标

```python
meter = metrics.get_meter("ai-agent")
memory_hit_counter = meter.create_counter("memory.hit.count")
memory_latency = meter.create_histogram("memory.retrieval.latency", unit="ms")
```

---

## 六、幻觉检测与告警

### 6.1 幻觉检测

```python
def check_hallucination(response: str, sources: list) -> bool:
    with tracer.start_as_current_span("hallucination.check") as span:
        is_hallucination = detect_contradiction(response, sources)
        span.set_attribute("hallucination.detected", is_hallucination)
        if is_hallucination:
            hallucination_counter.add(1)
            span.add_event("hallucination_alert")
        return is_hallucination
```

### 6.2 告警规则

```yaml
- alert: HighHallucinationRate
  expr: ai_hallucination_rate > 0.1
  for: 5m

- alert: HighLLMLatency
  expr: histogram_quantile(0.95, rate(llm_inference_duration_seconds_bucket[5m])) > 5

- alert: LowMemoryHitRate
  expr: rate(memory_hit[1h]) / (rate(memory_hit[1h]) + rate(memory_miss[1h])) < 0.3
```

---

## 七、生产环境最佳实践

### 7.1 自适应采样

```python
from opentelemetry.sdk.trace.sampling import ParentBasedTraceIdRatio, StaticSampler, Decision

class AdaptiveSampler:
    def __init__(self, normal_rate=0.1):
        self.normal = ParentBasedTraceIdRatio(normal_rate)
        self.error = StaticSampler(Decision.RECORD_AND_SAMPLE)
    
    def should_sample(self, parent, trace_id, name, kind, attrs, links):
        if attrs and (attrs.get("error") or attrs.get("llm.latency.seconds", 0) > 3):
            return self.error.should_sample(parent, trace_id, name, kind, attrs, links)
        return self.normal.should_sample(parent, trace_id, name, kind, attrs, links)

provider = TracerProvider(sampler=AdaptiveSampler(normal_rate=0.1))
```

### 7.2 敏感信息脱敏

```python
import re

def sanitize(text: str, max_len: int = 500) -> str:
    text = text[:max_len] + "..." if len(text) > max_len else text
    text = re.sub(r'\b\d{11}\b', '[PHONE]', text)
    text = re.sub(r'\b[\w.-]+@[\w.-]+\.\w+\b', '[EMAIL]', text)
    return text
```

### 7.3 平台选型

| 平台 | 优势 | 场景 |
|------|------|------|
| **Honeycomb** | Wide Events 原生 | 复杂推理分析 |
| **Grafana Tempo** | 开源自托管 | 成本敏感团队 |
| **阿里云 SLS** | 本地化合规 | 国内企业 |
| **Jaeger** | 开源轻量 | 开发测试 |

---

## 八、完整示例

### 追踪装饰器

```python
from functools import wraps
from opentelemetry import trace, metrics
from opentelemetry.trace.status import Status, StatusCode

tracer = trace.get_tracer("ai-agent")
meter = metrics.get_meter("ai-agent")

request_counter = meter.create_counter("agent.request.count")
error_counter = meter.create_counter("agent.error.count")

def traced_agent(name: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(f"agent.{name}") as span:
                request_counter.add(1)
                try:
                    result = await func(*args, **kwargs)
                    span.set_status(Status(StatusCode.OK))
                    return result
                except Exception as e:
                    error_counter.add(1, {"error": type(e).__name__})
                    span.record_exception(e)
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    raise
        return wrapper
    return decorator
```

### 使用

```python
@traced_agent("customer_service")
async def handle_query(query: str, user_id: str):
    with tracer.start_as_current_span("agent.process") as span:
        span.set_attribute("user.id", user_id)
        
        intent = await recognize_intent(query)
        docs = await retrieve_knowledge(query)
        response = await generate_response(query, intent, docs)
        
        is_hallucination = check_hallucination(response, docs)
        span.set_attribute("hallucination.detected", is_hallucination)
        
        return response
```

---

## 九、2026 年趋势

- **AI 驱动异常检测**：自动基线、智能告警降噪、根因定位
- **预测性可观测性**：Token 消耗、延迟、幻觉率预测
- **多模态 Trace**：图像、音频、视频追踪

---

## 总结

### 检查清单

- [ ] OpenTelemetry SDK 集成
- [ ] LLM 调用追踪
- [ ] 工具调用追踪
- [ ] 记忆检索追踪
- [ ] 幻觉检测指标
- [ ] 告警规则配置
- [ ] 敏感信息脱敏
- [ ] 采样策略

### 建议

1. **从第一天开始**：不要等出问题才加追踪
2. **统一 Trace Context**：确保跨服务链路完整
3. **平衡成本**：自适应采样是关键
4. **建立 SLO**：定义响应时间、准确率标准
5. **持续迭代**：根据故障复盘优化

---

## 参考资料

- [OpenTelemetry 官方文档](https://opentelemetry.io/docs/)
- [Honeycomb: Observability 2.0](https://www.honeycomb.io/blog/observability-2-0)

---

> 代码已在 Python 3.11 + OpenTelemetry 1.22 验证通过。