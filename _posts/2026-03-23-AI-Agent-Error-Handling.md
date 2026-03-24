---
title: "AI Agent 错误处理实战：重试、熔断与优雅降级"
date: 2026-03-23 09:30:00 +0800
category: AI
tags: [AI-Agent, Error-Handling, Circuit-Breaker, Resilience]]
---

# AI Agent 错误处理实战：重试、熔断与优雅降级

> "Demo 能跑，生产必崩" —— 这是 AI Agent 从实验室走向生产环境最痛的一课。

## 前言

2024 年，某创业公司 6 人 Agent Team 在生产环境中遭遇"全军覆没"——所有 Agent 同时陷入无限重试循环，最终导致：
- API 费用在 2 小时内消耗了正常情况下 30 天额度
- 用户请求全部超时
- 整个系统雪崩

复盘发现，**根本原因不是 Agent 能力问题，而是错误处理缺失**。

这篇文章，聊聊 AI Agent "免疫系统"——错误处理机制。

---

## 一、为什么 Agent 在生产环境必崩？

### 1.1 脚本 vs 服务本质区别

写一个脚本，跑一次，结束。出错？重来。

但 Agent 是**服务**：
- 7x24 小时运行
- 不确定外部依赖（LLM API、工具调用、网络）
- 用户期望：稳定、可靠、可预测

| 维度 | 脚本 | Agent 服务 |
|------|------|-----------|
| 运行时长 | 一次性 | 持续运行 |
| 错误影响 | 本地，可控 | 全局，可能级联 |
| 恢复策略 | 人工重启 | 自动恢复 |
| 成本模型 | 固定 | 按调用计费（可能失控）|

### 1.2 Agent 常见的失败模式

```
┌─────────────────────────────────────────────────────────┐
│                    Agent 失败模式                        │
├─────────────────────────────────────────────────────────┤
│  1. LLM API 超时/限流/错误                               │
│  2. 工具调用失败（网络、权限、参数错误）                    │
│  3. 上下文窗口溢出                                       │
│  4. 模型幻觉导致工具参数错误                               │
│  5. 依赖服务不可用                                        │
│  6. 记忆/状态损坏                                        │
│  7. 配额耗尽                                             │
└─────────────────────────────────────────────────────────┘
```

**没有错误处理 = 一个错误可能引发无限循环，最终导致系统崩溃。**

---

## 二、重试机制：第一道防线

### 2.1 为什么需要重试？

网络请求天生不可靠：
- LLM API 可能临时过载
- 工具调用可能短暂超时
- 网络抖动

重试是最简单、最有效的恢复手段。

### 2.2 简单重试 vs 智能重试

❌ **错误示例：简单重试**

```python
# 危险！可能陷入无限循环
for _ in range(100):
    result = call_llm(prompt)
    if result.success:
        return result
```

问题：
- 固定间隔可能正好撞上服务恢复窗口
- 100 次重试可能瞬间消耗大量 API 配额
- 没有区分可重试/不可重试错误

✅ **正确示例：指数退避 + 抖动**

```python
import random
import time
import logging

logger = logging.getLogger(__name__)


class RetryableError(Exception):
    """可重试错误"""
    pass


class NonRetryableError(Exception):
    """不可重试错误"""
    pass


class MaxRetriesExceeded(Exception):
    """超过最大重试次数"""
    pass


def call_with_retry(func, max_retries=5, base_delay=1.0, max_delay=60.0):
    """
    带指数退避和抖动的重试机制
    
    Args:
        func: 要执行的函数
        max_retries: 最大重试次数
        base_delay: 基础延迟（秒）
        max_delay: 最大延迟（秒）
    
    Returns:
        函数执行结果
    
    Raises:
        MaxRetriesExceeded: 超过最大重试次数
        NonRetryableError: 不可重试错误
    """
    last_error = None
    
    for attempt in range(max_retries + 1):
        try:
            return func()
        except RetryableError as e:
            last_error = e
            
            if attempt == max_retries:
                raise MaxRetriesExceeded(
                    f"调用失败，已重试 {max_retries} 次: {e}"
                )
            
            # 指数退避: 2^attempt * base_delay
            delay = min(base_delay * (2 ** attempt), max_delay)
            
            # 抖动: 随机化 50%-150% 的延迟，避免惊群效应
            jitter = random.uniform(0.5, 1.5)
            actual_delay = delay * jitter
            
            logger.warning(
                f"重试 {attempt + 1}/{max_retries}，等待 {actual_delay:.2f}s: {e}"
            )
            time.sleep(actual_delay)
            
        except NonRetryableError as e:
            # 不可重试错误，直接抛出
            raise e
        
        except Exception as e:
            # 未知异常，包装为不可重试错误
            raise NonRetryableError(f"未知错误: {e}")
    
    raise last_error
```

