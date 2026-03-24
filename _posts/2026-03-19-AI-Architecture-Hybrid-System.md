---
layout: post
title: "AI架构中的油水难融：确定性系统与概率性智能的融合挑战"
date: 2026-03-19
category: AI
tags: [Architecture, LLM, Hybrid-System]
---

# AI 架构中的"油水难融"：确定性系统与概率性智能的融合挑战

> 当确定性遇见概率性，当规则遇见推理，当传统软件工程遇见大模型——我们正站在一个架构范式转换的十字路口。

## 引言：一个架构师的困境

```
传统系统：输入 → 确定性处理 → 可预测输出
AI 系统：输入 → 概率性推理 → 不确定输出
```

2024 年，当我们的团队将第一个 LLM 集成到核心业务系统时，麻烦接踵而至：同一个问题，上午回复 A，下午回复 B；测试环境完美的 prompt，生产环境却掉了链子；系统监控一片绿，业务投诉却满天飞。

这不仅是技术选型问题，更是两种根本不同的系统范式在碰撞。就像油和水，共存在同一个容器中不难，但真正融合，需要全新的架构思维。

## 一、核心矛盾：两种系统的本质差异

### 1.1 确定性系统的铁律

传统软件系统建立在确定性原则之上：

```java
// 传统业务规则的确定性
public class OrderService {
    public BigDecimal calculateDiscount(Order order) {
        if (order.getTotalAmount().compareTo(new BigDecimal("1000")) >= 0) {
            return order.getTotalAmount().multiply(new BigDecimal("0.1")); // 永远是 10%
        }
        return BigDecimal.ZERO;
    }
}
```

特点鲜明：
- **可复现性**：相同输入，永远相同输出
- **可测试性**：单元测试能 100% 覆盖边界条件
- **可解释性**：每个决策都有明确的代码对应
- **可控性**：Bug 修复是确定性的，改完就能验证

### 1.2 概率性系统的混沌

AI 系统完全是另一套逻辑：

```python
# LLM 的概率性本质
response = llm.generate(
    prompt="分析这条评论的情感倾向",
    temperature=0.7,  # 控制随机性
    top_p=0.9
)
# 同一个 prompt，不同调用可能给出不同结果
# "正面" / "偏正面" / "积极" —— 都对，但不一致
```

核心差异：

| 维度 | 确定性系统 | 概率性系统 |
|------|-----------|-----------|
| 输出 | 唯一确定 | 概率分布采样 |
| 错误 | 代码 Bug | 模型幻觉/偏差 |
| 测试 | 输入输出精确断言 | 统计显著性验证 |
| 调试 | 断点追踪 | 很难追溯 |
| 修复 | 改代码 | 调 prompt 或微调 |

### 1.3 融合时的"相变"问题

两者结合时，问题往往在边界处爆发：

```python
# 典型的集成困境
def process_user_query(query: str) -> dict:
    # 确定性系统期待的结构化输出
    expected_schema = {
        "intent": str,      # 必须是预定义的值之一
        "entities": list,   # 必须是列表
        "confidence": float # 必须在 0-1 之间
    }
    
    # 但 LLM 返回的是概率性的自然语言
    llm_output = llm.generate(f"分析用户意图: {query}")
    
    # 解析失败率通常在 5-15%，取决于 prompt 和模型
    try:
        return parse_structured_output(llm_output, expected_schema)
    except ParseError:
        # 进入异常处理，但这里本身也是概率性的
        return fallback_parse(llm_output)  # 可能再次失败
```

## 二、架构挑战：三个维度的范式转换

### 2.1 决策面的分布式重构

传统系统的决策面清晰可见——if-else、switch-case、策略模式。AI 系统的决策面却"消失"在海量参数中。

**传统决策模式：**

```
决策点 = 代码位置
决策逻辑 = 显式规则
决策修改 = 改代码 + 重新发布
```

**AI 系统决策模式：**

