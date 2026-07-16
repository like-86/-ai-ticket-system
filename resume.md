# 李坤 — AI 应用开发简历

## 教育背景

人工智能 本科在读

---

## 项目经验

### 多 Agent 协作工单系统 — LangGraph ReAct 智能客服
**2026/07 – 至今 | 独立开发**
Github：https://github.com/like-86/-ai-ticket-system

**技术栈：** Python + FastAPI + LangGraph + DeepSeek + ChromaDB + MySQL + Redis + Vue 3 + Vite + Docker

- **Agent 架构：** 基于 LangGraph StateGraph 构建 ReAct 循环 Agent，LLM 自主决策工具调用（创建工单/检索知识库），通过 `bind_tools` 绑定工具、`astream_events` 实现端到端流式输出，替代传统 if-else 意图路由
- **RAG 知识库：** ChromaDB 向量存储 + 固定窗口切分（200字/50重叠），支持 .txt 上传自动切片入库，提供完整 CRUD 与爬虫 API，内置 35 条飞书 FAQ 真实数据
- **多轮对话：** Redis 存储历史消息，`message_to_dict` 序列化 LangChain Message 对象，24h TTL 自动过期，支持跨请求上下文记忆
- **流式输出：** FastAPI SSE 协议 + Vue 3 ReadableStream 逐字渲染，打字机效果
- **工程化：** Docker 编排 MySQL + Redis + FastAPI 三服务一键部署，模块化目录结构，职责清晰

---

### AI 模拟面试管理系统
**2026/06 – 2026/07 | 后端负责人 & 独立开发**
Github：https://github.com/like-86/ruoyi-ai-interview

**技术栈：** Spring Boot 2.x + Spring AI + DeepSeek + MyBatis + MySQL + Redis + Vue 2 + Element UI

- **架构设计：** 基于 RuoYi-Vue 多模块架构，独立设计 8 张业务表（岗位、维度、记录、问题、回答、评分、报告、微信用户），建立外键关联与索引策略，定义 RBAC 细粒度权限标识
- **AI 集成：** Spring AI + DeepSeek 实现 AI 自动出题（按岗位/维度/难度生成）、AI 智能评分（多维度评价 + 优劣势分析 + 改进建议），设计 `AIResultData` 封装返回结构
- **业务开发：** 完成 8 模块 Controller → Service → Mapper 全链路，状态机流转（进行中→已完成→已取消）
- **前端与部署：** Vue 2 + Element UI 完成 8 个功能页面，ECharts 数据可视化，Nginx 反向代理部署

---

## 个人技能

- **大模型应用：** LangGraph ReAct Agent 编排、Spring AI、DeepSeek API、Ollama 本地部署、Prompt Engineering、Function Calling
- **RAG 全流程：** 文档加载 → 切片 → Embedding → ChromaDB 向量库 → 语义检索 → LLM 生成，有完整落地经验
- **后端开发：** Java（Spring Boot + MyBatis + JWT + RBAC）、Python（FastAPI + LangChain + LangGraph）
- **前端开发：** Vue 2 + Element UI + ECharts、Vue 3 + Vite
- **数据库 & 缓存：** MySQL 表设计/索引优化/SQL 调优、Redis 缓存、ChromaDB 向量数据库
- **工具链：** Git、Docker、Nginx、Maven、npm、SSE 流式响应

---

## 个人优势

1. **Java + Python 双栈 AI 能力：** 同时具备 Spring AI 企业级落地经验与 LangChain/LangGraph 快速原型能力，从 API 调用（DeepSeek）到本地部署（Ollama）全线覆盖
2. **快速学习：** 实训 2 周从零上手 RuoYi-Vue 完成 AI 面试系统；课余独立完成 LangGraph ReAct 智能工单系统
3. **工程化意识：** 前后端分离、模块化架构、Docker 容器化部署、代码注释完整
4. **AI 专业背景：** 人工智能本科在读，有机器学习/深度学习理论基础，能阅读英文技术文档