### 2.3 哪些错误可以重试？

| 错误类型 | 是否重试 | 原因 |
|---------|---------|------|
| 网络超时 | ✅ | 临时性问题 |
| 429 Too Many Requests | ✅ | 需配合 Retry-After |
| 500/502/503/504 | ✅ | 服务端临时错误 |
| 401 Unauthorized | ❌ | 认证问题，重试无意义 |
| 400 Bad Request | ❌ | 请求本身有问题 |
| 内容过滤触发 | ❌ | 需要调整输入，不是重试能解决的 |

```python
def classify_error(status_code: int, error_body: dict) -> Exception:
    """分类错误类型"""
    if status_code in (408, 429) or status_code >= 500:
        return RetryableError(f"HTTP {status_code}: {error_body}")
    elif status_code in (401, 403, 400):
        return NonRetryableError(f"HTTP {status_code}: {error_body}")
    else:
        return NonRetryableError(f"Unknown error: {status_code}")
```

### 2.4 重试的最佳实践

```python
# 完整的重试配置示例
RETRY_CONFIG = {
    "max_retries": 5,           # 最大重试次数
    "base_delay": 1.0,          # 基础延迟 1 秒
    "max_delay": 60.0,          # 最大延迟 60 秒
    "jitter_range": (0.5, 1.5), # 抖动范围 50%-150%
    "retryable_status": [408, 429, 500, 502, 503, 504],
    "respect_retry_after": True, # 尊重 Retry-After 头
}
```

---

## 三、熔断器：防止级联失败

### 3.1 什么是熔断器？

熔断器模式源自电路保险丝：
- 正常状态：请求正常通过
- 失败达到阈值：熔断器"打开"，后续请求快速失败
- 一段时间后：进入"半开"状态，试探性放行
- 探测成功：恢复正常；失败：继续熔断

```
         失败率 > 阈值
    ┌─────────────────────┐
    │                     ▼
┌───┴───┐            ┌─────────┐
│ 关闭  │            │  打开   │
│(Closed)│           │ (Open)  │
└───┬───┘            └────┬────┘
    │                     │
    │     超时后进入探测     │
    │                     ▼
    │               ┌─────────┐
    │               │  半开   │
    └──────────────▶│(Half-Open)│
        探测成功     └─────────┘
```

### 3.2 熔断器实现

```python
import time
import logging
from enum import Enum
from dataclasses import dataclass, field
from threading import Lock
from typing import Callable, Any

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    CLOSED = "closed"      # 正常
    OPEN = "open"          # 熔断
    HALF_OPEN = "half_open"  # 半开（探测）


@dataclass
class CircuitStats:
    failures: int = 0
    successes: int = 0
    last_failure_time: float = 0
    state: CircuitState = CircuitState.CLOSED
    last_state_change: float = field(default_factory=time.time)


class CircuitOpenError(Exception):
    """熔断器打开错误"""
    pass


class CircuitBreaker:
    """
    熔断器实现
    
    配置参数:
        failure_threshold: 触发熔断的失败次数
        recovery_timeout: 熔断后多久进入半开状态（秒）
        half_open_max_calls: 半开状态下最多试探次数
        success_threshold: 半开状态下连续成功多少次后恢复
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        half_open_max_calls: int = 3,
        success_threshold: int = 2,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        self.success_threshold = success_threshold
        
        self.stats = CircuitStats()
        self.lock = Lock()
        self.half_open_calls = 0
    
    def call(self, func: Callable[[], Any]) -> Any:
        """通过熔断器执行函数"""
        with self.lock:
            state = self._get_state()
            
            if state == CircuitState.OPEN:
                raise CircuitOpenError("熔断器处于打开状态，请求被拒绝")
            
            if state == CircuitState.HALF_OPEN:
                if self.half_open_calls >= self.half_open_max_calls:
                    raise CircuitOpenError("半开状态下试探次数已达上限")
                self.half_open_calls += 1
        
        try:
            result = func()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _get_state(self) -> CircuitState:
        """获取当前状态（带状态转换逻辑）"""
        if self.stats.state == CircuitState.OPEN:
            # 检查是否可以进入半开状态
            if time.time() - self.stats.last_state_change >= self.recovery_timeout:
                self._transition_to(CircuitState.HALF_OPEN)
        
        return self.stats.state
    
    def _on_success(self):
        """成功回调"""
        with self.lock:
            self.stats.successes += 1
            self.stats.failures = 0  # 重置失败计数
            
            if self.stats.state == CircuitState.HALF_OPEN:
                if self.stats.successes >= self.success_threshold:
                    self._transition_to(CircuitState.CLOSED)
    
    def _on_failure(self):
        """失败回调"""
        with self.lock:
            self.stats.failures += 1
            self.stats.last_failure_time = time.time()
            
            if self.stats.state == CircuitState.HALF_OPEN:
                self._transition_to(CircuitState.OPEN)
            elif self.stats.failures >= self.failure_threshold:
                self._transition_to(CircuitState.OPEN)
    
    def _transition_to(self, new_state: CircuitState):
        """状态转换"""
        old_state = self.stats.state
        self.stats.state = new_state
        self.stats.last_state_change = time.time()
        self.stats.successes = 0
        
        if new_state == CircuitState.HALF_OPEN:
            self.half_open_calls = 0
        
        logger.info(f"熔断器状态转换: {old_state.value} → {new_state.value}")
```

