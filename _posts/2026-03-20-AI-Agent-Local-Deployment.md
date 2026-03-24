---
title: "AI Agent 本地部署实战：Ollama + LangGraph 隐私优先工作流"
date: 2026-03-20 10:00:00
category: AI
tags: [Agent, Ollama, LangGraph, Local-Deployment, RAG, Docker]
author: Liu AJ
excerpt: "2026 年数据隐私要求日益严格，企业面临公有云 AI 数据泄露风险。本文详解如何使用 Ollama + LangGraph 搭建 100% 本地化 AI Agent，实现零数据出境、零 API 成本、完全可控的隐私优先工作流。"
---

## 1. 引言：为什么需要本地部署 AI Agent？

### 1.1 云端 AI 的三大风险

随着 AI 技术的广泛应用，越来越多的企业和个人开始依赖云端 AI 服务。然而，这种依赖带来了不容忽视的风险：

| 风险类型 | 具体表现 | 潜在后果 |
|----------|----------|----------|
| **数据泄露** | 敏感信息上传第三方服务器 | 商业机密外泄、客户隐私暴露 |
| **合规风险** | 数据跨境传输违反监管要求 | GDPR 罚款、网络安全法违规 |
| **成本失控** | API 调用费用随业务规模增长 | 预算超支、难以预测成本 |

### 1.2 本地部署的核心优势

相比云端方案，本地部署提供了独特价值：

- **数据 100% 本地化**：所有敏感数据始终留在本地环境，杜绝数据出境风险
- **零 API 成本**：无需为每次调用付费，长期使用成本更低
- **完全可控**：模型选择、参数调优、数据存储全由自己掌控
- **离线可用**：不依赖网络连接，适合内网环境或偏远地区

### 1.3 本文目标读者

本文适合以下人群：

- 企业 IT 负责人：希望搭建私有 AI 基础设施
- 合规负责人：需要满足数据本地化监管要求
- 隐私敏感行业从业者：医疗、金融、法律等领域
- 个人开发者：希望零成本体验 AI Agent 技术

---

## 2. 技术栈选型

### 2.1 核心组件对比

| 组件 | 选型 | 替代方案 | 选型理由 |
|------|------|----------|----------|
| 模型推理 | **Ollama** | vLLM, LocalAI | 开源免费 / 一键部署 / 多模型支持 / 社区活跃 |
| Agent 框架 | **LangGraph** | LangChain, AutoGPT | 状态管理清晰 / 工作流可视化 / 调试友好 |
| 向量数据库 | **Chroma** | Milvus, Qdrant | 轻量级 / 本地运行 / 零配置启动 |
| 文档加载 | **LangChain** | LlamaIndex | 生态丰富 / 文档加载器全面 |

### 2.2 硬件需求参考

根据模型规模和应用场景，硬件需求差异较大：

| 规模 | CPU | 内存 | 显卡 | 模型推荐 | 适用场景 |
|------|-----|------|------|----------|----------|
| **入门** | 4 核 | 16 GB | 无 | Qwen2.5-7B, Llama3.2-3B | 个人学习 / 轻量对话 |
| **标准** | 8 核 | 32 GB | RTX 3060 (12GB) | Llama3.1-8B, Qwen2.5-14B | 小团队 / 日常办公 |
| **进阶** | 16 核 | 64 GB | RTX 4090 (24GB) | Llama3.1-70B-Q4, Qwen2.5-32B | 企业级 / 高并发 |
| **服务器** | 32 核 | 128 GB | A100 (40GB) × 2 | DeepSeek-V3, Qwen-Max | 大规模部署 |

> 💡 **提示**：如果只是入门体验，8GB 内存 + 无显卡的笔记本也能运行 3B 模型，只是速度较慢。

---

## 3. 实战一：Ollama 本地部署

### 3.1 安装 Ollama

#### Linux / macOS

```bash
# 一键安装
curl -fsSL https://ollama.com/install.sh | sh

# 验证安装
ollama --version
# 输出：ollama version is 0.5.x
```

#### Windows