```
决策点 = 模型参数 + Prompt + 检索范围 + 温度参数
决策逻辑 = 隐式分布在数十亿参数中
决策修改 = 调 prompt / 改检索 / 微调 / 换模型
```

**架构实践：让隐式决策显式化**

```python
from dataclasses import dataclass
from typing import List, Dict, Any
import hashlib

@dataclass
class DecisionTrace:
    """AI 决策的完整溯源"""
    decision_id: str
    timestamp: float
    
    # 输入层面
    user_query: str
    context_documents: List[str]  # RAG 检索的文档
    
    # 模型层面
    model_version: str
    prompt_template: str
    prompt_hash: str              # 追踪 prompt 变更
    temperature: float
    top_p: float
    
    # 检索层面
    retrieval_query: str          # 实际检索语句
    retrieved_doc_ids: List[str]
    retrieval_scores: List[float]
    
    # 输出层面
    raw_output: str
    parsed_output: Dict[str, Any]
    output_hash: str
    
    # 元数据
    latency_ms: float
    token_count: int

class DecisionTracker:
    """决策追踪器 - 把隐式决策晒到阳光下"""
    
    def __init__(self, vector_store, llm):
        self.vector_store = vector_store
        self.llm = llm
        self.decision_log = []
        
    def make_decision(self, query: str, prompt_template: str, 
                      config: dict) -> DecisionTrace:
        # 1. 检索相关上下文
        retrieval_result = self.vector_store.search(
            query=config.get("retrieval_query", query),
            k=config.get("top_k", 5)
        )
        
        # 2. 构建 prompt
        context = "\n".join([doc.content for doc in retrieval_result.docs])
        prompt = prompt_template.format(context=context, query=query)
        
        # 3. 调用 LLM
        response = self.llm.generate(
            prompt=prompt,
            temperature=config.get("temperature", 0.7),
            top_p=config.get("top_p", 0.9)
        )
        
        # 4. 记录完整决策轨迹
        trace = DecisionTrace(
            decision_id=hashlib.md5(f"{query}{time.time()}".encode()).hexdigest()[:12],
            timestamp=time.time(),
            user_query=query,
            context_documents=[doc.id for doc in retrieval_result.docs],
            model_version=self.llm.version,
            prompt_template=prompt_template[:100] + "...",
            prompt_hash=hashlib.sha256(prompt_template.encode()).hexdigest()[:16],
            temperature=config["temperature"],
            top_p=config["top_p"],
            retrieval_query=config.get("retrieval_query", query),
            retrieved_doc_ids=[doc.id for doc in retrieval_result.docs],
            retrieval_scores=[doc.score for doc in retrieval_result.docs],
            raw_output=response.text,
            parsed_output=self._parse_output(response.text),
            output_hash=hashlib.md5(response.text.encode()).hexdigest()[:8],
            latency_ms=response.latency_ms,
            token_count=response.token_count
        )
        
        self.decision_log.append(trace)
        return trace
    
    def analyze_decision_variance(self, query: str, n_samples: int = 10):
        """分析同一查询的决策方差"""
        results = []
        for _ in range(n_samples):
            trace = self.make_decision(query, self.default_prompt, {})
            results.append(trace.parsed_output)
        
        # 计算输出稳定性分数
        # ... 统计分析逻辑
        return {
            "query": query,
            "variance": self._compute_variance(results),
            "stability_score": self._compute_stability(results),
            "sample_outputs": results
        }
```

### 2.2 可观测性的维度扩展

传统可观测性三板斧（Metrics、Logs、Traces）在 AI 系统中需要升级。

**扩展后的可观测性矩阵：**

