---
layout: post
title: "AI Agent 记忆系统架构：从向量存储到长期记忆的演进之路"
date: 2026-03-20 12:00:00
category: AI
tags: [Agent, Memory-System, Vector-DB, Architecture]
---

# AI Agent 记忆系统架构：从向量存储到长期记忆的演进之路

> 2026 年被称为"AI 记忆元年"。当大语言模型的上下文窗口从 4K 扩展到 128K，甚至 1M，我们依然发现：光有"窗口"不够，Agent 需要真正的"记忆"。

## 一、为什么 Agent 需要记忆系统？

### 1.1 LLM 的"健忘"困境

大语言模型天生是"无状态"的。每次对话，它都像一张白纸：

```
用户：我叫张三，是一名 Java 开发者
LLM：你好张三！很高兴认识你...

用户：你还记得我是谁吗？（新会话）
LLM：抱歉，我不确定您是谁...  # 完全忘记了
```

这不是 Bug，而是 LLM 的设计本质。模型参数在训练后固定，无法在运行时"记住"新信息。

### 1.2 上下文窗口的局限

即便有了超长上下文窗口（Claude 3 的 200K、Gemini 的 1M），问题依然存在：

| 局限 | 描述 |
|------|------|
| **容量有限** | 无限对话历史无法全部塞进去 |
| **成本高昂** | 每次请求都要重复发送历史，Token 消耗巨大 |
| **检索低效** | 在 100 万 Token 中找信息，大海捞针 |
| **无法演化** | 知识无法跨会话沉淀和积累 |

### 1.3 记忆系统的核心价值

真正的 Agent 记忆系统解决三个核心问题：

```
┌─────────────────────────────────────────────────────────┐
│                    Agent 记忆系统                        │
├─────────────────────────────────────────────────────────┤
│  1. 存储：持久化保存交互历史、知识、用户偏好              │
│  2. 检索：根据当前上下文，智能召回相关记忆               │
│  3. 演化：自动压缩、遗忘、重组，形成长期知识积累          │
└─────────────────────────────────────────────────────────┘
```

## 二、记忆系统的分类体系

### 2.1 按时间维度分类

```
短期记忆 (Short-term Memory)
├── 会话内上下文
├── 最近 N 轮对话
└── 临时工作变量

长期记忆 (Long-term Memory)  
├── 用户偏好与画像
├── 历史对话摘要
├── 外部知识库
└── 任务执行经验

工作记忆 (Working Memory)
├── 当前任务状态
├── 中间推理结果
└── 待处理的子目标
```

### 2.2 按存储形式分类

| 类型 | 存储方式 | 特点 | 适用场景 |
|------|----------|------|----------|
| **参数化记忆** | 模型权重 | 训练时固化，推理快 | 领域知识、基础能力 |
| **非参数化记忆** | 向量数据库 | 动态更新，灵活扩展 | 用户数据、实时知识 |
| **混合记忆** | 两者结合 | 兼顾效率与灵活性 | 生产级系统首选 |

### 2.3 按内容类型分类

```python
class MemoryType(Enum):
    """记忆内容类型"""
    EPISODIC = "episodic"      # 情节记忆：具体事件、对话片段
    SEMANTIC = "semantic"      # 语义记忆：概念、事实、知识
    PROCEDURAL = "procedural"  # 程序记忆：技能、方法、流程
    PREFERENCE = "preference"  # 偏好记忆：用户习惯、喜好
```

## 三、核心架构设计

### 3.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        Agent Memory System                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │  Memory      │    │  Memory      │    │  Memory      │       │
│  │  Writer      │───▶│  Store       │◀───│  Retriever   │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         │                   │                   │                │
│         ▼                   ▼                   ▼                │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │  压缩/摘要   │    │  向量数据库   │    │  相似度检索  │       │
│  │  实体抽取   │    │  关键词索引   │    │  时间衰减    │       │
│  │  向量编码   │    │  元数据存储   │    │  重排序      │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Memory Orchestrator                    │   │
│  │  • 记忆生命周期管理  • 遗忘机制  • 记忆合并与重组         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 存储层：向量数据库选型