1. 访问 [https://ollama.com/download](https://ollama.com/download)
2. 下载 `OllamaSetup.exe`
3. 双击安装，按向导完成

#### Docker 方式（推荐用于服务器）

```bash
# 拉取镜像
docker pull ollama/ollama:latest

# 启动容器（CPU 版本）
docker run -d --name ollama \
  -v ollama_data:/root/.ollama \
  -p 11434:11434 \
  ollama/ollama:latest

# 启动容器（GPU 版本）
docker run -d --name ollama \
  --gpus all \
  -v ollama_data:/root/.ollama \
  -p 11434:11434 \
  ollama/ollama:latest
```

### 3.2 下载和运行模型

```bash
# 查看可用模型列表
ollama list

# 下载轻量模型（入门推荐）
ollama pull qwen2.5:7b

# 下载平衡模型（推荐）
ollama pull llama3.1:8b

# 下载强大模型（需要好显卡）
ollama pull llama3.1:70b

# 运行交互式对话
ollama run qwen2.5:7b

# 运行时指定参数
ollama run qwen2.5:7b --num-ctx 8192 --temperature 0.7
```

### 3.3 测试 API 接口

Ollama 默认在 `http://localhost:11434` 提供 REST API：

```bash
# 测试连接
curl http://localhost:11434/api/tags

# 发送生成请求
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:7b",
  "prompt": "请用一句话介绍 Python 语言",
  "stream": false
}'

# 发送对话请求
curl http://localhost:11434/api/chat -d '{
  "model": "qwen2.5:7b",
  "messages": [
    {"role": "user", "content": "你好，请介绍一下自己"}
  ],
  "stream": false
}'
```

### 3.4 常用配置参数

| 参数 | 说明 | 默认值 | 推荐值 |
|------|------|--------|--------|
| `num_ctx` | 上下文窗口大小 | 2048 | 4096-8192 |
| `temperature` | 生成随机性 | 0.8 | 0.7 |
| `top_p` | 核采样参数 | 0.9 | 0.9 |
| `num_gpu` | GPU 层数 | -1 (自动) | 按显卡调整 |
| `num_thread` | CPU 线程数 | 自动 | CPU 核心数 |

---

## 4. 实战二：LangGraph Agent 搭建

### 4.1 环境搭建

```bash
# 创建项目目录
mkdir ai-agent-local && cd ai-agent-local

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装核心依赖
pip install langgraph langchain-community langchain-ollama

# 安装向量数据库
pip install chromadb langchain-chroma

# 安装工具库
pip install python-dotenv pydantic
```

创建 `requirements.txt`：

```text
langgraph>=0.2.0
langchain-community>=0.3.0
langchain-ollama>=0.2.0
chromadb>=0.5.0
langchain-chroma>=0.1.0
python-dotenv>=1.0.0
pydantic>=2.0.0
```

### 4.2 基础 Agent 实现

创建 `simple_agent.py`：

```python
"""
简单对话 Agent 示例
演示 LangGraph 状态管理和工作流编排
"""
from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama

# 定义状态结构
class AgentState(TypedDict):
    """Agent 状态定义"""
    messages: Annotated[list, add]  # 消息历史，使用 add 操作符合并
    next_action: str  # 下一步行动

# 初始化本地模型
llm = ChatOllama(
    model="qwen2.5:7b",
    base_url="http://localhost:11434",
    temperature=0.7
)

def agent_node(state: AgentState) -> dict:
    """
    Agent 主节点：调用 LLM 生成回复
    """
    messages = state["messages"]
    
    # 调用本地模型
    response = llm.invoke(messages)
    
    # 检查是否需要结束（简单判断）
    should_end = "再见" in response.content or "bye" in response.content.lower()
    
    return {
        "messages": [response],
        "next_action": "end" if should_end else "continue"
    }

def end_node(state: AgentState) -> dict:
    """结束节点"""
    return {"next_action": "end"}

# 构建工作流图
def build_graph():
    workflow = StateGraph(AgentState)
    
    # 添加节点
    workflow.add_node("agent", agent_node)
    workflow.add_node("end", end_node)
    
    # 设置入口
    workflow.set_entry_point("agent")
    
    # 添加条件边
    workflow.add_conditional_edges(
        "agent",
        lambda state: state["next_action"],
        {
            "continue": "agent",  # 继续对话
            "end": "end"  # 结束
        }
    )
    
    return workflow.compile()

# 主程序
def main():
    print("=" * 50)
    print("本地 AI Agent - 输入 'quit' 退出")
    print("=" * 50)
    
    app = build_graph()
    
    # 初始化状态
    state = {
        "messages": [],
        "next_action": "continue"
    }
    
    while True:
        # 获取用户输入
        user_input = input("\n你: ").strip()
        
        if user_input.lower() == "quit":
            print("再见！")
            break
        
        # 添加用户消息
        state["messages"].append({"role": "user", "content": user_input})
        
        # 运行 Agent
        result = app.invoke(state)
        state = result
        
        # 输出回复
        last_message = result["messages"][-1]
        print(f"\nAgent: {last_message.content}")

if __name__ == "__main__":
    main()
```

运行测试：

```bash
python simple_agent.py
```

### 4.3 Agent 工作流可视化

LangGraph 支持生成工作流图：

```python
from IPython.display import Image, display

# 获取工作流图
graph = build_graph()
graph_image = graph.get_graph().draw_mermaid_png()

# 保存图片
with open("agent_workflow.png", "wb") as f:
    f.write(graph_image)
```

生成的流程图：

```
┌─────────┐
│ START   │
└────┬────┘
     │
     ▼
┌─────────┐
│  agent  │◄────────┐
└────┬────┘         │
     │              │
     ▼              │
┌─────────────┐     │
│ continue?   │     │
└────┬───┬────┘     │
     │   │          │
   Yes  No          │
     │   │          │
     │   ▼          │
     │  ┌───┐       │
     │  │end│       │
     │  └───┘       │
     │              │
     └──────────────┘
```

---

## 5. 实战三：RAG 知识库集成

### 5.1 为什么需要 RAG？

大语言模型存在固有局限：

| 局限 | 表现 | RAG 解决方案 |
|------|------|--------------|
| **知识过时** | 训练数据截止后的事件无法回答 | 实时检索最新文档 |
| **幻觉问题** | 编造不存在的信息 | 基于真实文档回答 |
| **私有知识缺失** | 无法回答企业内部问题 | 接入本地知识库 |

### 5.2 文档加载与处理

创建 `rag_agent.py`：

```python
"""
RAG Agent 示例
集成本地知识库，实现基于文档的问答
"""
import os
from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredFileLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# 配置
OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"
CHAT_MODEL = "qwen2.5:7b"
CHROMA_PERSIST_DIR = "./chroma_db"
DOCUMENTS_DIR = "./docs"

class RAGState(TypedDict):
    """RAG Agent 状态"""
    question: str
    context: str
    answer: str
    sources: list

class LocalRAG:
    """本地 RAG 系统"""
    
    def __init__(self):
        # 初始化嵌入模型
        self.embeddings = OllamaEmbeddings(
            model=EMBEDDING_MODEL,
            base_url=OLLAMA_BASE_URL
        )
        
        # 初始化对话模型
        self.llm = ChatOllama(
            model=CHAT_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.3  # RAG 场景降低随机性
        )
        
        # 初始化向量库
        self.vectorstore = None
        self.retriever = None
        
    def load_documents(self, docs_dir: str = DOCUMENTS_DIR):
        """加载文档"""
        print(f"📂 加载文档目录: {docs_dir}")
        
        documents = []
        
        # 加载 PDF
        for root, _, files in os.walk(docs_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if file.endswith('.pdf'):
                        loader = PyPDFLoader(file_path)
                        documents.extend(loader.load())
                    elif file.endswith('.md'):
                        loader = TextLoader(file_path, encoding='utf-8')
                        documents.extend(loader.load())
                    elif file.endswith('.txt'):
                        loader = TextLoader(file_path, encoding='utf-8')
                        documents.extend(loader.load())
                    print(f"  ✓ {file}")
                except Exception as e:
                    print(f"  ✗ {file}: {e}")
        
        print(f"📄 共加载 {len(documents)} 个文档片段")
        return documents
    
    def split_documents(self, documents, chunk_size=1000, chunk_overlap=200):
        """文档分块"""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", "。", "！", "？", " ", ""]
        )
        
        chunks = splitter.split_documents(documents)
        print(f"✂️ 分割为 {len(chunks)} 个文本块")
        return chunks
    
    def build_vectorstore(self, chunks, persist=True):
        """构建向量索引"""
        print("🔨 构建向量索引...")
        
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=CHROMA_PERSIST_DIR if persist else None
        )
        
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 4}  # 返回 top 4 相关文档
        )
        
        print(f"✅ 向量库构建完成，持久化到: {CHROMA_PERSIST_DIR}")
    
    def load_vectorstore(self):
        """加载已有向量库"""
        if os.path.exists(CHROMA_PERSIST_DIR):
            self.vectorstore = Chroma(
                persist_directory=CHROMA_PERSIST_DIR,
                embedding_function=self.embeddings
            )
            self.retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": 4}
            )
            print(f"✅ 已加载向量库: {CHROMA_PERSIST_DIR}")
            return True
        return False
    
    def query(self, question: str) -> dict:
        """查询知识库"""
        # RAG 提示词
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的知识库助手。请基于以下上下文回答问题。
            
上下文：
{context}

要求：
1. 只使用上下文中的信息回答
2. 如果上下文中没有相关信息，请明确告知
3. 回答要准确、简洁、有条理
4. 如果需要，可以引用原文"""),
            ("human", "{question}")
        ])
        
        # 检索相关文档
        docs = self.retriever.invoke(question)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # 生成回答
        chain = prompt | self.llm
        response = chain.invoke({
            "context": context,
            "question": question
        })
        
        return {
            "question": question,
            "answer": response.content,
            "sources": [doc.metadata.get("source", "未知") for doc in docs]
        }

def main():
    # 初始化 RAG 系统
    rag = LocalRAG()
    
    # 尝试加载已有向量库，否则重新构建
    if not rag.load_vectorstore():
        print("\n" + "=" * 50)
        print("首次运行，开始构建知识库...")
        print("=" * 50)
        
        # 加载文档
        documents = rag.load_documents()
        
        if not documents:
            print("❌ 未找到文档，请将文档放入 ./docs 目录")
            return
        
        # 分块
        chunks = rag.split_documents(documents)
        
        # 构建向量库
        rag.build_vectorstore(chunks)
    
    # 交互式问答
    print("\n" + "=" * 50)
    print("本地 RAG Agent - 输入 'quit' 退出")
    print("=" * 50)
    
    while True:
        question = input("\n问题: ").strip()
        
        if question.lower() == "quit":
            print("再见！")
            break
        
        if not question:
            continue
        
        # 查询
        result = rag.query(question)
        
        print(f"\n回答: {result['answer']}")
        print(f"\n来源: {', '.join(set(result['sources']))}")

if __name__ == "__main__":
    main()
```

### 5.3 使用示例

准备文档目录：

```bash
mkdir -p docs
# 将 PDF、Markdown、TXT 文件放入 docs 目录
```

运行 RAG Agent：

```bash
python rag_agent.py
```

交互示例：

```
问题: 请介绍一下公司的请假制度

回答: 根据公司《员工手册》第 3 章的规定，请假制度如下：

1. 年假：入职满 1 年后可享受 5 天带薪年假，满 5 年后增加至 10 天
2. 病假：需提供医院证明，每年累计不超过 30 天
3. 事假：需提前 3 天申请，经部门主管批准

来源: docs/员工手册.pdf, docs/请假制度.md
```

---

## 6. 实战四：企业级部署

### 6.1 Docker 容器化

创建 `Dockerfile`：

```dockerfile
# AI Agent 本地部署 Dockerfile
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 设置环境变量
ENV OLLAMA_BASE_URL=http://ollama:11434
ENV PYTHONUNBUFFERED=1

# 启动命令
CMD ["python", "main.py"]
```

### 6.2 Docker Compose 编排

创建 `docker-compose.yml`：

```yaml
# Docker Compose V2 格式（无需 version 字段）
services:
  # Ollama 模型服务
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_ORIGINS=*  # 允许跨域
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3

  # AI Agent 应用
  agent:
    build: .
    container_name: ai-agent
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - MODEL_NAME=qwen2.5:7b
      - CHROMA_PERSIST_DIR=/app/chroma_db
    volumes:
      - ./docs:/app/docs
      - chroma_data:/app/chroma_db
    depends_on:
      ollama:
        condition: service_healthy
    restart: unless-stopped

  # Nginx 反向代理（可选）
  nginx:
    image: nginx:alpine
    container_name: nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - agent
    restart: unless-stopped

volumes:
  ollama_data:
  chroma_data:

networks:
  default:
    name: ai-network
```

### 6.3 Nginx 反向代理配置

创建 `nginx.conf`：

```nginx
events {
    worker_connections 1024;
}

http {
    upstream agent_backend {
        server agent:8000;
    }

    upstream ollama_backend {
        server ollama:11434;
    }

    # HTTP 重定向到 HTTPS
    server {
        listen 80;
        server_name ai.internal.company.com;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS 配置
    server {
        listen 443 ssl;
        server_name ai.internal.company.com;

        # SSL 证书
        ssl_certificate /etc/nginx/ssl/ai.crt;
        ssl_certificate_key /etc/nginx/ssl/ai.key;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;

        # 客户端证书验证（可选，增强安全性）
        # ssl_client_certificate /etc/nginx/ssl/ca.crt;
        # ssl_verify_client on;

        # Agent API
        location /api/ {
            proxy_pass http://agent_backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # 超时配置
            proxy_connect_timeout 60s;
            proxy_send_timeout 300s;
            proxy_read_timeout 300s;
        }

        # Ollama API（仅限内网访问）
        location /ollama/ {
            # IP 白名单
            allow 192.168.0.0/16;
            allow 10.0.0.0/8;
            deny all;

            proxy_pass http://ollama_backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # 健康检查
        location /health {
            access_log off;
            return 200 "OK\n";
            add_header Content-Type text/plain;
        }
    }
}
```

### 6.4 网络安全配置

#### 防火墙配置（Linux）

```bash
# 仅允许内网访问 Ollama API
iptables -A INPUT -p tcp --dport 11434 -s 192.168.0.0/16 -j ACCEPT
iptables -A INPUT -p tcp --dport 11434 -s 10.0.0.0/8 -j ACCEPT
iptables -A INPUT -p tcp --dport 11434 -j DROP

# 保存规则
iptables-save > /etc/iptables/rules.v4
```

#### Ollama 服务配置

创建 `~/.ollama/env`：

```bash
# 只监听本地
OLLAMA_HOST=127.0.0.1:11434

# 或监听内网
OLLAMA_HOST=192.168.1.100:11434

# 并发设置
OLLAMA_NUM_PARALLEL=4
OLLAMA_MAX_LOADED_MODELS=2
```

---

## 7. 生产环境最佳实践

### 7.1 性能优化策略

| 优化项 | 方法 | 效果 |
|--------|------|------|
| **模型量化** | 使用 4bit/8bit 量化版本 | 显存减少 50-75% |
| **批量推理** | 合并多个请求处理 | 吞吐提升 2-3 倍 |
| **缓存策略** | 缓存常见问答结果 | 减少 70% 重复计算 |
| **异步处理** | 使用消息队列解耦 | 提升系统并发能力 |

#### 模型量化示例

```bash
# 使用量化模型
ollama pull qwen2.5:7b-q4_0  # 4bit 量化

# 或在 API 中指定
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:7b",
  "prompt": "你好",
  "options": {
    "num_gpu": 1,
    "num_thread": 8
  }
}'
```

### 7.2 监控与日志

创建 `monitoring.py`：

```python
"""
AI Agent 监控模块
集成 Prometheus 指标
"""
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
from functools import wraps

# 定义指标
REQUEST_COUNT = Counter(
    'agent_requests_total',
    'Total agent requests',
    ['model', 'status']
)

REQUEST_LATENCY = Histogram(
    'agent_request_latency_seconds',
    'Agent request latency',
    ['model'],
    buckets=[0.1, 0.5, 1, 2, 5, 10, 30, 60]
)

TOKEN_COUNT = Counter(
    'agent_tokens_total',
    'Total tokens processed',
    ['model', 'type']  # type: input/output
)

ACTIVE_REQUESTS = Gauge(
    'agent_active_requests',
    'Number of active requests'
)

# 装饰器
def track_request(model_name):
    """请求追踪装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ACTIVE_REQUESTS.inc()
            start_time = time.time()
            status = 'success'
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                status = 'error'
                raise
            finally:
                latency = time.time() - start_time
                REQUEST_COUNT.labels(model=model_name, status=status).inc()
                REQUEST_LATENCY.labels(model=model_name).observe(latency)
                ACTIVE_REQUESTS.dec()
        return wrapper
    return decorator

# 启动监控服务器
def start_monitoring(port=9090):
    """启动 Prometheus 指标服务器"""
    start_http_server(port)
    print(f"📊 监控服务启动: http://localhost:{port}/metrics")
```

### 7.3 健康检查与自动恢复

```python
"""
健康检查模块
"""
import asyncio
import httpx
from datetime import datetime

class HealthChecker:
    def __init__(self, ollama_url: str):
        self.ollama_url = ollama_url
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def check_ollama(self) -> dict:
        """检查 Ollama 服务状态"""
        try:
            response = await self.client.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                return {
                    "status": "healthy",
                    "models": [m["name"] for m in models],
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def check_all(self) -> dict:
        """执行所有健康检查"""
        ollama = await self.check_ollama()
        return {
            "ollama": ollama,
            "overall": "healthy" if ollama["status"] == "healthy" else "unhealthy"
        }

# 使用示例
async def main():
    checker = HealthChecker("http://localhost:11434")
    health = await checker.check_all()
    print(health)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 8. 2026 年本地部署新趋势

### 8.1 端云混合架构

```
┌─────────────────────────────────────────────────────────┐
│                    端云混合架构                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   用户请求 ──► 路由层 ──► 决策引擎                       │
│                              │                          │
│               ┌──────────────┴──────────────┐          │
│               ▼                              ▼          │
│         本地模型                        云端模型         │
│     (敏感数据/低延迟)               (复杂任务/高精度)     │
│                                                         │
│   优势：                                                 │
│   • 敏感数据本地处理，隐私合规                           │
│   • 简单任务本地完成，成本低                             │
│   • 复杂任务云端支援，效果好                             │
└─────────────────────────────────────────────────────────┘
```

### 8.2 多模态本地推理

```python
# 多模态本地推理示例
from langchain_ollama import ChatOllama
from PIL import Image
import base64

# 加载多模态模型
llm = ChatOllama(
    model="llava:7b",  # 视觉语言模型
    base_url="http://localhost:11434"
)

# 图像理解
with open("image.png", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode()

response = llm.invoke([
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "请描述这张图片"},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
        ]
    }
])