```
传统维度：
├── Metrics: 延迟、错误率、吞吐量
├── Logs: 结构化日志
└── Traces: 调用链追踪

AI 扩展维度：
├── Prompt 遗产学
│   ├── prompt_template_id
│   ├── prompt_version
│   ├── prompt_hash
│   └── prompt_effectiveness_score
├── 上下文来源追踪
│   ├── retrieved_doc_ids
│   ├── retrieval_strategy
│   ├── context_window_utilization
│   └── context_relevance_score
├── 输出差异分析
│   ├── output_stability (多次调用的一致性)
│   ├── parsing_success_rate
│   ├── hallucination_detection_score
│   └── human_feedback_score
└── 经济指标
    ├── token_cost_per_query
    ├── latency_p50/p95/p99
    └── quality_cost_ratio
```

**架构图：AI 可观测性平台**

```
┌─────────────────────────────────────────────────────────────────┐
│                      AI Observability Platform                    │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  Prompt      │  │  Context     │  │  Output      │           │
│  │  Lineage     │  │  Tracking    │  │  Analysis    │           │
│  │  Service    │  │  Service     │  │  Service     │           │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘           │
│         │                 │                 │                    │
│         └─────────────────┼─────────────────┘                    │
│                           ▼                                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              Unified Decision Trace Store                   │ │
│  │   (时序数据库 + 图数据库 + 向量数据库的混合存储)              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                           │                                      │
│         ┌─────────────────┼─────────────────┐                   │
│         ▼                 ▼                 ▼                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  实时监控    │  │  离线分析    │  │  告警系统    │           │
│  │  Dashboard   │  │  Pipeline    │  │  Alerting    │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

**核心代码：扩展的追踪系统**

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

class AIObservabilityExtension:
    """AI 系统可观测性扩展"""
    
    def __init__(self):
        self.tracer = trace.get_tracer(__name__)
        
    def trace_llm_call(self, func):
        """装饰器：为 LLM 调用添加扩展追踪"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self.tracer.start_as_current_span("llm.call") as span:
                start_time = time.time()
                
                try:
                    result = func(*args, **kwargs)
                    
                    # AI 扩展指标
                    span.set_attribute("llm.model", kwargs.get("model"))
                    span.set_attribute("llm.prompt_tokens", result.usage.prompt_tokens)
                    span.set_attribute("llm.completion_tokens", result.usage.completion_tokens)
                    span.set_attribute("llm.total_cost", self._calculate_cost(result.usage))
                    
                    # Prompt 遗产
                    prompt_hash = hashlib.sha256(
                        kwargs.get("prompt", "").encode()
                    ).hexdigest()[:16]
                    span.set_attribute("llm.prompt_hash", prompt_hash)
                    
                    # 输出质量评估
                    quality_score = self._assess_output_quality(result.text)
                    span.set_attribute("llm.quality_score", quality_score)
                    
                    # 幻觉风险检测
                    hallucination_risk = self._detect_hallucination_risk(
                        result.text, 
                        kwargs.get("context", "")
                    )
                    span.set_attribute("llm.hallucination_risk", hallucination_risk)
                    
                    return result
                    
                except Exception as e:
                    span.set_attribute("llm.error", str(e))
                    span.set_attribute("llm.error_type", type(e).__name__)
                    raise
                finally:
                    span.set_attribute("llm.latency_ms", (time.time() - start_time) * 1000)
                    
        return wrapper
```

### 2.3 治理：从静态规则到运行时自适应

传统治理发生在设计时：制定规则 → 编码实现 → 部署执行。AI 系统需要在运行时动态调整。

**治理模式的演变：**

```
传统治理:
[规则设计] → [代码实现] → [测试验证] → [部署执行]
                ↑
            变更需要重新发布

AI 治理:
[原则定义] → [策略配置] → [运行时执行] → [效果监控]
                ↑                            ↓
                └──── [动态调整] ←──── [反馈学习]
```

**运行时治理引擎：**

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class GovernanceContext:
    """治理上下文"""
    user_query: str
    intent: str
    entities: Dict[str, Any]
    confidence: float
    model_output: str
    user_metadata: Dict[str, Any]
    session_context: Dict[str, Any]