```python
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum
import numpy as np

class VectorStoreType(Enum):
    """向量存储类型"""
    MILVUS = "milvus"        # 开源，分布式，生产首选
    PINECONE = "pinecone"    # 云服务，免运维
    FAISS = "faiss"          # 轻量级，本地开发
    CHROMA = "chroma"        # 嵌入式，快速原型
    QDRANT = "qdrant"        # Rust 实现，性能优秀

@dataclass
class VectorStoreConfig:
    """向量存储配置"""
    store_type: VectorStoreType
    dimension: int = 1536          # embedding 维度
    metric: str = "cosine"          # 相似度度量
    index_type: str = "HNSW"        # 索引类型
    nlist: int = 1024               # 聚类中心数（IVF 索引）
    m: int = 16                     # HNSW 参数
    ef_construction: int = 256      # HNSW 构建参数

class VectorStore:
    """向量存储抽象接口"""
    
    def __init__(self, config: VectorStoreConfig):
        self.config = config
        self._init_store()
    
    def _init_store(self):
        """初始化存储"""
        if self.config.store_type == VectorStoreType.MILVUS:
            from pymilvus import connections, Collection
            connections.connect("default", host="localhost", port="19530")
            self.collection = Collection("agent_memory")
            
        elif self.config.store_type == VectorStoreType.FAISS:
            import faiss
            self.index = faiss.IndexHNSWFlat(
                self.config.dimension, 
                self.config.m
            )
            
        elif self.config.store_type == VectorStoreType.CHROMA:
            import chromadb
            self.client = chromadb.Client()
            self.collection = self.client.create_collection("memory")
    
    def insert(self, vectors: np.ndarray, metadata: List[Dict[str, Any]]):
        """插入向量"""
        if self.config.store_type == VectorStoreType.MILVUS:
            self.collection.insert([metadata, vectors.tolist()])
        elif self.config.store_type == VectorStoreType.FAISS:
            self.index.add(vectors)
        elif self.config.store_type == VectorStoreType.CHROMA:
            self.collection.add(
                embeddings=vectors.tolist(),
                metadatas=metadata,
                ids=[m["id"] for m in metadata]
            )
    
    def search(self, query_vector: np.ndarray, top_k: int = 10) -> List[Dict]:
        """相似度搜索"""
        if self.config.store_type == VectorStoreType.MILVUS:
            results = self.collection.search(
                [query_vector.tolist()],
                "embedding",
                {"metric_type": "COSINE", "params": {"nprobe": 16}},
                top_k
            )
            return results[0]
        elif self.config.store_type == VectorStoreType.FAISS:
            distances, indices = self.index.search(
                query_vector.reshape(1, -1), top_k
            )
            return list(zip(indices[0], distances[0]))
        elif self.config.store_type == VectorStoreType.CHROMA:
            return self.collection.query(
                query_embeddings=query_vector.tolist(),
                n_results=top_k
            )
```

**选型对比**：

| 特性 | Milvus | Pinecone | FAISS | Chroma |
|------|--------|----------|-------|--------|
| 部署方式 | 自托管/云 | 仅云服务 | 本地 | 嵌入式 |
| 分布式 | ✅ | ✅ | ❌ | ❌ |
| 性能 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 运维成本 | 中 | 低 | 无 | 无 |
| 生产就绪 | ✅ | ✅ | ⚠️ | ⚠️ |
| 推荐场景 | 大规模生产 | 快速上线 | 开发测试 | 原型验证 |

### 3.3 索引层：Embedding 与编码