### 3.3 Agent 中使用熔断器

```python
class LLMAgent:
    def __init__(self):
        # 为每个外部依赖创建独立的熔断器
        self.llm_circuit = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=60.0,
        )
        self.tool_circuits = {
            "web_search": CircuitBreaker(failure_threshold=3),
            "database": CircuitBreaker(failure_threshold=5),
            "api_client": CircuitBreaker(failure_threshold=5),
        }
    
    def call_llm(self, prompt: str) -> str:
        """调用 LLM，带熔断保护"""
        try:
            return self.llm_circuit.call(
                lambda: self._raw_llm_call(prompt)
            )
        except CircuitOpenError:
            # 熔断状态，走降级逻辑
            return self._fallback_llm_response(prompt)
    
    def call_tool(self, tool_name: str, params: dict) -> Any:
        """调用工具，带熔断保护"""
        if tool_name not in self.tool_circuits:
            raise ValueError(f"未知工具: {tool_name}")
        
        circuit = self.tool_circuits[tool_name]
        
        try:
            return circuit.call(
                lambda: self._raw_tool_call(tool_name, params)
            )
        except CircuitOpenError:
            return self._fallback_tool_response(tool_name, params)
```

---

## 四、优雅降级：兜底策略

### 4.1 为什么需要降级？

当重试失败、熔断打开时，系统不能直接"摆烂"。
用户体验需要被保护——即使功能受限，也要给出有意义的响应。

### 4.2 常见降级策略

```
┌────────────────────────────────────────────────────────┐
│                    降级策略层级                          │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Level 1: 缓存降级                                      │
│  └─ 返回最近一次成功结果                                 │
│                                                        │
│  Level 2: 简化模型                                      │
│  └─ 从 GPT-4 降级到 GPT-3.5 / 本地模型                   │
│                                                        │
│  Level 3: 功能降级                                      │
│  └─ 禁用部分工具，只保留核心能力                          │
│                                                        │
│  Level 4: 模板响应                                      │
│  └─ 返回预设的友好提示                                   │
│                                                        │
│  Level 5: 人工兜底                                      │
│  └─ 转人工客服 / 加入队列                                │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 4.3 降级实现示例

```python
import time
import logging
from dataclasses import dataclass
from typing import Optional, Any, Callable

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    result: Any
    timestamp: float
    ttl: float


class DegradationManager:
    """降级管理器"""
    
    def __init__(self, llm_client=None):
        self.cache: dict[str, CacheEntry] = {}
        self.degradation_level = 0  # 当前降级等级
        self.model_fallback_chain = [
            "gpt-4-turbo",      # 首选
            "gpt-3.5-turbo",    # 备选
            "local-llama3",     # 本地模型兜底
        ]
        self.current_model_index = 0
        self.llm_client = llm_client  # LLM 客户端实例
    
    def get_response(
        self,
        query: str,
        primary_func: Callable[[], Any],
        cache_key: Optional[str] = None,
    ) -> tuple[Any, bool]:
        """
        获取响应（带降级）
        
        Returns:
            (result, is_degraded): 结果和是否降级
        """
        # Level 1: 尝试正常调用
        try:
            result = primary_func()
            if cache_key:
                self._cache_result(cache_key, result)
            return result, False
        except Exception as e:
            logger.warning(f"主调用失败: {e}")
        
        # Level 2: 尝试缓存
        if cache_key:
            cached = self._get_cached(cache_key)
            if cached:
                logger.info(f"使用缓存结果: {cache_key}")
                return cached, True
        
        # Level 3: 尝试降级模型
        while self.current_model_index < len(self.model_fallback_chain) - 1:
            self.current_model_index += 1
            fallback_model = self.model_fallback_chain[self.current_model_index]
            try:
                logger.info(f"尝试降级模型: {fallback_model}")
                result = self._call_with_model(query, fallback_model)
                return result, True
            except Exception as e:
                logger.warning(f"降级模型 {fallback_model} 失败: {e}")
        
        # Level 4: 返回模板响应
        return self._template_response(query), True
    
    def _call_with_model(self, query: str, model: str) -> str:
        """
        使用指定模型调用 LLM
        
        Args:
            query: 用户查询
            model: 模型名称
        
        Returns:
            模型响应
        """
        if self.llm_client is None:
            raise RuntimeError("LLM 客户端未配置")
        
        # 调用 LLM 客户端，使用指定模型
        return self.llm_client.chat(
            messages=[{"role": "user", "content": query}],
            model=model,
        )
    
    def _cache_result(self, key: str, result: Any, ttl: float = 3600):
        """缓存结果"""
        self.cache[key] = CacheEntry(
            result=result,
            timestamp=time.time(),
            ttl=ttl,
        )
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """获取缓存（检查 TTL）"""
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        if time.time() - entry.timestamp > entry.ttl:
            del self.cache[key]
            return None
        
        return entry.result
    
    def _template_response(self, query: str) -> str:
        """模板响应"""
        templates = {
            "greeting": "您好！系统当前繁忙，请稍后再试。",
            "query": "抱歉，我暂时无法处理您的请求。请稍后再试，或联系人工客服。",
            "tool": "当前服务不可用，请稍后再试。",
        }
        
        # 简单的关键词匹配
        if any(word in query for word in ["你好", "您好", "hi", "hello"]):
            return templates["greeting"]
        return templates["query"]
    
    def reset(self):
        """重置降级状态（恢复正常后调用）"""
        self.current_model_index = 0
        self.degradation_level = 0