class GovernanceRule(ABC):
    """治理规则抽象"""
    
    @abstractmethod
    def evaluate(self, context: GovernanceContext) -> Tuple[bool, str, RiskLevel]:
        """评估规则，返回 (是否通过, 原因, 风险等级)"""
        pass

class RuntimeGovernanceEngine:
    """运行时治理引擎"""
    
    def __init__(self):
        self.rules: List[GovernanceRule] = []
        self.strategies: Dict[str, Any] = {}
        self.audit_log = []
        
    def register_rule(self, rule: GovernanceRule, priority: int = 0):
        """注册治理规则"""
        self.rules.append((priority, rule))
        self.rules.sort(key=lambda x: x[0], reverse=True)
        
    def evaluate(self, context: GovernanceContext) -> Dict[str, Any]:
        """执行治理评估"""
        results = []
        overall_risk = RiskLevel.LOW
        
        for priority, rule in self.rules:
            passed, reason, risk = rule.evaluate(context)
            results.append({
                "rule": rule.__class__.__name__,
                "passed": passed,
                "reason": reason,
                "risk": risk.value,
                "priority": priority
            })
            
            if not passed:
                overall_risk = max(overall_risk, risk, 
                                   key=lambda r: list(RiskLevel).index(r))
        
        # 记录审计日志
        self._log_audit(context, results, overall_risk)
        
        return {
            "decision": "allow" if overall_risk != RiskLevel.CRITICAL else "block",
            "risk_level": overall_risk.value,
            "rule_results": results,
            "mitigation_actions": self._get_mitigation_actions(overall_risk)
        }
    
    def update_strategy(self, strategy_name: str, config: Dict[str, Any]):
        """动态更新治理策略，无需重新发布"""
        self.strategies[strategy_name] = config
        self._reload_rules()
        
    def _get_mitigation_actions(self, risk: RiskLevel) -> List[str]:
        """根据风险等级获取缓解措施"""
        actions = {
            RiskLevel.LOW: [],
            RiskLevel.MEDIUM: ["add_disclaimer"],
            RiskLevel.HIGH: ["add_disclaimer", "human_review"],
            RiskLevel.CRITICAL: ["block_response", "escalate"]
        }
        return actions.get(risk, [])


# 具体规则实现示例
class PIIProtectionRule(GovernanceRule):
    """PII 保护规则"""
    
    def __init__(self, pii_detector):
        self.pii_detector = pii_detector
        
    def evaluate(self, context: GovernanceContext) -> tuple[bool, str, RiskLevel]:
        pii_found = self.pii_detector.scan(context.model_output)
        
        if pii_found:
            return (False, f"检测到敏感信息: {pii_found}", RiskLevel.HIGH)
        return (True, "无 PII 泄露风险", RiskLevel.LOW)


class ContentSafetyRule(GovernanceRule):
    """内容安全规则"""
    
    def __init__(self, safety_classifier):
        self.safety_classifier = safety_classifier
        
    def evaluate(self, context: GovernanceContext) -> tuple[bool, str, RiskLevel]:
        safety_result = self.safety_classifier.classify(context.model_output)
        
        if safety_result.is_unsafe:
            return (
                False, 
                f"内容安全违规: {safety_result.violation_type}",
                RiskLevel.HIGH
            )
        return (True, "内容安全检查通过", RiskLevel.LOW)


class FactualAccuracyRule(GovernanceRule):
    """事实准确性规则（使用 RAG 验证）"""
    
    def __init__(self, fact_checker, threshold: float = 0.7):
        self.fact_checker = fact_checker
        self.threshold = threshold
        
    def evaluate(self, context: GovernanceContext) -> tuple[bool, str, RiskLevel]:
        if not context.session_context.get("source_documents"):
            return (True, "无参考文档，跳过事实检查", RiskLevel.LOW)
            
        accuracy = self.fact_checker.verify(
            claim=context.model_output,
            sources=context.session_context["source_documents"]
        )
        
        if accuracy < self.threshold:
            return (
                False,
                f"事实准确率 {accuracy:.2%} 低于阈值 {self.threshold:.2%}",
                RiskLevel.MEDIUM
            )
        return (True, f"事实准确率 {accuracy:.2%}", RiskLevel.LOW)