```python
from abc import ABC, abstractmethod
from typing import List
import numpy as np

class EmbeddingModel(ABC):
    """Embedding 模型抽象"""
    
    @abstractmethod
    def encode(self, texts: List[str]) -> np.ndarray:
        """编码文本为向量"""
        pass

class OpenAIEmbedding(EmbeddingModel):
    """OpenAI Embedding"""
    
    def __init__(self, model: str = "text-embedding-3-small"):
        from openai import OpenAI
        self.client = OpenAI()
        self.model = model
    
    def encode(self, texts: List[str]) -> np.ndarray:
        response = self.client.embeddings.create(
            input=texts,
            model=self.model
        )
        return np.array([item.embedding for item in response.data])

class BGEEmbedding(EmbeddingModel):
    """BGE 中文 Embedding（开源）"""
    
    def __init__(self, model_name: str = "BAAI/bge-large-zh-v1.5"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)
    
    def encode(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, normalize_embeddings=True)

class MemoryEncoder:
    """记忆编码器"""
    
    def __init__(self, embedding_model: EmbeddingModel):
        self.embedding_model = embedding_model
    
    def encode_memory(self, memory: 'MemoryItem') -> np.ndarray:
        """编码单个记忆项"""
        # 组合多种信息进行编码
        text_to_encode = f"""
        [{memory.memory_type}] {memory.content}
        时间: {memory.timestamp}
        重要性: {memory.importance}
        """
        return self.embedding_model.encode([text_to_encode])[0]
    
    def encode_with_context(self, memory: 'MemoryItem', context: str) -> np.ndarray:
        """带上下文的编码"""
        combined = f"{context}\n\n{memory.content}"
        return self.embedding_model.encode([combined])[0]
```

### 3.4 检索层：多策略召回

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import numpy as np

@dataclass
class MemoryItem:
    """记忆项"""
    id: str
    content: str
    embedding: Optional[np.ndarray] = None
    memory_type: str = "episodic"
    timestamp: datetime = None
    importance: float = 0.5
    access_count: int = 0
    last_accessed: datetime = None
    metadata: Dict[str, Any] = None

class MemoryRetriever:
    """记忆检索器"""
    
    def __init__(
        self,
        vector_store: VectorStore,
        embedding_model: EmbeddingModel,
        time_decay_factor: float = 0.1,
        importance_weight: float = 0.3,
        relevance_weight: float = 0.5,
        recency_weight: float = 0.2
    ):
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.time_decay_factor = time_decay_factor
        self.importance_weight = importance_weight
        self.relevance_weight = relevance_weight
        self.recency_weight = recency_weight
    
    def retrieve(
        self, 
        query: str, 
        top_k: int = 10,
        memory_types: List[str] = None,
        time_range: tuple = None
    ) -> List[MemoryItem]:
        """检索相关记忆"""
        
        # 1. 向量相似度检索
        query_embedding = self.embedding_model.encode([query])[0]
        candidates = self.vector_store.search(query_embedding, top_k * 3)
        
        # 2. 过滤
        if memory_types:
            candidates = [
                c for c in candidates 
                if c.metadata.get("memory_type") in memory_types
            ]
        
        if time_range:
            start_time, end_time = time_range
            candidates = [
                c for c in candidates
                if start_time <= c.metadata.get("timestamp", end_time) <= end_time
            ]
        
        # 3. 重排序（综合得分）
        scored_candidates = []
        for candidate in candidates:
            score = self._compute_final_score(candidate, query_embedding)
            scored_candidates.append((candidate, score))
        
        # 4. 返回 Top-K
        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        return [item for item, score in scored_candidates[:top_k]]
    
    def _compute_final_score(
        self, 
        candidate: Dict, 
        query_embedding: np.ndarray
    ) -> float:
        """计算综合得分"""
        
        # 相关性得分（向量相似度）
        relevance_score = self._cosine_similarity(
            query_embedding, 
            np.array(candidate.get("embedding", []))
        )
        
        # 时间衰减得分
        timestamp = candidate.get("timestamp", datetime.now())
        age_days = (datetime.now() - timestamp).days
        recency_score = np.exp(-self.time_decay_factor * age_days)
        
        # 重要性得分
        importance_score = candidate.get("importance", 0.5)
        
        # 加权综合
        final_score = (
            self.relevance_weight * relevance_score +
            self.recency_weight * recency_score +
            self.importance_weight * importance_score
        )
        
        return final_score
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """计算余弦相似度"""
        if a.size == 0 or b.size == 0:
            return 0.0
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class HybridRetriever(MemoryRetriever):
    """混合检索器：向量 + 关键词"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword_index = {}  # 简化的关键词索引
    
    def build_keyword_index(self, memories: List[MemoryItem]):
        """构建关键词索引"""
        for memory in memories:
            keywords = self._extract_keywords(memory.content)
            for keyword in keywords:
                if keyword not in self.keyword_index:
                    self.keyword_index[keyword] = []
                self.keyword_index[keyword].append(memory.id)
    
    def retrieve_hybrid(
        self, 
        query: str, 
        top_k: int = 10,
        vector_weight: float = 0.7,
        keyword_weight: float = 0.3
    ) -> List[MemoryItem]:
        """混合检索"""
        
        # 向量检索
        vector_results = self.retrieve(query, top_k * 2)
        vector_scores = {r.id: 1.0 - i / len(vector_results) 
                        for i, r in enumerate(vector_results)}
        
        # 关键词检索
        query_keywords = self._extract_keywords(query)
        keyword_scores = {}
        for keyword in query_keywords:
            if keyword in self.keyword_index:
                for memory_id in self.keyword_index[keyword]:
                    keyword_scores[memory_id] = keyword_scores.get(memory_id, 0) + 1
        
        # 归一化
        max_keyword_score = max(keyword_scores.values()) if keyword_scores else 1
        keyword_scores = {k: v / max_keyword_score for k, v in keyword_scores.items()}
        
        # 融合得分
        all_ids = set(vector_scores.keys()) | set(keyword_scores.keys())
        final_scores = {}
        for mid in all_ids:
            final_scores[mid] = (
                vector_weight * vector_scores.get(mid, 0) +
                keyword_weight * keyword_scores.get(mid, 0)
            )
        
        # 排序返回
        sorted_ids = sorted(final_scores.keys(), 
                           key=lambda x: final_scores[x], 
                           reverse=True)
        return [self._get_memory_by_id(mid) for mid in sorted_ids[:top_k]]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词（简化版）"""
        import jieba
        return list(jieba.cut(text))
    
    def _get_memory_by_id(self, memory_id: str) -> MemoryItem:
        """根据 ID 获取记忆"""
        # 实际实现需要从存储中获取
        pass
