# AI Training & RAG Strategy: Satu-Sama AI

## 1. 核心策略 (Core Strategy)
我们采用 **RAG-First, Fine-Tuning-Second** 的策略。
*   **RAG (Retrieval-Augmented Generation)**: 解决“幻觉”问题，确保合规回答有据可依（引用 JAKIM/TikTok 官方文档）。
*   **Fine-Tuning (SFT)**: 解决“风格”和“推理”问题，让模型更懂马来西亚华语/马来语的表达习惯，以及更擅长从非结构化文本中提取合规风险点。

---

## 2. 硬件资源分配 (Infrastructure)

| 任务                   | 环境              | 模型/工具                                             | 显存需求 |
| :--------------------- | :---------------- | :---------------------------------------------------- | :------- |
| **Embedding (向量化)** | Local (RTX 4060)  | `BAAI/bge-m3` (支持多语言，长度8192)                  | < 2GB    |
| **Vector DB (存储)**   | Local             | ChromaDB (本地持久化)                                 | RAM/Disk |
| **Inference (推理)**   | Local (RTX 4060)  | `DeepSeek-R1-Distill-Llama-8B-GGUF` (4-bit Quantized) | ~6-7GB   |
| **Training (微调)**    | Cloud (V100 32GB) | `Llama-3-8B-Instruct` or `DeepSeek-7B` (LoRA/QLoRA)   | ~16-24GB |

### 生产环境部署与成本分析 (Production Cost Strategy)
针对“三创赛”的商业计划书，建议采用 **Hybrid (混合) 部署架构** 以极致压缩成本并保留核心技术壁垒：

1.  **自有模型 (The "Brain")**: 针对高敏感数据（如未公开的配方、核心合规算法），使用微调后的 7B/8B 模型。
    *   **部署方案**: 租用消费级云 GPU (如 RTX 3090/4090 或 T4 服务器，AutoDL/阿里云抢占式实例)。
    *   **成本估算**: 约 ¥2000-3000/月 (对比 V100/A100 动辄 ¥10000+)。
    *   **商业价值**: 强调“数据主权”和“核心算法自主可控”，这是比赛加分项。

2.  **通用能力 (The "Mouth")**: 针对润色、翻译等通用任务，调用高性价比 API。
    *   **方案**: DeepSeek API 或 SiliconFlow。
    *   **成本**: 极低 (DeepSeek-V3 仅 ¥1-2 / 百万 tokens)。
    *   **优势**: 避免为了“且”字怎么写而消耗昂贵的自有算力。

**结论**: 这种“小核心(本地) + 大外围(API)”的架构，既证明了技术实力（有自研模型），又证明了商业头脑（成本控制）。

---

## 3. RAG 架构设计 (RAG Pipeline)

### 3.1 数据源 (Data Sources)
我们需要构建两个核心知识库：
1.  **Halal Knowledge Base (清真知识库)**
    *   源文件: JAKIM Halal Manual (PDF), MyeHALAL User Guideline.
    *   处理: 使用 `LlamaParse` 解析复杂表格（PDF中的非结构化数据）。
2.  **Compliance Knowledge Base (合规知识库)**
    *   源文件: TikTok Shop Prohibited Products Policy, Shopee Malaysia Listing Guidelines.
    *   处理: Markdown 切片。

### 3.2 检索流程 (Retrieval)
*   **Chunking**: 按语义切分 (Semantic Chunking)，每块 512 tokens，重叠 50 tokens。
*   **Embedding**: 使用 `bge-m3` 生成密集向量。
*   **Hybrid Search**: 结合 向量搜索 (Dense) + 关键词搜索 (BM25)，确保专有名词（如 "Carmine"）能被精准召回。

---

## 4. 模型微调计划 (Fine-Tuning Plan)

### 4.1 为什么需要微调？
通用模型（如 GPT-4/DeepSeek）虽然强大，但在以下场景表现不佳：
1.  **"Manglish" (马来西亚式英语)**: 本地化文案需要特定的俚语和句式。
2.  **JSON 格式遵循**: 我们需要 API 稳定输出 JSON 格式的合规报告，微调能极大提高指令遵循能力。

### 4.2 训练数据构建 (Dataset)
*   **目标**: 500-1000 条高质量 (Instruction, Output) 对。
*   **合成数据**: 使用 GPT-4 根据 JAKIM 规则生成模拟的“用户提问-专家回答”对。
    *   *Input*: "这个口红含有胭脂红，能在马来西亚卖吗？"
    *   *Output*: "不能。根据 JAKIM 标准，胭脂红 (Carmine) 属于昆虫提取物..."

### 4.3 训练流程 (LoRA)
1.  **Base Model**: `Llama-3-8B-Instruct`。
2.  **Method**: QLoRA (4-bit Quantization + LoRA adapters)。
3.  **Hyperparameters**:
    *   Rank (r): 16
    *   Alpha: 32
    *   Learning Rate: 2e-4
    *   Epochs: 3
4.  **Output**: 训练好的 LoRA Adapter (约 100MB)，可在本地 RTX 4060 上与 Base Model 合并加载。

---

## 5. 开发路线图 (Execution Roadmap)

1.  **Step 1: RAG Demo (Local)**
    *   搭建 ChromaDB。
    *   编写脚本 `scripts/ingest_data.py` 将 `docs/research/` 下的文档向量化。
    *   使用 `LiteLLM` 调用云端 API (DeepSeek/GPT) 测试检索效果。
2.  **Step 2: Local LLM Inference**
    *   在本地部署 `Ollama` 或 `Llama.cpp`。
    *   测试 8B 模型在 4060 上的推理速度 (Tokens/sec)。
3.  **Step 3: Fine-Tuning (Cloud)**
    *   在云端服务器租用 V100。
    *   运行 `Unsloth` (训练速度快2倍) 进行微调。
    *   导出 LoRA 权重回本地。

---

---

## 6. MVP 开发与前端联动 (MVP & Frontend Integration)

### 6.1 MVP 策略
**直接开发即 MVP**。不要开发一个“用完即弃”的 Demo。
正如 SOP 中所述，我们采用 **Modular Monolith**。现在的 MVP 就是未来正式版的核心模块（Auth + Compliance）。

### 6.2 前端联动方案
由于前端已开发完毕（且可能是静态或 Mock 数据），后端需提供标准 API 进行对接。

1.  **API 文档**: 后端启动后访问 `http://localhost:8000/docs` 会自动生成 Swagger UI。
2.  **对接流程**:
    *   前端同学查看 Swagger 文档。
    *   将前端代码中的 `fetch('/fake-data')` 替换为 `fetch('http://localhost:8000/api/v1/compliance/check')`。
    *   **CORS**: 后端会配置 CORS 允许前端跨域调用。

建议立即将前端代码放入 `frontend/` 目录（如果可以），这样可以统一管理。