```

## 三、解决方案框架：V 型影响画布

面对这些挑战，我们提出了 **V-Impact Canvas** 框架，通过三层结构系统性地解决融合问题。

```
                    ┌─────────────────────────────────┐
                    │      架构意图层 (Intent)         │
                    │   不可妥协的原则与伦理约束        │
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │      设计治理层 (Governance)     │
                    │   智能体自主性与风险控制的平衡     │
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │    影响与价值层 (Impact & Value)  │
                    │   AI 决策质量与业务收益量化       │
                    └─────────────────────────────────┘
```

### 3.1 架构意图层：定义不变量

这一层回答：**什么是绝对不能妥协的。**

```yaml
# architecture_intent.yaml
intent:
  name: "智能客服系统架构意图"
  version: "1.0.0"
  
  # 不可妥协原则
  invariant_principles:
    - id: "PRIVACY_001"
      name: "用户隐私保护"
      description: "绝不向第三方传输或存储用户原始对话内容"
      enforcement: "hard_block"  # 硬性阻断
      
    - id: "SAFETY_001"
      name: "内容安全底线"
      description: "禁止生成违法、有害、误导性内容"
      enforcement: "hard_block"
      exceptions: []  # 无例外
      
    - id: "ACCURACY_001"
      name: "关键信息准确性"
      description: "价格、库存、政策等关键信息必须准确"
      enforcement: "soft_gate"  # 软性关卡
      exceptions:
        - "创意性回复场景"
        - "闲聊场景"

  # 伦理约束
  ethical_constraints:
    - id: "ETH_001"
      name: "公平性约束"
      description: "不得基于用户特征进行歧视性响应"
      monitoring: "continuous"
      remediation: "automatic_retrain"
      
    - id: "ETH_002"
      name: "透明性约束"
      description: "用户有权知道他们在与 AI 交互"
      implementation: "explicit_disclosure"

  # 质量底线
  quality_floor:
    response_relevance: 0.8  # 相关性最低 80%
    factual_accuracy: 0.9    # 事实准确率最低 90%
    user_satisfaction: 0.75   # 用户满意度最低 75%
```

### 3.2 设计治理层：动态平衡

这一层回答：**如何在保持安全的前提下，最大化智能体的自主性。**

```python
@dataclass
class AgentAutonomyLevel:
    """智能体自主性等级"""
    level: int  # 1-5, 1最保守，5最自主
    
    # 各维度的权限
    can_search_web: bool
    can_execute_code: bool
    can_access_external_api: bool
    can_make_decisions: bool
    requires_human_approval: bool
    
    @classmethod
    def get_levels(cls) -> Dict[int, 'AgentAutonomyLevel']:
        return {
            1: cls(1, False, False, False, False, True),   # 仅回答
            2: cls(2, True, False, False, False, True),     # 可搜索
            3: cls(3, True, True, False, True, True),        # 可执行代码
            4: cls(4, True, True, True, True, True),         # 可调用 API
            5: cls(5, True, True, True, True, False),        # 完全自主
        }