```

## 四、记忆生命周期管理

### 4.1 记忆写入流程

```python
from datetime import datetime
import uuid
from typing import List, Dict, Any

class MemoryWriter:
    """记忆写入器"""
    
    def __init__(
        self,
        vector_store: VectorStore,
        embedding_model: EmbeddingModel,
        compression_threshold: int = 500  # 字符数阈值
    ):
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.compression_threshold = compression_threshold
    
    async def write(
        self,
        content: str,
        memory_type: str = "episodic",
        importance: float = 0.5,
        metadata: Dict[str, Any] = None
    ) -> MemoryItem:
        """写入新记忆"""
        
        # 1. 评估是否需要压缩
        if len(content) > self.compression_threshold:
            content = await self._compress(content)
        
        # 2. 生成 embedding
        embedding = self.embedding_model.encode([content])[0]
        
        # 3. 创建记忆项
        memory = MemoryItem(
            id=str(uuid.uuid4()),
            content=content,
            embedding=embedding,
            memory_type=memory_type,
            timestamp=datetime.now(),
            importance=importance,
            last_accessed=datetime.now(),
            metadata=metadata or {}
        )
        
        # 4. 存入向量库
        self.vector_store.insert(
            embedding.reshape(1, -1),
            [{
                "id": memory.id,
                "content": memory.content,
                "memory_type": memory.memory_type,
                "timestamp": memory.timestamp.isoformat(),
                "importance": memory.importance,
                **memory.metadata
            }]
        )
        
        return memory
    
    async def _compress(self, content: str) -> str:
        """使用 LLM 压缩记忆"""
        # 实际实现调用 LLM 进行摘要
        prompt = f"""请将以下内容压缩为关键信息，保留重要细节：

{content}

压缩后的内容（不超过200字）："""
        # compressed = await self.llm.generate(prompt)
        # return compressed
        return content[:200] + "..."  # 简化示例
```

### 4.2 遗忘机制

```python
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class ForgettingStrategy(ABC):
    """遗忘策略抽象"""
    
    @abstractmethod
    def should_forget(self, memory: MemoryItem) -> bool:
        """判断是否应该遗忘"""
        pass

class TimeBasedForgetting(ForgettingStrategy):
    """基于时间的遗忘"""
    
    def __init__(self, max_age_days: int = 30):
        self.max_age_days = max_age_days
    
    def should_forget(self, memory: MemoryItem) -> bool:
        age = datetime.now() - memory.timestamp
        return age > timedelta(days=self.max_age_days)