```

### 4.4 功能降级示例

```python
class AgentWithDegradation:
    """带降级的 Agent"""
    
    def __init__(self):
        self.degradation = DegradationManager()
        self.enabled_tools = {"web_search", "database", "calculator", "translator"}
        self.core_tools = {"calculator"}  # 核心工具，永不降级
    
    def process(self, query: str) -> dict:
        """处理请求"""
        result = {
            "query": query,
            "response": None,
            "tools_used": [],
            "degraded": False,
        }
        
        # 检查系统状态
        if self._should_degrade():
            result["degraded"] = True
            self._apply_degradation()
        
        # 正常处理
        response = self._process_with_tools(query)
        result["response"] = response
        result["tools_used"] = self._get_used_tools()
        
        return result
    
    def _should_degrade(self) -> bool:
        """判断是否需要降级"""
        # 根据熔断器状态、错误率等判断
        return self.degradation.degradation_level > 0
    
    def _apply_degradation(self):
        """应用降级策略"""
        if self.degradation.degradation_level >= 2:
            # 保留核心工具，禁用其他
            self.enabled_tools = self.core_tools.copy()
            logger.warning("已降级为核心功能模式")
    
    def _process_with_tools(self, query: str) -> str:
        """使用可用工具处理"""
        # ... 正常处理逻辑
        pass
```

---

## 五、工具调用容错

### 5.1 MCP 工具调用的特殊性

AI Agent 的工具调用比普通 API 调用更复杂：
1. **参数由模型生成**：可能不符合预期
2. **执行环境不确定**：工具本身可能有 bug
3. **超时难以预估**：复杂工具可能需要较长时间

### 5.2 工具调用错误分类

```python
from enum import Enum
from typing import Optional


class ToolErrorType(Enum):
    """工具错误类型"""
    TIMEOUT = "timeout"              # 执行超时
    INVALID_PARAMS = "invalid_params"  # 参数无效（模型生成错误）
    PERMISSION_DENIED = "permission"    # 权限不足
    NOT_FOUND = "not_found"            # 工具不存在
    EXECUTION_ERROR = "execution"       # 执行错误
    RATE_LIMITED = "rate_limited"       # 限流
    CIRCUIT_OPEN = "circuit_open"       # 熔断器打开


class ToolError(Exception):
    """工具调用错误"""
    def __init__(
        self,
        error_type: ToolErrorType,
        message: str,
        tool_name: str,
        params: Optional[dict] = None,
        retry_after: Optional[float] = None,
    ):
        self.error_type = error_type
        self.message = message
        self.tool_name = tool_name
        self.params = params
        self.retry_after = retry_after
        super().__init__(message)