class AdaptiveGovernanceController:
    """自适应治理控制器"""
    
    def __init__(self):
        self.current_autonomy = AgentAutonomyLevel.get_levels()[2]
        self.performance_history = []
        self.incident_history = []
        
    def adjust_autonomy(self, metrics: Dict[str, float]) -> int:
        """根据性能指标动态调整自主性"""
        # 计算综合得分
        quality_score = metrics.get("quality_score", 0.8)
        safety_score = metrics.get("safety_score", 1.0)
        efficiency_score = metrics.get("efficiency_score", 0.7)
        
        composite = (quality_score * 0.4 + 
                     safety_score * 0.4 + 
                     efficiency_score * 0.2)
        
        # 根据得分调整等级
        if composite >= 0.9 and safety_score == 1.0:
            new_level = min(self.current_autonomy.level + 1, 5)
        elif composite < 0.7 or safety_score < 0.9:
            new_level = max(self.current_autonomy.level - 1, 1)
        else:
            new_level = self.current_autonomy.level
            
        # 检查最近是否有安全事件
        if self._has_recent_incidents():
            new_level = max(1, new_level - 1)
            
        self.current_autonomy = AgentAutonomyLevel.get_levels()[new_level]
        return new_level
    
    def _has_recent_incidents(self, window_hours: int = 24) -> bool:
        """检查最近是否有安全事件"""
        cutoff = time.time() - window_hours * 3600
        return any(incident["timestamp"] > cutoff 
                   for incident in self.incident_history)
```

### 3.3 影响与价值层：量化收益

这一层回答：**AI 系统到底带来了多少价值。**

```python
class AIValueQuantifier:
    """AI 价值量化器"""
    
    def __init__(self):
        self.baseline_metrics = {}  # 传统系统的基线指标
        self.ai_metrics = {}         # AI 系统的指标
        
    def calculate_roi(self, period_days: int = 30) -> Dict[str, Any]:
        """计算 AI 系统的投资回报率"""
        
        # 成本维度
        ai_cost = self._calculate_ai_cost(period_days)
        baseline_cost = self._calculate_baseline_cost(period_days)
        
        # 收益维度
        efficiency_gain = self._calculate_efficiency_gain(period_days)
        quality_improvement = self._calculate_quality_improvement(period_days)
        new_value = self._calculate_new_value_enabled(period_days)
        
        # 计算 ROI
        total_benefit = efficiency_gain + quality_improvement + new_value
        cost_delta = ai_cost - baseline_cost
        
        roi = (total_benefit - cost_delta) / cost_delta * 100
        
        return {
            "roi_percentage": roi,
            "total_benefit": total_benefit,
            "cost_delta": cost_delta,
            "breakdown": {
                "efficiency_gain": efficiency_gain,
                "quality_improvement": quality_improvement,
                "new_value_enabled": new_value
            },
            "recommendations": self._generate_recommendations(roi, {
                "efficiency": efficiency_gain,
                "quality": quality_improvement,
                "new_value": new_value
            })
        }
    
    def _calculate_ai_cost(self, period_days: int) -> float:
        """计算 AI 系统运营成本"""
        return (
            self._get_token_cost(period_days) +
            self._get_infrastructure_cost(period_days) +
            self._get_human_review_cost(period_days) +
            self._get_maintenance_cost(period_days)
        )
    
    def _calculate_efficiency_gain(self, period_days: int) -> float:
        """计算效率提升收益"""
        time_saved = (
            self.baseline_metrics.get("avg_handling_time", 300) -
            self.ai_metrics.get("avg_handling_time", 150)
        )
        queries_per_day = self.ai_metrics.get("queries_per_day", 1000)
        cost_per_minute = self.ai_metrics.get("agent_cost_per_minute", 1.0)
        
        return time_saved / 60 * queries_per_day * period_days * cost_per_minute
    
    def calculate_decision_quality(self) -> Dict[str, float]:
        """量化 AI 决策质量"""
        return {
            "accuracy": self._measure_accuracy(),
            "consistency": self._measure_consistency(),
            "coverage": self._measure_coverage(),
            "latency_p95": self._measure_latency(),
            "cost_per_decision": self._measure_cost_efficiency()
        }
```

## 四、实战话题：Token 与上下文经济学

### 4.1 问题本质

上下文窗口是 AI 系统最稀缺的资源：

```
上下文窗口 = 固定容量
需要装入 = 系统提示词 + 任务指令 + 检索文档 + 对话历史 + 用户输入 + 输出预留
```

就像在固定大小的背包中装东西，每一寸空间都精打细算。

### 4.2 Token 经济学模型

```python
from dataclasses import dataclass
from typing import List, Tuple
import tiktoken