class AccessBasedForgetting(ForgettingStrategy):
    """基于访问的遗忘"""
    
    def __init__(self, max_inactive_days: int = 14):
        self.max_inactive_days = max_inactive_days
    
    def should_forget(self, memory: MemoryItem) -> bool:
        if memory.last_accessed is None:
            return False
        inactive = datetime.now() - memory.last_accessed
        return inactive > timedelta(days=self.max_inactive_days)

class ImportanceBasedForgetting(ForgettingStrategy):
    """基于重要性的遗忘"""
    
    def __init__(self, min_importance: float = 0.3):
        self.min_importance = min_importance
    
    def should_forget(self, memory: MemoryItem) -> bool:
        return memory.importance < self.min_importance

class CompositeForgetting(ForgettingStrategy):
    """组合遗忘策略"""
    
    def __init__(self, strategies: List[ForgettingStrategy]):
        self.strategies = strategies
    
    def should_forget(self, memory: MemoryItem) -> bool:
        # 任一策略触发即遗忘
        return any(s.should_forget(memory) for s in self.strategies)

class MemoryForgetter:
    """记忆遗忘管理器"""
    
    def __init__(self, strategy: ForgettingStrategy):
        self.strategy = strategy
    
    def scan_and_forget(self, memories: List[MemoryItem]) -> List[str]:
        """扫描并返回应遗忘的记忆 ID"""
        to_forget = []
        for memory in memories:
            if self.strategy.should_forget(memory):
                to_forget.append(memory.id)
        return to_forget
    
    def archive_instead_of_delete(self, memory: MemoryItem) -> dict:
        """归档而非删除"""
        return {
            "id": memory.id,
            "content_hash": hash(memory.content),
            "archived_at": datetime.now().isoformat(),
            "reason": "forgotten"
        }
```

### 4.3 记忆合并与重组

```python
class MemoryConsolidator:
    """记忆整合器"""
    
    def __init__(
        self,
        similarity_threshold: float = 0.85,
        llm_client = None
    ):
        self.similarity_threshold = similarity_threshold
        self.llm_client = llm_client
    
    async def consolidate(
        self, 
        memories: List[MemoryItem]
    ) -> List[MemoryItem]:
        """整合相似记忆"""
        
        # 1. 聚类相似记忆
        clusters = self._cluster_similar(memories)
        
        consolidated = []
        for cluster in clusters:
            if len(cluster) > 1:
                # 2. 合并相似记忆
                merged = await self._merge_memories(cluster)
                consolidated.append(merged)
            else:
                consolidated.append(cluster[0])
        
        return consolidated
    
    def _cluster_similar(
        self, 
        memories: List[MemoryItem]
    ) -> List[List[MemoryItem]]:
        """聚类相似记忆"""
        clusters = []
        used = set()
        
        for i, mem1 in enumerate(memories):
            if i in used:
                continue
            
            cluster = [mem1]
            used.add(i)
            
            for j, mem2 in enumerate(memories):
                if j in used:
                    continue
                
                similarity = self._cosine_similarity(
                    mem1.embedding, mem2.embedding
                )
                
                if similarity > self.similarity_threshold:
                    cluster.append(mem2)
                    used.add(j)
            
            clusters.append(cluster)
        
        return clusters
    
    async def _merge_memories(
        self, 
        memories: List[MemoryItem]
    ) -> MemoryItem:
        """合并多条记忆"""
        
        # 提取共同信息
        combined_content = "\n".join([m.content for m in memories])
        
        # 使用 LLM 提取核心信息
        prompt = f"""请从以下多条相关记忆中提取核心信息，生成一条整合后的记忆：

{combined_content}

整合后的记忆（保留关键信息，去除重复）："""

        # merged_content = await self.llm_client.generate(prompt)
        merged_content = f"[整合] {memories[0].content[:100]}..."
        
        # 创建合并后的记忆
        return MemoryItem(
            id=str(uuid.uuid4()),
            content=merged_content,
            embedding=memories[0].embedding,  # 使用第一条的 embedding
            memory_type=memories[0].memory_type,
            timestamp=datetime.now(),
            importance=max(m.importance for m in memories),
            metadata={
                "merged_from": [m.id for m in memories],
                "merge_count": len(memories)
            }
        )
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        if a is None or b is None:
            return 0.0
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

