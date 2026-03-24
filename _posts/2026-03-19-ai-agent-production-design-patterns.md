---
layout: post
title: "AI Agent生产化落地：从原型到架构的5个关键设计模式"
date: 2026-03-19
category: AI
tags: [Agent, Architecture, Production]
---

## 引言

过去两年，AI Agent 从实验室概念快速演变为企业应用的新热点。然而，许多团队在将 Agent 从 Demo 推向生产环境时，都遇到了相似的困境：原型演示时表现惊艳，上线后却问题频出——响应不稳定、成本失控、行为不可预测、调试困难。

这些问题并非 AI 技术本身的缺陷，而是传统软件工程思维与 AI 系统特性之间的认知鸿沟。本文将分享我们在多个 Agent 项目中总结的 5 个关键设计模式，帮助有 Java/数据库/Linux 基础的开发者跨越这道鸿沟。

---

## 一、确定性 vs 非确定性：传统软件架构与 AI 行为的融合挑战

### 问题本质

传统软件系统建立在确定性假设之上：相同的输入必然产生相同的输出。测试用例可以精确断言，bug 可以稳定复现。但 AI Agent 引入了非确定性——模型推理结果受温度参数、上下文顺序等多种因素影响。

这种差异给架构设计带来了根本性挑战：

```java
// 传统服务：行为完全可预测
public class OrderService {
    public Order createOrder(OrderRequest request) {
        // 相同 request → 相同 Order，100% 确定性
        validate(request);
        return repository.save(new Order(request));
    }
}

// Agent 服务：输出依赖于模型推理
public class ChatAgent {
    public Response chat(String userInput, String sessionId) {
        // 相同 userInput 可能产生不同 Response
        // 取决于历史上下文、温度参数、模型版本等
        return llmClient.generate(buildPrompt(userInput, sessionId));
    }
}
```

### 设计模式：分层确定性架构

**核心思想**：在系统边界建立确定性外壳，将非确定性封装在可控范围内。

**实践方案**：

1. **输入预处理层（确定性）**：参数校验、权限检查、内容过滤、格式标准化
2. **上下文管理层（确定性）**：会话状态管理、历史消息检索、工具绑定
3. **推理执行层（非确定性）**：LLM 调用、工具执行、结果解析
4. **输出后处理层（确定性）**：格式校验、敏感信息过滤、审计日志、降级处理

```
┌─────────────────────────────────────────────────────────────┐
│                     确定性外壳                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ 输入预处理  │→ │ 上下文管理  │→ │ 输出后处理  │         │
│  │ (确定性)    │  │ (确定性)    │  │ (确定性)    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         ↓                ↓                ↑                │
│  ┌───────────────────────────────────────────────────┐     │
│  │              推理执行层 (非确定性)                  │     │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐          │     │
│  │  │ LLM调用 │  │ 工具执行│  │ 结果解析│          │     │
│  │  └─────────┘  └─────────┘  └─────────┘          │     │
│  └───────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

**关键代码示例**：

```java
@Service
public class AgentOrchestrator {
    