@dataclass
class TokenBudget:
    """Token 预算管理"""
    total_budget: int          # 总预算（模型上下文窗口）
    system_prompt: int         # 系统提示词
    task_instruction: int      # 任务指令
    retrieved_docs: int        # 检索文档
    conversation_history: int  # 对话历史
    user_input: int            # 用户输入
    output_reserve: int        # 输出预留
    
    @property
    def used(self) -> int:
        return (self.system_prompt + self.task_instruction + 
                self.retrieved_docs + self.conversation_history + 
                self.user_input)
    
    @property
    def remaining(self) -> int:
        return self.total_budget - self.used - self.output_reserve
    
    @property
    def utilization(self) -> float:
        return self.used / self.total_budget


class ContextEconomist:
    """上下文经济学家 - 优化 Token 分配"""
    
    def __init__(self, model_name: str = "gpt-4"):
        self.encoding = tiktoken.encoding_for_model(model_name)
        self.context_window = self._get_context_window(model_name)
        
    def count_tokens(self, text: str) -> int:
        """计算文本的 Token 数"""
        return len(self.encoding.encode(text))
    
    def optimize_allocation(self, 
                           system_prompt: str,
                           task: str,
                           user_query: str,
                           available_docs: List[str],
                           conversation_history: List[dict],
                           output_reserve: int = 1000) -> dict:
        """优化 Token 分配"""
        
        budget = TokenBudget(
            total_budget=self.context_window,
            system_prompt=self.count_tokens(system_prompt),
            task_instruction=self.count_tokens(task),
            retrieved_docs=0,  # 待优化
            conversation_history=0,  # 待优化
            user_input=self.count_tokens(user_query),
            output_reserve=output_reserve
        )
        
        # 可用于检索文档和对话历史的预算
        flexible_budget = budget.remaining
        
        # 分配策略：60% 给文档，40% 给历史
        doc_budget = int(flexible_budget * 0.6)
        history_budget = int(flexible_budget * 0.4)
        
        # 优化检索文档选择
        selected_docs = self._select_optimal_docs(
            available_docs, doc_budget, user_query
        )
        
        # 优化对话历史截断
        truncated_history = self._truncate_conversation(
            conversation_history, history_budget
        )
        
        return {
            "selected_docs": selected_docs,
            "truncated_history": truncated_history,
            "budget_allocation": {
                "system_prompt": budget.system_prompt,
                "task": budget.task_instruction,
                "docs": sum(d["tokens"] for d in selected_docs),
                "history": sum(h["tokens"] for h in truncated_history),
                "user_query": budget.user_input,
                "output_reserve": output_reserve,
                "total_used": budget.used + 
                              sum(d["tokens"] for d in selected_docs) +
                              sum(h["tokens"] for h in truncated_history),
                "utilization": budget.utilization
            }
        }
    
    def _select_optimal_docs(self, 
                            docs: List[str], 
                            token_budget: int,
                            query: str) -> List[dict]:
        """选择最优文档组合（经典的背包问题）"""
        
        doc_values = []
        for i, doc in enumerate(docs):
            tokens = self.count_tokens(doc)
            # 简化的相关性分数（实际用 embedding 相似度）
            relevance = self._compute_relevance(doc, query)
            density = relevance / tokens if tokens > 0 else 0
            doc_values.append({
                "index": i,
                "content": doc,
                "tokens": tokens,
                "relevance": relevance,
                "density": density
            })
        
        # 按信息密度排序
        doc_values.sort(key=lambda x: x["density"], reverse=True)
        
        # 贪心选择
        selected = []
        total_tokens = 0
        for doc in doc_values:
            if total_tokens + doc["tokens"] <= token_budget:
                selected.append(doc)
                total_tokens += doc["tokens"]
            # 部分包含（截断文档）
            elif token_budget - total_tokens > 100:
                truncated_content = self._truncate_to_tokens(
                    doc["content"], 
                    token_budget - total_tokens
                )
                selected.append({
                    **doc,
                    "content": truncated_content,
                    "tokens": token_budget - total_tokens
                })
                break
        
        return selected
    
    def _truncate_conversation(self, 
                               history: List[dict], 
                               token_budget: int) -> List[dict]:
        """智能截断对话历史"""
        if not history:
            return []
        
        result = []
        total_tokens = 0
        
        # 逆序遍历，保留最近的对话
        for msg in reversed(history):
            msg_tokens = self.count_tokens(msg.get("content", ""))
            if total_tokens + msg_tokens <= token_budget:
                result.insert(0, msg)
                total_tokens += msg_tokens
            else:
                break
        
        return result