## 五、实战：构建一个完整的记忆系统

### 5.1 系统集成

```python
from dataclasses import dataclass
from typing import List, Optional
import asyncio

@dataclass
class MemorySystemConfig:
    """记忆系统配置"""
    vector_store_type: str = "milvus"
    embedding_model: str = "bge-large-zh"
    max_short_term_items: int = 10
    max_long_term_items: int = 10000
    compression_threshold: int = 500
    forgetting_max_age_days: int = 30
    consolidation_interval_hours: int = 24

class AgentMemorySystem:
    """Agent 记忆系统"""
    
    def __init__(self, config: MemorySystemConfig):
        self.config = config
        
        # 初始化组件
        self.vector_store = self._init_vector_store()
        self.embedding_model = self._init_embedding_model()
        
        self.writer = MemoryWriter(
            self.vector_store, 
            self.embedding_model,
            config.compression_threshold
        )
        self.retriever = MemoryRetriever(
            self.vector_store,
            self.embedding_model
        )
        self.forgetter = MemoryForgetter(
            CompositeForgetting([
                TimeBasedForgetting(config.forgetting_max_age_days),
                AccessBasedForgetting(14),
                ImportanceBasedForgetting(0.3)
            ])
        )
        self.consolidator = MemoryConsolidator()
        
        # 工作记忆（内存中）
        self.working_memory: List[MemoryItem] = []
    
    def _init_vector_store(self) -> VectorStore:
        """初始化向量存储"""
        config = VectorStoreConfig(
            store_type=VectorStoreType[self.config.vector_store_type.upper()],
            dimension=1024  # bge-large-zh
        )
        return VectorStore(config)
    
    def _init_embedding_model(self) -> EmbeddingModel:
        """初始化 Embedding 模型"""
        return BGEEmbedding(f"BAAI/{self.config.embedding_model}")
    
    async def remember(
        self,
        content: str,
        memory_type: str = "episodic",
        importance: float = 0.5,
        metadata: dict = None
    ) -> MemoryItem:
        """记住新信息"""
        memory = await self.writer.write(
            content=content,
            memory_type=memory_type,
            importance=importance,
            metadata=metadata
        )
        
        # 同时加入工作记忆
        self.working_memory.append(memory)
        if len(self.working_memory) > self.config.max_short_term_items:
            self.working_memory.pop(0)
        
        return memory
    
    async def recall(
        self,
        query: str,
        top_k: int = 5,
        include_working_memory: bool = True
    ) -> List[MemoryItem]:
        """回忆相关信息"""
        results = []
        
        # 1. 从长期记忆检索
        long_term_results = self.retriever.retrieve(query, top_k)
        results.extend(long_term_results)
        
        # 2. 从工作记忆匹配
        if include_working_memory:
            query_embedding = self.embedding_model.encode([query])[0]
            for memory in self.working_memory:
                similarity = self._cosine_similarity(
                    query_embedding, memory.embedding
                )
                if similarity > 0.7:
                    results.append(memory)
        
        return results[:top_k]
    
    async def forget(self) -> int:
        """执行遗忘"""
        # 获取所有记忆
        all_memories = await self._get_all_memories()
        
        # 识别应遗忘的记忆
        to_forget = self.forgetter.scan_and_forget(all_memories)
        
        # 执行删除
        for memory_id in to_forget:
            await self._delete_memory(memory_id)
        
        return len(to_forget)
    
    async def consolidate(self) -> int:
        """执行记忆整合"""
        all_memories = await self._get_all_memories()
        consolidated = await self.consolidator.consolidate(all_memories)
        
        # 更新存储
        await self._update_memories(consolidated)
        
        return len(all_memories) - len(consolidated)
    
    def get_context_for_prompt(
        self,
        current_query: str,
        max_tokens: int = 2000
    ) -> str:
        """构建用于 Prompt 的记忆上下文"""
        memories = asyncio.run(self.recall(current_query, top_k=5))
        
        context_parts = ["## 相关记忆\n"]
        current_tokens = 0
        
        for memory in memories:
            # 简单的 token 估算
            estimated_tokens = len(memory.content) // 4
            
            if current_tokens + estimated_tokens > max_tokens:
                break
            
            context_parts.append(f"- [{memory.memory_type}] {memory.content}\n")
            current_tokens += estimated_tokens
        
        return "".join(context_parts)
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        if a is None or b is None:
            return 0.0
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    async def _get_all_memories(self) -> List[MemoryItem]:
        """获取所有记忆"""
        # 实际实现需要从存储中获取
        return []
    
    async def _delete_memory(self, memory_id: str):
        """删除记忆"""
        pass
    
    async def _update_memories(self, memories: List[MemoryItem]):
        """更新记忆"""
        pass
```