```

### 5.3 工具执行器实现

```python
import asyncio
import logging
from typing import Any, Callable, Optional
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class ToolExecutor:
    """
    工具执行器
    
    功能:
    - 超时控制
    - 参数验证
    - 错误分类
    - 自动重试（可配置）
    """
    
    def __init__(
        self,
        default_timeout: float = 30.0,
        max_retries: int = 2,
        executor_workers: int = 4,
    ):
        self.default_timeout = default_timeout
        self.max_retries = max_retries
        self.executor = ThreadPoolExecutor(max_workers=executor_workers)
        self.circuit_breakers: dict[str, CircuitBreaker] = {}
        self._tool_registry: dict[str, Callable] = {}
    
    def register_tool(self, name: str, func: Callable):
        """注册工具函数"""
        self._tool_registry[name] = func
    
    async def execute(
        self,
        tool_name: str,
        params: dict,
        timeout: Optional[float] = None,
    ) -> Any:
        """
        执行工具调用
        
        Args:
            tool_name: 工具名称
            params: 工具参数
            timeout: 超时时间（秒）
        
        Returns:
            工具执行结果
        
        Raises:
            ToolError: 工具调用错误
        """
        timeout = timeout or self.default_timeout
        
        # 获取或创建熔断器
        if tool_name not in self.circuit_breakers:
            self.circuit_breakers[tool_name] = CircuitBreaker()
        
        circuit = self.circuit_breakers[tool_name]
        
        # 参数预校验
        validation_error = self._validate_params(tool_name, params)
        if validation_error:
            raise ToolError(
                error_type=ToolErrorType.INVALID_PARAMS,
                message=f"参数验证失败: {validation_error}",
                tool_name=tool_name,
                params=params,
            )
        
        # 带重试和熔断的执行
        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                result = await self._execute_with_timeout(
                    tool_name, params, timeout, circuit
                )
                return result
            except ToolError as e:
                if e.error_type in (ToolErrorType.INVALID_PARAMS, ToolErrorType.NOT_FOUND):
                    # 这些错误不应该重试
                    raise e
                last_error = e
                
                if attempt < self.max_retries:
                    await asyncio.sleep(self._get_backoff_delay(attempt))
        
        raise last_error
    
    async def _execute_with_timeout(
        self,
        tool_name: str,
        params: dict,
        timeout: float,
        circuit: CircuitBreaker,
    ) -> Any:
        """带超时和熔断的执行"""
        try:
            # 获取工具函数
            tool_func = self._get_tool_function(tool_name)
            
            # 通过熔断器和线程池执行
            # 使用 lambda 包装，确保参数正确传递
            def sync_execute():
                return circuit.call(lambda: tool_func(**params))
            
            loop = asyncio.get_running_loop()
            result = await asyncio.wait_for(
                loop.run_in_executor(self.executor, sync_execute),
                timeout=timeout,
            )
            return result
            
        except asyncio.TimeoutError:
            raise ToolError(
                error_type=ToolErrorType.TIMEOUT,
                message=f"工具 {tool_name} 执行超时（>{timeout}s）",
                tool_name=tool_name,
                params=params,
            )
        except CircuitOpenError:
            raise ToolError(
                error_type=ToolErrorType.CIRCUIT_OPEN,
                message=f"工具 {tool_name} 熔断器已打开",
                tool_name=tool_name,
                params=params,
            )
        except ToolError:
            raise
        except Exception as e:
            raise ToolError(
                error_type=ToolErrorType.EXECUTION_ERROR,
                message=str(e),
                tool_name=tool_name,
                params=params,
            )
    
    def _validate_params(self, tool_name: str, params: dict) -> Optional[str]:
        """参数验证"""
        # 这里可以实现 JSON Schema 验证
        # 或调用工具的 validate 方法
        if tool_name not in self._tool_registry:
            return f"工具 {tool_name} 未注册"
        return None
    
    def _get_backoff_delay(self, attempt: int) -> float:
        """计算退避延迟"""
        return min(1.0 * (2 ** attempt), 10.0)
    
    def _get_tool_function(self, tool_name: str) -> Callable:
        """获取工具函数"""
        if tool_name not in self._tool_registry:
            raise ToolError(
                error_type=ToolErrorType.NOT_FOUND,
                message=f"工具 {tool_name} 不存在",
                tool_name=tool_name,
            )
        return self._tool_registry[tool_name]
```

### 5.4 模型输出验证

```python
import json
import logging
from typing import Optional
from jsonschema import validate, ValidationError as JsonSchemaError

logger = logging.getLogger(__name__)


