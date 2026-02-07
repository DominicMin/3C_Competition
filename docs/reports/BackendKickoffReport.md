# Backend Kickoff Report: Satu-Sama AI 后端开发启动报告

## 1. 项目概述 (Project Overview)

**项目名称**: Satu-Sama AI (马来西亚合规与本地化SaaS平台)
**核心定位**: 这里的“AI”不能只是噱头。我们的核心是 **Compliance-as-a-Service (CaaS)**，即“合规即服务”。
**目标用户**: 计划或已经进入马来西亚市场的中国跨境电商卖家（Shopee/TikTok），特别是美妆、食品、个人护理等高合规风险品类。

**核心痛点解决**:
1.  **清真合规 (Halal Compliance)**: 解析JAKIM复杂的认证流程，识别非清真成分（如胭脂红Carmine）。
2.  **平台合规 (Platform Policy)**: TikTok Shop/Shopee 的封号规则预警，避免“误导性宣传”或违禁内容。
3.  **本地化 (Localization)**: 生成符合马来西亚多元文化（Malay/Chinese/Indian）的营销文案。

---

## 2. 当前进度 (Current Progress)

### 已完成 (Done)
- [x] **商业逻辑验证**: 完成了初步的市场调研和问卷调查。
    - 关键发现：用户最需要 **“智能文案本地化” (75%)** 和 **“AI合规快问快答” (66.7%)**。
- [x] **前端演示 (Frontend Demo)**: 
    - UI已实现（参考三态股份风格）。
    - 已部署在 Vercel 上进行测试。
- [x] **初步AI Demo**: 
    - 简单的AI功能展示（目前主要是调用通用大模型API），实现了基本的对话和文案生成。

### 进行中 (In Progress)
- [ ] **域名与品牌**: 正在申请独立域名，品牌Logo（鹭/仙鹤）正在设计中。
- [ ] **商业计划书 (BP)**: 正在整合Demo作为落地证明。

---

## 3. 问题与潜在风险 (Risk Assessment)

为了防止项目后期代码变成“屎山” (Unmaintainable Spaghetti Code)，必须直面当前Demo阶段存在的问题：

### 3.1 核心技术壁垒缺失 (“Wrapper” Risk)
*   **现状**: 目前的AI功能主要是“套壳”通用大模型（GPT/DeepSeek）。
*   **风险**: 用户会问“我为什么不用ChatGPT直接问？”。如果我们的回答和通用AI一样，就没有付费意愿。
*   **对策**: 必须引入 **RAG (检索增强生成)** 技术。我们的护城河在于**私有知识库**（JAKIM官方文档、最新的TikTok封号案例、马来西亚当地法律法规）。通用大模型没有这些实时、细致的垂直数据。

### 3.2 架构扩展性问题
*   **现状**: Demo代码可能为了求快，将逻辑硬编码在前端的一两个文件中。
*   **风险**: 随着功能增加（如添加“利润计算器”、“违规图片检测”），代码将变得极其混乱，无法维护。
*   **对策**: 必须严格实行 **前后端分离**。后端负责复杂的逻辑处理、数据库交互和AI推理，前端只负责展示。

### 3.3 数据隐私与合规 (Data Privacy)
*   **风险**: 跨境SaaS涉及用户上传的产品数据（可能包含商业机密）。
*   **对策**: 需要设计安全的数据存储架构。

### 3.4 幻觉问题 (Hallucination)
*   **风险**: 在“合规”领域，AI不能胡说八道。如果AI错误地告诉卖家“这个成分是清真的”，导致卖家被罚款，SaaS平台将面临巨大责任。
*   **对策**: 必须有 **引用源 (Citations)** 功能，让AI在回答时标注“根据JAKIM 2025年第X条规定...”。

---

## 4. 后端开发规划 (Next Steps & Roadmap)

### Phase 1: 基础设施搭建 (Infrastructure)
*   **技术栈选型**:
    *   **Language**: Python 3.10+ (AI生态最丰富)。
    *   **Framework**: **FastAPI** (高性能，适合异步AI调用，自动生成文档)。
    *   **Database**: PostgreSQL (存储用户、产品数据) + Vector DB (如ChromaDB/Pinecone，用于RAG知识库)。
    *   **LLM Framework**: **LangChain** 或 **LlamaIndex** (用于构建RAG pipeline)。
*   **API规范**: 定义清晰的RESTful API接口文档 (Swagger/OpenAPI)。

### Phase 2: 构建垂直知识库 (Knowledge Base Construction)
这是我们区别于竞品的关键一步。
1.  **数据收集**: 
    *   爬取/整理 JAKIM 官网的最新认证指南。
    *   收集 TikTok Shop Malaysia / Shopee Malaysia 的卖家中心规则文档。
    *   整理马来西亚当地的动植物进出口禁令。
2.  **数据清洗与向量化**: 将上述文档切片，存入向量数据库。

### Phase 3: 核心功能开发 (Core Features Implementation)
优先级基于调查问卷结果：

1.  **AI Localized Copywriting Engine (文案引擎)**
    *   输入：中文商品描述 + 目标画像。
    *   处理：Prompt Engineering + 本地文化知识库（避雷词库）。
    *   输出：Malay/English/Chinese 三语种文案。
    
2.  **Compliance RAG Chatbot (合规问答机器人)**
    *   输入：用户提问（如“这款口红含胭脂红能卖吗？”）。
    *   处理：检索JAKIM成分库 -> LLM生成回答 -> 附带来源链接。
    
3.  **Ingredient Scanner (成分扫描)** (后续迭代)
    *   OCR识别成分表图片 -> 关键词匹配风险库。

### Phase 4: 部署与监控 (Deployment & Monitoring)
*   配置CI/CD流水线，自动化测试后端接口。
*   添加日志监控，记录用户提问，用于后续优化模型。

---

**建议**: 我们现在的核心任务是将“演示版”升级为“工程版”。请尽快确认技术栈首选项，我将为你生成详细的 API 接口定义和数据库设计文档。