    // 确定性外壳：所有异常都在边界被捕获和处理
    public AgentResult execute(AgentRequest request) {
        String traceId = UUID.randomUUID().toString();
        long startTime = System.currentTimeMillis();
        
        try {
            // Layer 1: 输入预处理（确定性）
            ValidationResult validation = inputValidator.validate(request);
            if (!validation.isValid()) {
                return AgentResult.failure(validation.getErrors());
            }
            
            // Layer 2: 上下文管理（确定性）
            AgentContext context = contextManager.buildContext(
                request.getSessionId(), 
                request.getTools()
            );
            
            // Layer 3: 推理执行（非确定性，但有重试和超时保护）
            LLMResponse response = retryTemplate.execute(ctx -> {
                return llmClient.generate(context, request.getUserInput());
            });
            
            // Layer 4: 输出后处理（确定性）
            return outputProcessor.process(response, traceId);
            
        } catch (LLMTimeoutException e) {
            return AgentResult.timeout("推理超时，请稍后重试");
        } catch (Exception e) {
            log.error("Agent execution failed, traceId={}", traceId, e);
            return AgentResult.error("系统异常，请联系管理员");
        } finally {
            metricsRecorder.record(traceId, 
                System.currentTimeMillis() - startTime);
        }
    }
}
```

---

## 二、评估体系设计：建立 Agent 的基准测试与自动化评估流程

### 为什么传统测试不够用

传统单元测试基于断言：`assertEquals(expected, actual)`。但 Agent 输出的非确定性使这种方法失效。更重要的是，Agent 的优劣往往是多维度的——准确性、相关性、安全性、响应时间、成本。

### 设计模式：多维度评估矩阵

**评估维度设计**：

| 维度 | 指标 | 评估方法 | 权重 |
|------|------|----------|------|
| 准确性 | 任务完成率 | 人工评估 / LLM-as-Judge | 40% |
| 相关性 | 回答相关度 | 语义相似度 / 人工打分 | 20% |
| 安全性 | 有害输出率 | 关键词过滤 / 分类模型 | 否决项 |
| 效率 | 平均 Token 数 / 响应时间 | 自动统计 | 20% |
| 成本 | 单次调用成本 | 自动计算 | 20% |

**自动化评估流程**：

```yaml
# evaluation-pipeline.yaml
name: Agent Evaluation Pipeline

on:
  schedule:
    - cron: '0 2 * * *'  # 每日凌晨2点
  workflow_dispatch:
    inputs:
      agent_version:
        description: 'Agent version to evaluate'

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - name: Load Test Cases
        run: |
          curl -X GET "${{ secrets.TESTCASES_API }}" \
            -o testcases.json
      
      - name: Run Agent Against Test Cases
        run: |
          python scripts/run_evaluation.py \
            --testcases testcases.json \
            --agent-version ${{ inputs.agent_version }} \
            --output results.json
      
      - name: LLM-as-Judge Evaluation
        run: |
          python scripts/llm_judge.py \
            --results results.json \
            --judge-model gpt-4o \
            --output judged_results.json
      
      - name: Generate Report
        run: |
          python scripts/generate_report.py \
            --input judged_results.json \
            --output report.md
      
      - name: Alert on Regression
        if: steps.evaluate.outputs.accuracy < 0.85
        run: |
          python scripts/send_alert.py \
            --message "Agent accuracy dropped below 85%"