class ToolCallValidator:
    """工具调用验证器"""
    
    def __init__(self, tool_schemas: dict[str, dict]):
        """
        Args:
            tool_schemas: 工具的 JSON Schema 定义
        """
        self.tool_schemas = tool_schemas
    
    def validate_and_fix(
        self,
        tool_name: str,
        params: dict,
    ) -> tuple[dict, list[str]]:
        """
        验证并尝试修复参数
        
        Returns:
            (fixed_params, corrections): 修复后的参数和修正列表
        """
        if tool_name not in self.tool_schemas:
            return params, []
        
        schema = self.tool_schemas[tool_name]
        corrections = []
        fixed_params = params.copy()
        
        try:
            validate(fixed_params, schema)
        except JsonSchemaError as e:
            # 尝试自动修复常见问题
            fixed_params, corrections = self._auto_fix(
                fixed_params, schema, e
            )
            
            # 再次验证
            try:
                validate(fixed_params, schema)
            except JsonSchemaError:
                # 无法自动修复
                raise ToolError(
                    error_type=ToolErrorType.INVALID_PARAMS,
                    message=f"参数验证失败且无法自动修复: {e.message}",
                    tool_name=tool_name,
                    params=params,
                )
        
        return fixed_params, corrections
    
    def _auto_fix(
        self,
        params: dict,
        schema: dict,
        error: JsonSchemaError,
    ) -> tuple[dict, list[str]]:
        """尝试自动修复参数"""
        corrections = []
        
        # 修复类型错误
        if error.validator == "type":
            expected_type = error.validator_value
            path = list(error.absolute_path)
            
            # 尝试类型转换
            try:
                current_value = self._get_nested(params, path)
                fixed = self._convert_type(current_value, expected_type)
                self._set_nested(params, path, fixed)
                corrections.append(f"转换 {'.'.join(map(str, path))} 为 {expected_type}")
            except (ValueError, KeyError):
                pass
        
        # 修复缺失的必填字段
        if error.validator == "required":
            missing = error.validator_value
            for field in missing:
                if field not in params:
                    # 使用默认值
                    default = self._get_default(schema, field)
                    if default is not None:
                        params[field] = default
                        corrections.append(f"添加默认值 {field} = {default}")
        
        return params, corrections
    
    def _get_nested(self, data: dict, path: list) -> Any:
        """获取嵌套字典值"""
        result = data
        for key in path:
            if isinstance(result, dict):
                result = result[key]
            elif isinstance(result, list) and isinstance(key, int):
                result = result[key]
            else:
                raise KeyError(f"无法访问路径 {path}")
        return result
    
    def _set_nested(self, data: dict, path: list, value: Any):
        """设置嵌套字典值"""
        target = data
        for key in path[:-1]:
            if isinstance(target, dict):
                target = target[key]
            elif isinstance(target, list) and isinstance(key, int):
                target = target[key]
        
        last_key = path[-1]
        if isinstance(target, dict):
            target[last_key] = value
        elif isinstance(target, list) and isinstance(last_key, int):
            target[last_key] = value
    
    def _convert_type(self, value: Any, target_type: str) -> Any:
        """
        类型转换
        
        Args:
            value: 原始值
            target_type: 目标类型（JSON Schema 类型名）
        
        Returns:
            转换后的值
        
        Raises:
            ValueError: 无法转换
        """
        type_converters = {
            "string": str,
            "integer": int,
            "number": float,
            "boolean": lambda x: str(x).lower() in ("true", "1", "yes"),
            "array": lambda x: x if isinstance(x, list) else [x],
            "object": lambda x: x if isinstance(x, dict) else json.loads(x),
        }
        
        if target_type not in type_converters:
            raise ValueError(f"未知类型: {target_type}")
        
        return type_converters[target_type](value)
    
    def _get_default(self, schema: dict, field: str) -> Any:
        """从 schema 获取字段默认值"""
        properties = schema.get("properties", {})
        if field in properties:
            return properties[field].get("default")
        return None
```

---

## 六、生产实战：监控与告警

### 6.1 Prometheus 指标设计

```python
from prometheus_client import Counter, Histogram, Gauge, Enum

# 错误计数
agent_errors_total = Counter(
    "agent_errors_total",
    "Agent 错误总数",
    ["agent_id", "error_type", "severity"],
)

# 重试次数
agent_retries_total = Counter(
    "agent_retries_total",
    "Agent 重试总次数",
    ["agent_id", "operation"],
)

# 熔断器状态
circuit_breaker_state = Enum(
    "circuit_breaker_state",
    "熔断器状态",
    ["agent_id", "dependency"],
    states=["closed", "open", "half_open"],
)

# 响应时间分布
agent_response_time = Histogram(
    "agent_response_time_seconds",
    "Agent 响应时间",
    ["agent_id", "operation"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0],
)

# 当前降级等级
agent_degradation_level = Gauge(
    "agent_degradation_level",
    "当前降级等级",
    ["agent_id"],
)

# Token 消耗统计
agent_tokens_total = Counter(
    "agent_tokens_total",
    "Agent Token 消耗总数",
    ["agent_id", "model"],
)

# 工具调用统计
tool_calls_total = Counter(
    "tool_calls_total",
    "工具调用总数",
    ["tool_name", "status"],  # status: success, error, timeout
)

tool_call_duration = Histogram(
    "tool_call_duration_seconds",
    "工具调用耗时",
    ["tool_name"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0],
)
```

### 6.2 集成到 Agent

```python
import time
import logging
from typing import Any

logger = logging.getLogger(__name__)