### 5.2 与 Agent 集成

```python
from typing import AsyncIterator

class MemoryAwareAgent:
    """具备记忆能力的 Agent"""
    
    def __init__(
        self,
        llm_client,
        memory_system: AgentMemorySystem,
        system_prompt: str = ""
    ):
        self.llm_client = llm_client
        self.memory = memory_system
        self.system_prompt = system_prompt
    
    async def chat(self, user_input: str) -> AsyncIterator[str]:
        """带记忆的对话"""
        
        # 1. 检索相关记忆
        relevant_memories = await self.memory.recall(user_input)
        
        # 2. 构建带记忆的 Prompt
        memory_context = self.memory.get_context_for_prompt(user_input)
        
        full_prompt = f"""
{self.system_prompt}

{memory_context}

## 当前对话
用户: {user_input}
助手: """
        
        # 3. 调用 LLM
        response_text = ""
        async for chunk in self.llm_client.generate_stream(full_prompt):
            response_text += chunk
            yield chunk
        
        # 4. 存储对话记忆
        await self.memory.remember(
            content=f"用户: {user_input}\n助手: {response_text}",
            memory_type="episodic",
            importance=self._estimate_importance(user_input, response_text)
        )
    
    def _estimate_importance(self, user_input: str, response: str) -> float:
        """估算记忆重要性"""
        # 简化实现：根据内容长度和关键词判断
        importance = 0.5
        
        # 包含用户偏好信息
        if any(kw in user_input for kw in ["我喜欢", "我是", "我的"]):
            importance += 0.2
        
        # 包含重要事实
        if any(kw in response for kw in ["重要", "注意", "记住"]):
            importance += 0.2
        
        return min(importance, 1.0)
    
    async def learn_preference(self, preference: str):
        """显式学习用户偏好"""
        await self.memory.remember(
            content=preference,
            memory_type="preference",
            importance=0.9  # 用户偏好高重要性
        )
    
    async def save_fact(self, fact: str):
        """保存知识事实"""
        await self.memory.remember(
            content=fact,
            memory_type="semantic",
            importance=0.7
        )
```

## 六、高级话题

### 6.1 多模态记忆

```python
from typing import Union
import base64

class MultiModalMemory:
    """多模态记忆"""
    
    def __init__(self, text_encoder, image_encoder, audio_encoder):
        self.text_encoder = text_encoder
        self.image_encoder = image_encoder
        self.audio_encoder = audio_encoder
    
    async def store(
        self,
        content: Union[str, bytes],
        modality: str = "text",
        metadata: dict = None
    ) -> MemoryItem:
        """存储多模态内容"""
        
        if modality == "text":
            embedding = self.text_encoder.encode([content])[0]
        elif modality == "image":
            embedding = await self.image_encoder.encode(content)
        elif modality == "audio":
            embedding = await self.audio_encoder.encode(content)
        else:
            raise ValueError(f"Unknown modality: {modality}")
        
        return MemoryItem(
            id=str(uuid.uuid4()),
            content=content if isinstance(content, str) else base64.b64encode(content).decode(),
            embedding=embedding,
            memory_type=f"{modality}_memory",
            metadata={**(metadata or {}), "modality": modality}
        )
    
    async def cross_modal_retrieve(
        self,
        query: str,
        target_modality: str = "image",
        top_k: int = 5
    ) -> List[MemoryItem]:
        """跨模态检索（如用文本搜索图片）"""
        # 使用 CLIP 等多模态模型实现
        pass
```

### 6.2 多 Agent 共享记忆