```

**评估数据集构建**：

```sql
-- 评估用例表设计（PostgreSQL）
CREATE TABLE agent_eval_cases (
    id BIGSERIAL PRIMARY KEY,
    case_group VARCHAR(100),        -- 用例分组（如"订单查询"、"退款处理"）
    user_input TEXT NOT NULL,       -- 用户输入
    expected_tools JSONB,           -- 预期调用的工具
    expected_output_pattern TEXT,   -- 预期输出模式（正则或描述）
    difficulty VARCHAR(20),         -- 难度：easy/medium/hard
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 评估结果表
CREATE TABLE agent_eval_results (
    id BIGSERIAL PRIMARY KEY,
    case_id BIGINT REFERENCES agent_eval_cases(id),
    agent_version VARCHAR(50),
    actual_tools JSONB,             -- 实际调用的工具
    actual_output TEXT,             -- 实际输出
    accuracy_score DECIMAL(3,2),    -- 准确性得分
    relevance_score DECIMAL(3,2),   -- 相关性得分
    safety_violation BOOLEAN,       -- 是否违反安全规则
    token_count INT,                -- Token 消耗
    latency_ms BIGINT,              -- 响应延迟
    evaluated_at TIMESTAMP DEFAULT NOW()
);

-- 创建评估指标视图
CREATE VIEW eval_metrics AS
SELECT 
    agent_version,
    AVG(accuracy_score) as avg_accuracy,
    AVG(relevance_score) as avg_relevance,
    SUM(CASE WHEN safety_violation THEN 1 ELSE 0 END)::FLOAT / COUNT(*) as violation_rate,
    AVG(token_count) as avg_tokens,
    AVG(latency_ms) as avg_latency_ms
FROM agent_eval_results
GROUP BY agent_version;
```

---

## 三、核心架构模式：规划、工具调用与多轮交互的工程化实现

### 模式 1：ReAct（推理-行动循环）

ReAct 是最常用的 Agent 架构模式，将推理与行动交替进行：

```
用户输入 → [思考] → [行动] → [观察] → [思考] → … → 最终回答
```

**工程化实现要点**：

```java
public class ReActAgent {
    
    private static final int MAX_ITERATIONS = 10;
    private static final String THOUGHT_PROMPT = """
        你是一个智能助手。请根据用户问题和可用工具进行推理和行动。
        
        当前状态：
        - 用户问题：%s
        - 已执行步骤：%s
        - 当前观察：%s
        
        请按以下格式输出：
        思考：[分析当前情况，决定下一步]
        行动：[工具名称]
        行动输入：{"param1": "value1"}
        """;
    
    public AgentResult run(String userInput) {
        List<Step> steps = new ArrayList<>();
        String observation = "";
        
        for (int i = 0; i < MAX_ITERATIONS; i++) {
            // 1. 推理
            ThoughtResult thought = think(userInput, steps, observation);
            steps.add(new Step(StepType.THINK, thought.getContent()));
            
            // 2. 检查是否应该结束
            if (thought.shouldFinish()) {
                return AgentResult.success(thought.getFinalAnswer());
            }
            
            // 3. 执行行动
            ActionResult action = act(thought.getAction(), thought.getParams());
            steps.add(new Step(StepType.ACT, action.toString()));
            
            // 4. 观察结果
            observation = action.getResult();
            steps.add(new Step(StepType.OBSERVE, observation));
        }
        
        // 超过最大迭代次数，强制结束
        return AgentResult.failure("推理步骤过多，请简化问题");
    }
}
```

### 模式 2：工具调用标准化

**挑战**：不同 LLM 提供商的工具调用格式各异，需要统一抽象。

**解决方案**：工具调用协议层

```java
// 统一的工具定义接口
public interface AgentTool {
    String getName();
    String getDescription();
    JsonSchema getInputSchema();
    ToolResult execute(JsonNode input);
}

// 工具注册中心
@Service
public class ToolRegistry {
    
    private final Map<String, AgentTool> tools = new ConcurrentHashMap<>();
    
    public void register(AgentTool tool) {
        tools.put(tool.getName(), tool);
    }
    
    // 转换为 OpenAI 格式
    public List<OpenAITool> toOpenAIFormat() {
        return tools.values().stream()
            .map(tool -> new OpenAITool(
                "function",
                new OpenAIFunction(
                    tool.getName(),
                    tool.getDescription(),
                    tool.getInputSchema()
                )
            ))
            .collect(Collectors.toList());
    }
    
    // 转换为 Anthropic 格式
    public List<AnthropicTool> toAnthropicFormat() {
        return tools.values().stream()
            .map(tool -> new AnthropicTool(
                tool.getName(),
                tool.getDescription(),
                tool.getInputSchema()
            ))
            .collect(Collectors.toList());
    }
}

// 工具执行器（带超时和错误处理）
// 需要 spring-retry 依赖和 @EnableRetry 注解
@Service
public class ToolExecutor {
    
    @Retryable(maxAttempts = 3, backoff = @Backoff(delay = 1000))
    @Timeout(value = 30, unit = TimeUnit.SECONDS)
    public ToolResult execute(String toolName, JsonNode params) {
        AgentTool tool = toolRegistry.get(toolName);
        if (tool == null) {
            return ToolResult.error("工具不存在: " + toolName);
        }
        
        // 参数校验
        ValidationResult validation = validateParams(tool, params);
        if (!validation.isValid()) {
            return ToolResult.error("参数校验失败: " + validation.getErrors());
        }
        
        try {
            return tool.execute(params);
        } catch (Exception e) {
            log.error("工具执行失败: {}", toolName, e);
            return ToolResult.error("执行异常: " + e.getMessage());
        }
    }
}
```

### 模式 3：多轮对话状态管理

**核心挑战**：如何在无状态服务中管理有状态的对话。

**解决方案**：会话状态外置 + 版本控制

```java
@Service
public class ConversationManager {
    
    private final RedisTemplate<String, ConversationState> redisTemplate;
    private static final long CONVERSATION_TTL = 24 * 60 * 60; // 24小时
    
    public ConversationState getState(String sessionId) {
        String key = "conversation:" + sessionId;
        ConversationState state = redisTemplate.opsForValue().get(key);
        
        if (state == null) {
            state = new ConversationState(sessionId);
        }
        
        return state;
    }
    
    public void saveState(String sessionId, ConversationState state) {
        String key = "conversation:" + sessionId;
        
        // 版本控制，防止并发冲突
        state.incrementVersion();
        redisTemplate.opsForValue().set(key, state, 
            CONVERSATION_TTL, TimeUnit.SECONDS);
    }
    
    // 使用乐观锁更新（基于 Redis Lua 脚本实现 CAS）
    public boolean updateWithOptimisticLock(
        String sessionId, 
        Function<ConversationState, ConversationState> updater
    ) {
        int maxRetries = 3;
        String key = "conversation:" + sessionId;
        
        for (int i = 0; i < maxRetries; i++) {
            ConversationState current = getState(sessionId);
            int currentVersion = current.getVersion();
            ConversationState updated = updater.apply(current);
            updated.setVersion(currentVersion + 1);
            
            // 使用 Lua 脚本实现原子性 CAS 操作
            String luaScript = """
                if redis.call('GET', KEYS[1]) == ARGV[1] then
                    redis.call('SET', KEYS[1], ARGV[2], 'EX', ARGV[3])
                    return 1
                else
                    return 0
                end
                """;
            
            Long result = redisTemplate.execute(
                new DefaultRedisScript<>(luaScript, Long.class),
                List.of(key + ":version"),
                String.valueOf(currentVersion),
                objectMapper.writeValueAsString(updated),
                String.valueOf(CONVERSATION_TTL)
            );
            
            if (result != null && result == 1) {
                return true;
            }
            // 版本冲突，重试
        }
        return false;
    }
}

// 会话状态设计
@Data
public class ConversationState {
    private String sessionId;
    private List<Message> messages;      // 对话历史
    private Map<String, Object> context; // 上下文变量
    private List<ToolCall> pendingTools;  // 待执行的工具调用
    private int version;                  // 版本号
    private Instant createdAt;
    private Instant updatedAt;
}
```

---

## 四、信任与治理：生产环境中 AI 行为的管理与控制机制

### 信任体系的三道防线

```
┌─────────────────────────────────────────────────────────────┐
│                    第一道防线：输入治理                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Prompt注入 │  │  敏感信息   │  │  权限校验   │         │
│  │   检测      │  │   过滤      │  │             │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    第二道防线：过程控制                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  工具调用   │  │  输出生成   │  │  资源消耗   │         │
│  │  白名单     │  │  温度控制   │  │  限额       │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    第三道防线：输出审计                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  内容安全   │  │  格式校验   │  │  审计日志   │         │
│  │  检测       │  │             │  │             │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### 输入治理实现

```java
@Service
public class InputGovernance {
    
    private final List<InputFilter> filters;
    
    @PostConstruct
    public void init() {
        filters = List.of(
            new PromptInjectionFilter(),    // Prompt 注入检测
            new SensitiveDataFilter(),      // 敏感信息过滤
            new RateLimitFilter(),          // 频率限制
            new PermissionFilter()          // 权限校验
        );
    }
    
    public GovernanceResult validate(AgentRequest request) {
        List<String> violations = new ArrayList<>();
        
        for (InputFilter filter : filters) {
            FilterResult result = filter.filter(request);
            if (!result.isAllowed()) {
                violations.addAll(result.getViolations());
            }
        }
        
        if (!violations.isEmpty()) {
            return GovernanceResult.rejected(violations);
        }
        
        return GovernanceResult.approved();
    }
}

// Prompt 注入检测器
@Component
public class PromptInjectionFilter implements InputFilter {
    
    private static final List<Pattern> INJECTION_PATTERNS = List.of(
        Pattern.compile("ignore previous instructions", Pattern.CASE_INSENSITIVE),
        Pattern.compile("forget your role", Pattern.CASE_INSENSITIVE),
        Pattern.compile("you are now", Pattern.CASE_INSENSITIVE),
        Pattern.compile("system:\\s*you", Pattern.CASE_INSENSITIVE)
    );
    
    @Override
    public FilterResult filter(AgentRequest request) {
        String input = request.getUserInput();
        
        for (Pattern pattern : INJECTION_PATTERNS) {
            if (pattern.matcher(input).find()) {
                return FilterResult.rejected(
                    "检测到潜在的 Prompt 注入攻击");
            }
        }
        
        return FilterResult.approved();
    }
}
```

### 输出审计实现

```java
@Service
public class OutputAudit {
    
    private final ContentSafetyClient safetyClient;
    private final AuditLogRepository auditRepo;
    
    public AuditResult audit(AgentResponse response, String sessionId) {
        // 1. 内容安全检测
        SafetyResult safety = safetyClient.analyze(response.getContent());
        if (safety.isHarmful()) {
            log.warn("Harmful content detected, session={}, categories={}", 
                sessionId, safety.getCategories());
            return AuditResult.rejected("内容安全检测未通过");
        }
        
        // 2. 格式校验
        if (response.getExpectedFormat() != null) {
            ValidationResult format = validateFormat(
                response.getContent(), 
                response.getExpectedFormat()
            );
            if (!format.isValid()) {
                return AuditResult.rejected("输出格式不符合预期");
            }
        }
        
        // 3. 记录审计日志
        AuditLog log = AuditLog.builder()
            .sessionId(sessionId)
            .userInput(response.getRequest().getUserInput())
            .modelOutput(response.getContent())
            .toolCalls(response.getToolCalls())
            .tokenUsage(response.getTokens())
            .safetyCategories(safety.getCategories())
            .timestamp(Instant.now())
            .build();
        
        auditRepo.save(log);
        
        return AuditResult.approved();
    }
}
```

### 速率限制与成本控制

```java
// 需要依赖：com.google.guava:guava 或 io.github.resilience4j:resilience4j-ratelimiter
@Configuration
public class RateLimitConfig {
    
    @Bean
    public RateLimiter agentRateLimiter() {
        return RateLimiter.create(100.0); // 每秒100个请求
    }
    
    @Bean
    public TokenBucket tokenBucket() {
        return TokenBucket.builder()
            .capacity(1000000)          // 每日100万Token
            .refillRate(10000)          // 每小时补充1万
            .build();
    }
}

@Service
public class CostController {
    
    private final TokenBucket tokenBucket;
    private final UserQuotaRepository quotaRepo;
    
    public CostResult checkAndConsume(String userId, int estimatedTokens) {
        // 1. 检查用户配额
        UserQuota quota = quotaRepo.findByUserId(userId);
        if (quota.getRemainingTokens() < estimatedTokens) {
            return CostResult.exceeded("用户配额不足");
        }
        
        // 2. 检查全局配额
        if (!tokenBucket.tryConsume(estimatedTokens)) {
            return CostResult.exceeded("系统繁忙，请稍后重试");
        }
        
        // 3. 扣减用户配额
        quotaRepo.decrementTokens(userId, estimatedTokens);
        
        return CostResult.approved();
    }
}
```

---

## 五、实战经验：从 Demo 到上线的常见问题与解决方案

### 坑 1：上下文窗口膨胀

**问题**：多轮对话中，历史消息累积导致 Token 数量急剧增长。

**解决方案**：滑动窗口 + 关键信息提取

```java
@Service
public class ContextCompressor {
    
    private static final int MAX_CONTEXT_TOKENS = 4000;
    
    public List<Message> compress(List<Message> history) {
        int totalTokens = estimateTokens(history);
        
        if (totalTokens <= MAX_CONTEXT_TOKENS) {
            return history;
        }
        
        // 策略1：保留最近N轮对话
        List<Message> recentMessages = keepRecent(history, 5);
        
        // 策略2：提取关键信息作为摘要
        String summary = extractKeyInfo(history);
        
        // 策略3：重组上下文
        List<Message> compressed = new ArrayList<>();
        compressed.add(new Message("system", "之前的对话摘要：" + summary));
        compressed.addAll(recentMessages);
        
        return compressed;
    }
    
    private String extractKeyInfo(List<Message> history) {
        // 使用 LLM 提取关键信息
        String prompt = "请从以下对话中提取关键信息（实体、决策、结论）：\n\n" +
            formatHistory(history);
        return llmClient.summarize(prompt);
    }
}
```

### 坑 2：工具调用循环

**问题**：Agent 陷入工具调用的循环，无法收敛到最终答案。

**解决方案**：迭代计数器 + 进度检测

```java
@Service
public class LoopDetector {
    
    private static final int MAX_ITERATIONS = 10;
    private static final int MAX_SAME_ACTION = 3;
    
    public DetectionResult detect(List<Step> steps) {
        // 1. 检查总迭代次数
        if (steps.size() >= MAX_ITERATIONS) {
            return DetectionResult.loop("达到最大迭代次数");
        }
        
        // 2. 检查是否重复相同动作
        if (steps.size() >= MAX_SAME_ACTION) {
            List<Step> recent = steps.subList(
                steps.size() - MAX_SAME_ACTION, steps.size());
            
            if (allSameAction(recent)) {
                return DetectionResult.loop("检测到重复动作");
            }
        }
        
        // 3. 检查是否无进展
        if (hasNoProgress(steps)) {
            return DetectionResult.loop("对话无进展");
        }
        
        return DetectionResult.ok();
    }
    
    private boolean allSameAction(List<Step> steps) {
        return steps.stream()
            .map(s -> s.getAction() + ":" + s.getParams())
            .distinct()
            .count() == 1;
    }
}
```

### 坑 3：模型幻觉导致工具调用失败

**问题**：模型生成了不存在的工具名或参数格式错误。

**解决方案**：严格的工具调用校验

```java
@Service
public class ToolCallValidator {
    
    private final ToolRegistry toolRegistry;
    private final ObjectMapper objectMapper;
    
    public ValidationResult validate(ToolCall toolCall) {
        // 1. 工具存在性检查
        AgentTool tool = toolRegistry.get(toolCall.getName());
        if (tool == null) {
            // 尝试模糊匹配
            String suggestion = findSimilarTool(toolCall.getName());
            return ValidationResult.error(
                "工具不存在: " + toolCall.getName() + 
                "，您是否想调用: " + suggestion);
        }
        
        // 2. 参数格式检查
        JsonSchema schema = tool.getInputSchema();
        JsonNode params;
        try {
            params = objectMapper.readTree(toolCall.getArguments());
            Set<ValidationMessage> errors = schema.validate(params);
            
            if (!errors.isEmpty()) {
                return ValidationResult.error(
                    "参数格式错误: " + formatErrors(errors));
            }
        } catch (JsonProcessingException e) {
            return ValidationResult.error("参数 JSON 解析失败");
        }
        
        // 3. 必填参数检查
        for (String required : schema.getRequired()) {
            if (!params.has(required)) {
                return ValidationResult.error(
                    "缺少必填参数: " + required);
            }
        }
        
        return ValidationResult.ok();
    }
}
```

### 坑 4：生产环境调试困难

**问题**：Agent 行为具有不可预测性，生产环境问题难以复现。

**解决方案**：全链路追踪 + 结构化日志

```java
@Aspect
@Component
public class AgentTracingAspect {
    
    private final Tracer tracer;
    private final AuditLogRepository auditRepo;
    
    @Around("@annotation(AgentExecution)")
    public Object traceAgentExecution(ProceedingJoinPoint pjp) throws Throwable {
        Span span = tracer.spanBuilder("agent.execution")
            .setAttribute("session.id", getSessionId())
            .startSpan();
        
        try (Scope scope = span.makeCurrent()) {
            // 记录输入
            span.setAttribute("user.input", getUserInput());
            
            Object result = pjp.proceed();
            
            // 记录输出
            if (result instanceof AgentResult agentResult) {
                span.setAttribute("result.status", agentResult.getStatus());
                span.setAttribute("result.tokens", agentResult.getTokens());
            }
            
            return result;
            
        } catch (Exception e) {
            span.recordException(e);
            span.setStatus(StatusCode.ERROR, e.getMessage());
            throw e;
            
        } finally {
            span.end();
        }
    }
}

// 结构化日志配置
logback-spring.xml:
<appender name="AUDIT" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>logs/agent-audit.json</file>
    <encoder class="net.logstash.logback.encoder.LogstashEncoder">
        <includeMdcKeyName>traceId</includeMdcKeyName>
        <includeMdcKeyName>sessionId</includeMdcKeyName>
        <includeMdcKeyName>userId</includeMdcKeyName>
    </encoder>
</appender>
```

### 坑 5：成本失控

**问题**：上线后 Token 消耗远超预期，成本难以控制。

**解决方案**：分级服务 + 智能降级

```java
@Service
public class TieredAgentService {
    
    private final Map<String, AgentConfig> tierConfigs = Map.of(
        "premium", AgentConfig.premium(),    // GPT-4, 完整工具集
        "standard", AgentConfig.standard(), // GPT-3.5, 常用工具
        "economy", AgentConfig.economy()    // 小模型, 有限工具
    );
    
    public AgentResult execute(String userId, String input) {
        // 1. 根据用户等级选择配置
        UserTier tier = userService.getTier(userId);
        AgentConfig config = tierConfigs.get(tier.getName());
        
        // 2. 检查配额
        if (!quotaService.hasQuota(userId, tier)) {
            // 降级到更低等级
            config = tierConfigs.get("economy");
        }
        
        // 3. 执行
        return agentExecutor.execute(input, config);
    }
}

@Data
public class AgentConfig {
    private String model;              // 模型名称
    private List<String> tools;        // 可用工具
    private int maxTokens;             // 最大Token数
    private double temperature;        // 温度参数
    private int maxRetries;            // 最大重试次数
    
    public static AgentConfig premium() {
        return AgentConfig.builder()
            .model("gpt-4-turbo")
            .tools(List.of("search", "database", "api", "code"))
            .maxTokens(8000)
            .temperature(0.7)
            .maxRetries(3)
            .build();
    }
    
    public static AgentConfig economy() {
        return AgentConfig.builder()
            .model("gpt-3.5-turbo")
            .tools(List.of("search"))
            .maxTokens(2000)
            .temperature(0.3)
            .maxRetries(1)
            .build();
    }
}
```

---

## 总结

AI Agent 的生产化落地，本质上是在确定性工程体系与概率性 AI 能力之间寻找平衡。本文介绍的 5 个设计模式：

1. **分层确定性架构**：用确定性外壳封装非确定性行为
2. **多维度评估体系**：建立可量化的质量基准
3. **标准化架构模式**：ReAct、工具调用、会话管理的工程化实现
4. **信任与治理机制**：输入过滤、过程控制、输出审计的三道防线
5. **实战经验积累**：上下文压缩、循环检测、成本控制等具体方案

这些模式并非孤立存在，而是相互支撑的有机整体。确定性架构为评估提供稳定基线，评估体系为治理提供决策依据，治理机制确保系统可控，实战经验指导持续优化。

从 Demo 到生产，最大的转变不是技术本身，而是工程思维的升级——从「能跑起来」到「可控、可测、可审计、可运营」。这需要开发者在架构设计、测试策略、监控体系、成本控制等多个维度同步发力。

期待这些经验能帮助更多团队跨越 AI Agent 生产化的鸿沟。

---

*本文基于多个企业级 Agent 项目的实践经验总结，涉及智能客服、数据分析助手、代码助手等场景。如有问题或建议，欢迎交流讨论。*