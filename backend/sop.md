# Vibe Coding SOP: Satu-Sama AI Backend

> **宗旨**: 利用 AI 极大化开发效率。你 (User) 是产品经理 + 架构师，AI 是高级工程师。你负责“定标准”和“Review”，AI 负责“写代码”和“找 Bug”。

## 1. 软硬件资源与分工 (Resource Allocation)

鉴于你的设备配置，我们将计算任务进行分层：

| 环境      | 硬件资源                  | 核心任务                   | Vibe Coding 策略                                                                                                                                                                                                  |
| :-------- | :------------------------ | :------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Local** | **RTX 4060 Laptop (8GB)** | **开发 & 调试 & RAG索引**  | 1. **IDE**: Google Antigravity (编写代码)<br>2. **Environment**: Conda env `3c` + `uv` package manager.<br>3. **后端服务**: 运行 FastAPI server。<br>4. **轻量推理**: 偶尔跑 7B-8B 量化模型 (Q4_K_M) 做本地验证。 |
| **Cloud** | **Tesla V100 (32GB)**     | **训练 & 微调 & 复杂推理** | 1. **Model Training**: 微调 DeepSeek/Llama3 (LoRA/QLoRA) 以适应合规与本地化文案生成。<br>2. **Deployment**: 如果本地显存不够，可将大模型部署为 OpenAI-compatible API 供本地后端调用。                             |

---

## 2. 也是最重要的：Prompt 模板 (Prompt Engineering)

在 Vibe Coding 中，**Prompt 就是源代码的“源代码”**。为了保持风格统一，请使用以下 Structurized Prompt (结构化提示词) 格式。

### 🌟 通用模板 (复制到 IDE 侧边栏/对话框)

```markdown
# Role
你是一个精通 Python (FastAPI) 和 向量数据库 (RAG) 的资深后端工程师。熟悉 Clean Architecture 和 TDD (测试驱动开发)。
环境: Conda env '3c', 使用 'uv pip' 管理依赖。

# Context
项目: Satu-Sama AI (马来西亚跨境电商合规 SaaS)。
技术栈: Python 3.10+, FastAPI, PostgreSQL (SQLModel), ChromaDB (Vector), Pydantic v2.
当前任务: [这里简述你要做什么，例如：开发“合规检查”接口]

# Task Requirements
1. [具体需求1]
2. [具体需求2]

# Constraints & Style
- **Type Hints**: 强制使用 Python 类型注解。
- **Docstrings**: 使用 Google Style Docstrings。
- **Error Handling**: 不要让整个 app 崩溃，抛出具体的 HTTPException。
- **Modular**: 保持函数短小，一个函数只做一件事。
- **Async**: 数据库和外部 API 调用必须是异步 (async/await) 的。
```

### 场景 A: 新功能开发 (Feature Implementation)
> **技巧**: 先让 AI 写 Interface (Pydantic Schema)，你确认后再写 Logic。
> **Example**:
> "我需要一个 API 来上传 PDF 并提取文本。
> 输入: PDF 文件。
> 输出: 提取出的文本内容。
> 请先给出 `schemas/compliance.py` 的定义，再给出 `api/endpoints/compliance.py` 的实现。"

### 场景 B: 重构与优化 (Refactoring)
> **Example**:
> "这个 `services/check.py` 函数太长了（超过 50 行），逻辑混乱。请将其拆分为 3 个子函数：`validate_input`, `process_rules`, `format_report`。保持原有逻辑不变。"

### 场景 C: 写测试 (One-Click Testing)
> **Example**:
> "为 `api/endpoints/compliance.py` 生成 pytest 单元测试。覆盖正常情况和 '文件格式不支持' 的异常情况。"

---

## 3. 项目结构与命名规范 (Project Structure & Naming)

采用 **Modular Monolith (模块化单体)** 架构。Docs 目录分类管理。

```text
backend/
├── app/
│   ├── api/                # API 路由层
│   ├── core/               # 核心配置
│   ├── db/                 # 数据库相关
│   ├── models/             # SQLModel/SQLAlchemy 模型 (DB Schema)
│   ├── schemas/            # Pydantic 模型 (Request/Response Schema)
│   ├── services/           # 业务逻辑层 (Business Logic) + AI Pipeline
│   └── main.py             # App 入口
├── data/                   # 本地知识库源文件 (PDF/Markdown)
├── tests/                  # 测试用例
├── .env                    # 环境变量
├── requirements.txt
└── sop.md                  # 本 SOP 文件

docs/
├── admin/                  # 提案、会议纪要
├── research/               # 调研报告、问卷结果
├── reports/                # 开发报告
└── archive/                # 归档文件
```

### 命名规范 (Naming Convention)
*   **文件名**: `snake_case.py` (e.g., `compliance_service.py`)
*   **类名**: `PascalCase` (e.g., `ComplianceReport`)
*   **变量/函数**: `snake_case` (e.g., `check_halal_compliance`)
*   **常量**: `UPPER_CASE` (e.g., `MAX_TOKEN_LIMIT`)

---

## 4. 极致效率工作流 (The Vibe Coding Workflow)

### Step 1: 环境激活
所有开发开始前，确保终端已激活环境：
```bash
conda activate 3c
```

### Step 2: 伪代码/注释驱动 (Comment-Driven Development)
不要直接写代码。在文件中先写注释，描述你想做什么，然后按 `Tab` 或让 AI 生成。

### Step 3: 模块化生成
1. Schemas -> 2. Services -> 3. API Endpoints

### Step 4: 一键生成测试
"Generate tests for this file."

### Step 5: 错误自愈 (Auto-Debug)
"Fix this." (附带 Error Log)

---

## 5. 推荐技术栈 (Recommended Stack)

*   **API Framework**: **FastAPI**
*   **Database ORM**: **SQLModel**
*   **Vector DB**: **ChromaDB**
*   **LLM Orchestration**: **LiteLLM** + **LlamaIndex**
*   **Package Manager**: **uv** (within Conda)

---