print(response.content)
```

### 8.3 自动模型选择

```python
"""
智能模型选择器
根据任务复杂度自动选择合适的模型
"""
class ModelSelector:
    def __init__(self):
        self.models = {
            "light": "qwen2.5:3b",    # 轻量模型
            "standard": "qwen2.5:7b",  # 标准模型
            "heavy": "qwen2.5:14b"     # 重型模型
        }
    
    def estimate_complexity(self, prompt: str) -> str:
        """评估任务复杂度"""
        # 简单规则：根据输入长度和关键词
        if len(prompt) < 100 and "简单" in prompt:
            return "light"
        elif any(kw in prompt for kw in ["详细分析", "复杂", "深度"]):
            return "heavy"
        else:
            return "standard"
    
    def get_model(self, prompt: str) -> str:
        """获取合适的模型"""
        complexity = self.estimate_complexity(prompt)
        return self.models[complexity]

# 使用
selector = ModelSelector()
model = selector.get_model("请详细分析这篇文章的核心观点")
```

---

## 9. 总结

### 9.1 本地部署实施检查清单

- [ ] **硬件准备**
  - [ ] 确认 CPU/内存/显卡满足需求
  - [ ] 准备足够存储空间（建议 100GB+）

- [ ] **软件安装**
  - [ ] 安装 Ollama
  - [ ] 下载所需模型
  - [ ] 配置 Python 环境

- [ ] **Agent 开发**
  - [ ] 实现 LangGraph 工作流
  - [ ] 集成 RAG 知识库
  - [ ] 添加监控日志

- [ ] **部署上线**
  - [ ] 容器化打包
  - [ ] 配置网络访问
  - [ ] 设置健康检查

- [ ] **安全加固**
  - [ ] 配置防火墙
  - [ ] 启用 HTTPS
  - [ ] 设置访问白名单

### 9.2 给企业 IT 的建议

1. **从小规模试点开始**：先在单个部门部署，验证效果后再推广
2. **建立模型管理规范**：统一模型版本，定期评估效果
3. **重视数据安全**：本地部署不是安全终点，仍需访问控制和审计
4. **预留扩展空间**：架构设计要支持未来向云端扩展

### 9.3 参考资源

| 资源 | 链接 |
|------|------|
| Ollama 官方文档 | [https://ollama.com/docs](https://ollama.com/docs) |
| LangGraph 文档 | [https://langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph) |
| Qwen 模型系列 | [https://qwenlm.github.io](https://qwenlm.github.io) |
| Chroma 向量数据库 | [https://www.trychroma.com](https://www.trychroma.com) |

---

> 💡 **下一步**：完成本地部署后，您可以继续探索：
> - 搭建多 Agent 协作系统
> - 集成企业知识库（飞书、钉钉等）
> - 开发专业领域 Agent（代码助手、数据分析等）

---

*本文代码已在以下环境测试通过：*
- *Ollama 0.5.x*
- *Python 3.11*
- *LangGraph 0.2.x*
- *Ubuntu 22.04 / macOS 14*

*最后更新：2026-03-20*