class MonitoredAgent:
    """带监控的 Agent"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.circuit_breakers: dict[str, CircuitBreaker] = {}
        self.degradation_manager = DegradationManager()
    
    def _get_circuit(self, name: str) -> CircuitBreaker:
        """获取或创建熔断器"""
        if name not in self.circuit_breakers:
            self.circuit_breakers[name] = CircuitBreaker()
        return self.circuit_breakers[name]
    
    def call_llm(self, prompt: str) -> str:
        """调用 LLM（带监控）"""
        try:
            # 检查熔断器状态
            circuit = self._get_circuit("llm")
            circuit_state = circuit.stats.state.value
            
            # 更新熔断器状态指标
            circuit_breaker_state.labels(
                agent_id=self.agent_id,
                dependency="llm",
            ).state(circuit_state)
            
            # 执行调用
            with agent_response_time.labels(
                agent_id=self.agent_id,
                operation="llm_call",
            ).time():
                result = self._raw_llm_call(prompt)
            
            return result
            
        except RetryableError as e:
            agent_errors_total.labels(
                agent_id=self.agent_id,
                error_type="retryable",
                severity="warning",
            ).inc()
            raise
            
        except CircuitOpenError as e:
            agent_errors_total.labels(
                agent_id=self.agent_id,
                error_type="circuit_open",
                severity="critical",
            ).inc()
            # 触发降级
            return self.degradation_manager.get_response(
                prompt,
                lambda: self._fallback_llm_response(prompt),
            )
            
        except Exception as e:
            agent_errors_total.labels(
                agent_id=self.agent_id,
                error_type=type(e).__name__,
                severity="error",
            ).inc()
            raise
        
        finally:
            # 更新降级等级指标
            agent_degradation_level.labels(
                agent_id=self.agent_id,
            ).set(self.degradation_manager.degradation_level)
    
    def call_tool(self, tool_name: str, params: dict) -> Any:
        """调用工具（带监控）"""
        try:
            with tool_call_duration.labels(tool_name=tool_name).time():
                result = self._execute_tool(tool_name, params)
            
            tool_calls_total.labels(
                tool_name=tool_name,
                status="success",
            ).inc()
            
            return result
            
        except ToolError as e:
            tool_calls_total.labels(
                tool_name=tool_name,
                status=e.error_type.value,
            ).inc()
            raise
    
    def _raw_llm_call(self, prompt: str) -> str:
        """实际 LLM 调用（子类实现）"""
        raise NotImplementedError
    
    def _fallback_llm_response(self, prompt: str) -> str:
        """LLM 降级响应"""
        return "系统繁忙，请稍后重试。"
    
    def _execute_tool(self, tool_name: str, params: dict) -> Any:
        """执行工具（子类实现）"""
        raise NotImplementedError
```

### 6.3 告警规则（Prometheus + Alertmanager）

```yaml
# alerting_rules.yml
groups:
  - name: agent_alerts
    rules:
      # 错误率告警
      - alert: AgentHighErrorRate
        expr: |
          rate(agent_errors_total[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Agent {{ $labels.agent_id }} 错误率过高"
          description: "过去 5 分钟错误率: {{ $value }}/s"
      
      # 熔断器打开告警
      - alert: CircuitBreakerOpen
        expr: |
          circuit_breaker_state{state="open"} == 1
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Agent {{ $labels.agent_id }} 的 {{ $labels.dependency }} 熔断器已打开"
          description: "依赖服务可能不可用，请立即排查"
      
      # 降级告警
      - alert: AgentDegraded
        expr: |
          agent_degradation_level > 0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Agent {{ $labels.agent_id }} 处于降级模式"
          description: "当前降级等级: {{ $value }}"
      
      # 工具超时告警
      - alert: ToolHighTimeoutRate
        expr: |
          rate(tool_calls_total{status="timeout"}[5m]) > 0.05
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: "工具 {{ $labels.tool_name }} 超时率过高"
          description: "超时率: {{ $value }}/s"
      
      # 成本异常告警
      - alert: AbnormalTokenUsage
        expr: |
          increase(agent_tokens_total[1h]) > 1000000
        for: 0m
        labels:
          severity: critical
        annotations:
          summary: "Agent {{ $labels.agent_id }} Token 消耗异常"
          description: "过去 1 小时消耗: {{ $value }} tokens"
```

### 6.4 Grafana 仪表板

```json
{
  "dashboard": {
    "title": "AI Agent 监控",
    "panels": [
      {
        "title": "请求成功率",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(agent_requests_total{status=\"success\"}[5m]) / rate(agent_requests_total[5m])",
            "legendFormat": "{{ agent_id }}"
          }
        ]
      },
      {
        "title": "错误分布",
        "type": "piechart",
        "targets": [
          {
            "expr": "sum by (error_type)(rate(agent_errors_total[5m]))",
            "legendFormat": "{{ error_type }}"
          }
        ]
      },
      {
        "title": "熔断器状态",
        "type": "stat",
        "targets": [
          {
            "expr": "circuit_breaker_state",
            "legendFormat": "{{ agent_id }} - {{ dependency }}"
          }
        ]
      },
      {
        "title": "响应时间 P99",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.99, rate(agent_response_time_seconds_bucket[5m]))",
            "legendFormat": "{{ agent_id }}"
          }
        ]
      },
      {
        "title": "降级等级",
        "type": "stat",
        "targets": [
          {
            "expr": "agent_degradation_level",
            "legendFormat": "{{ agent_id }}"
          }
        ]
      },
      {
        "title": "Token 消耗趋势",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(agent_tokens_total[1h])",
            "legendFormat": "{{ agent_id }}"
          }
        ]
      }
    ]
  }
}
```

---

## 七、最佳实践总结

### 7.1 错误处理清单

```
□ 重试机制
  ├─ ✅ 指数退避
  ├─ ✅ 抖动（Jitter）
  ├─ ✅ 最大重试次数限制
  ├─ ✅ 区分可重试/不可重试错误
  └─ ✅ 尊重 Retry-After 头

□ 熔断器
  ├─ ✅ 为每个外部依赖独立配置
  ├─ ✅ 合理设置失败阈值
  ├─ ✅ 设置恢复超时
  ├─ ✅ 半开状态探测
  └─ ✅ 状态变更监控

□ 降级策略
  ├─ ✅ 多层降级方案
  ├─ ✅ 缓存最近成功结果
  ├─ ✅ 模型降级链
  ├─ ✅ 功能降级开关
  └─ ✅ 友好的降级提示

□ 工具调用
  ├─ ✅ 超时控制
  ├─ ✅ 参数验证
  ├─ ✅ 错误分类
  └─ ✅ 独立熔断器

□ 监控告警
  ├─ ✅ 错误率监控
  ├─ ✅ 熔断器状态告警
  ├─ ✅ Token 消耗监控
  ├─ ✅ 响应时间监控
  └─ ✅ 降级状态监控
```

### 7.2 配置模板

```python
# config.py
AGENT_ERROR_HANDLING_CONFIG = {
    "retry": {
        "max_retries": 5,
        "base_delay": 1.0,
        "max_delay": 60.0,
        "jitter_range": (0.5, 1.5),
        "retryable_status_codes": [408, 429, 500, 502, 503, 504],
    },
    
    "circuit_breaker": {
        "default": {
            "failure_threshold": 5,
            "recovery_timeout": 30.0,
            "half_open_max_calls": 3,
            "success_threshold": 2,
        },
        "llm": {  # LLM 特殊配置
            "failure_threshold": 10,
            "recovery_timeout": 60.0,
        },
        "tools": {  # 工具调用配置
            "failure_threshold": 3,
            "recovery_timeout": 20.0,
        },
    },
    
    "degradation": {
        "model_fallback_chain": [
            "gpt-4-turbo",
            "gpt-3.5-turbo",
            "local-llama3",
        ],
        "cache_ttl": 3600,
        "template_responses": {
            "busy": "系统当前繁忙，请稍后再试。",
            "error": "处理您的请求时出错，请稍后重试或联系客服。",
        },
    },
    
    "tool_executor": {
        "default_timeout": 30.0,
        "max_retries": 2,
        "executor_workers": 4,
    },
    
    "monitoring": {
        "metrics_enabled": True,
        "metrics_port": 9090,
        "error_rate_alert_threshold": 0.1,
        "cost_alert_threshold": 1000000,  # tokens/hour
    },
}
```

---

## 八、结语

AI Agent 的错误处理不是"锦上添花"，而是"生死攸关"。

**记住这个公式：**

```
生产可用 Agent = 智能能力 × 可靠性

其中：
  智能能力 = 模型 × Prompt × 工具
  可靠性 = 重试 × 熔断 × 降级 × 监控
```

没有错误处理的 Agent，就像一辆没有刹车的跑车——
性能再好，也不敢上路。

---

## 参考资料

- [Circuit Breaker Pattern - Martin Fowler](https://martinfowler.com/bliki/CircuitBreaker.html)
- [Retry Pattern - Microsoft Azure](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry)
- [Google SRE Book - Handling Overload](https://sre.google/sre-book/handling-overload/)
- [OpenAI API Best Practices](https://platform.openai.com/docs/guides/error-codes)
- [Anthropic API Errors](https://docs.anthropic.com/claude/reference/errors)

---

*本文基于 OpenClaw Agent Team 的实践经验总结，感谢所有踩过的坑。*