```

### 4.3 实战优化策略

```python
class AdvancedContextStrategy:
    """高级上下文优化策略"""
    
    def __init__(self, llm, vector_store):
        self.llm = llm
        self.vector_store = vector_store
        self.tokenizer = tiktoken.encoding_for_model("gpt-4")
        
    def progressive_context_loading(self, 
                                    query: str, 
                                    max_rounds: int = 3):
        """渐进式上下文加载：按需获取，不多不少"""
        
        context = {
            "system": self._get_minimal_system_prompt(),
            "docs": [],
            "history": []
        }
        
        for round_num in range(max_rounds):
            # 根据当前上下文生成查询扩展
            expanded_query = self._expand_query(query, context)
            
            # 动态检索
            new_docs = self.vector_store.search(
                expanded_query, 
                k=5 - len(context["docs"])
            )
            
            # 信息足够就停下
            if self._is_sufficient(query, context, new_docs):
                break
                
            context["docs"].extend(new_docs)
        
        return context
    
    def semantic_compression(self, docs: List[str]) -> str:
        """语义压缩：将多个文档压成精炼摘要"""
        
        combined = "\n\n".join(docs)
        
        compressed = self.llm.generate(
            prompt=f"""将以下信息压缩为关键要点，保持事实准确：

{combined}

压缩要点（不超过200字）："""
        )
        
        return compressed.text
    
    def query_aware_truncation(self, 
                               text: str, 
                               query: str, 
                               max_tokens: int) -> str:
        """查询感知截断：保留与查询最相关的部分"""
        
        sentences = text.split("。")
        
        # 计算每个句子与查询的相关性
        scored_sentences = []
        for sent in sentences:
            score = self._compute_relevance(sent, query)
            tokens = len(self.tokenizer.encode(sent))
            scored_sentences.append({
                "text": sent,
                "score": score,
                "tokens": tokens
            })
        
        # 按相关性排序
        scored_sentences.sort(key=lambda x: x["score"], reverse=True)
        
        # 选择高相关句子直到预算用完
        selected = []
        total_tokens = 0
        for sent in scored_sentences:
            if total_tokens + sent["tokens"] <= max_tokens:
                selected.append(sent)
                total_tokens += sent["tokens"]
        
        # 按原文顺序重新排列
        selected.sort(key=lambda x: text.index(x["text"]))
        
        return "。".join(s["text"] for s in selected)
```

## 结语：迈向融合架构

确定性系统与概率性智能的融合，不是简单的技术叠加，而是架构范式的根本性转变。我们需要：

1. **接受不确定性**：在系统设计中内置概率性思维，而非试图消除它
2. **建立可观测性**：让隐式的决策显式化，让黑盒变得透明
3. **动态治理**：从静态规则转向运行时自适应策略
4. **经济思维**：将 Token、上下文、延迟视为经济资源来优化

这不是终点，而是起点。随着 AI 技术的演进，架构模式也将持续迭代。但核心原则不变：**在不确定中寻找确定性，在概率中建立可控性**。

---

*本文是 AI 架构实践的阶段性总结，欢迎交流讨论。*论。*