```python
class SharedMemorySpace:
    """共享记忆空间"""
    
    def __init__(self, memory_system: AgentMemorySystem):
        self.memory = memory_system
        self.agent_access_log = {}  # agent_id -> accessed_memory_ids
    
    async def share_memory(
        self,
        from_agent: str,
        to_agent: str,
        memory_id: str
    ):
        """在 Agent 间共享记忆"""
        memory = await self.memory.recall_by_id(memory_id)
        
        # 添加共享标记
        memory.metadata["shared_by"] = from_agent
        memory.metadata["shared_to"] = to_agent
        
        # 记录访问
        if to_agent not in self.agent_access_log:
            self.agent_access_log[to_agent] = []
        self.agent_access_log[to_agent].append(memory_id)
    
    async def get_team_memories(
        self,
        agent_ids: List[str],
        query: str,
        top_k: int = 10
    ) -> List[MemoryItem]:
        """获取团队共享记忆"""
        all_memories = []
        for agent_id in agent_ids:
            accessible = self.agent_access_log.get(agent_id, [])
            # 检索并合并
            pass
        return all_memories[:top_k]
```

## 七、性能优化与最佳实践

### 7.1 批量处理

```python
class BatchMemoryProcessor:
    """批量记忆处理器"""
    
    def __init__(self, memory_system: AgentMemorySystem, batch_size: int = 100):
        self.memory = memory_system
        self.batch_size = batch_size
        self.pending_memories = []
    
    async def add(self, content: str, **kwargs):
        """添加到待处理队列"""
        self.pending_memories.append((content, kwargs))
        
        if len(self.pending_memories) >= self.batch_size:
            await self.flush()
    
    async def flush(self):
        """批量写入"""
        if not self.pending_memories:
            return
        
        # 批量生成 embedding
        contents = [item[0] for item in self.pending_memories]
        embeddings = self.memory.embedding_model.encode(contents)
        
        # 批量写入
        for i, (content, kwargs) in enumerate(self.pending_memories):
            await self.memory.remember(
                content=content,
                embedding=embeddings[i],
                **kwargs
            )
        
        self.pending_memories.clear()
```

### 7.2 缓存策略

```python
import redis
import json

class MemoryCache:
    """记忆缓存层"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.ttl = 3600  # 1 小时缓存
    
    def get(self, query_hash: str) -> Optional[List[dict]]:
        """获取缓存"""
        cached = self.redis.get(f"memory:query:{query_hash}")
        if cached:
            return json.loads(cached)
        return None
    
    def set(self, query_hash: str, results: List[dict]):
        """设置缓存"""
        self.redis.setex(
            f"memory:query:{query_hash}",
            self.ttl,
            json.dumps(results)
        )
    
    def invalidate(self, memory_id: str):
        """失效相关缓存"""
        # 删除包含该 memory_id 的所有查询缓存
        pattern = f"memory:query:*"
        for key in self.redis.scan_iter(pattern):
            cached = self.redis.get(key)
            if cached and memory_id in cached.decode():
                self.redis.delete(key)
```

## 八、总结

AI Agent 的记忆系统是实现真正智能的关键基础设施。从向量存储到长期记忆，从遗忘机制到记忆整合，每一个环节都需要精心设计。

**核心要点**：

| 组件 | 关键技术 | 注意事项 |
|------|----------|----------|
| 存储层 | 向量数据库选型 | 根据规模选择 Milvus/FAISS |
| 索引层 | Embedding 模型 | 中文推荐 BGE 系列 |
| 检索层 | 多策略召回 | 结合向量+关键词+时间 |
| 生命周期 | 写入/遗忘/整合 | 定期执行整合任务 |
| 优化 | 批量+缓存 | 生产环境必备 |

**未来趋势**：

1. **记忆 OS**：MemGPT、Letta 等记忆操作系统兴起
2. **参数化记忆**：模型微调作为长期记忆
3. **统一表征**：多模态记忆的统一编码
4. **隐私计算**：联邦学习 + 记忆保护

---

*本文系统性地介绍了 AI Agent 记忆系统的设计与实现，希望能为架构师和开发者提供参考。记忆是智能的基础，让我们一起构建更有"灵魂"的 Agent。*