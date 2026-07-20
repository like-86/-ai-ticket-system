# 🤖 AI 工单助手 - 多 Agent 协作系统

基于 **LangGraph ReAct Agent** 的智能客服 + 工单系统。接入 DeepSeek LLM，自动识别用户意图，检索知识库或创建工单，支持流式对话和多轮记忆。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | FastAPI + LangGraph |
| AI 模型 | DeepSeek Chat (ChatOpenAI) |
| Agent 架构 | ReAct (Reasoning + Acting) 循环 |
| 向量数据库 | ChromaDB (35 条飞书 FAQ) |
| 会话缓存 | Redis |
| 业务数据库 | MySQL |
| 前端 | Vue 3 + Vite |
| 部署 | Docker + docker-compose |

## 功能

- **ReAct Agent** — LLM 自主决定调不调工具、调哪个工具，支持多轮推理循环
- **流式输出** — SSE 协议，逐字显示，打字机效果
- **多轮对话** — Redis 存储会话历史，24 小时自动过期
- **知识库 RAG** — ChromaDB 向量检索，支持上传文档自动切分入库
- **工单系统** — LLM 判断需人工介入时自动创建工单，存入 MySQL
- **知识管理 API** — 增删改查、上传 .txt 文件、自动切片
- **用户认证** — JWT 登录鉴权，bcrypt 密码加密，全局中间件保护所有 API
- **自动化测试** — pytest 全覆盖（纯函数、Service、API），Mock 外部依赖，SQLite 内存库替代 MySQL
- **CI/CD** — GitHub Actions 每次推送自动跑测试

## 项目结构

```
├── app/
│   ├── agents/              # LLM 封装（同步 + 流式）
│   │   ├── base_agent.py    # ChatOpenAI 封装
│   │   ├── intent_agent.py  # 意图识别（旧，已由 ReAct 替代）
│   │   └── retrieval_agent.py # 知识库检索封装
│   │
│   ├── api/                 # REST API
│   │   ├── chat.py          # 聊天接口（同步 + 流式 SSE）
│   │   ├── tickets.py       # 工单 CRUD
│   │   └── knowledge.py     # 知识库管理
│   │
│   ├── graph/
│   │   └── workflow.py      # LangGraph ReAct 图编排
│   │
│   ├── services/
│   │   ├── knowledge_base.py # ChromaDB 向量知识库
│   │   ├── session.py       # Redis 会话管理
│   │   └── crawler.py       # 网页爬虫（导入知识库）
│   │
│   ├── tools/
│   │   └── mcp_server.py    # @tool 工具定义
│   │
│   ├── db/
│   │   ├── database.py      # MySQL 连接
│   │   └── models.py        # Ticket 模型
│   │
│   ├── config.py            # 配置管理
│   └── main.py              # FastAPI 入口
│
├── frontend/                # Vue 3 前端
│   └── src/
│       ├── App.vue
│       ├── components/
│       │   ├── ChatPage.vue      # 聊天界面（流式接收）
│       │   └── TicketsPanel.vue  # 工单侧边栏
│       └── style.css
│
├── Dockerfile               # 后端容器化
├── docker-compose.yml       # MySQL + Redis + 后端编排
└── requirements.txt         # Python 依赖
```

## ReAct Agent 工作流

```
用户消息
  ↓
agent（LLM 思考 + 选择工具）
  ↓
should_continue（检查 tool_calls）
  ├── 有 → tools（执行：创建工单 / 查知识库）→ 回到 agent 再思考
  └── 没有 → 直接回复 → 结束
```

不再需要人工编写 if-else 路由，LLM 自主决定何时调工具、调哪个工具。

## 快速开始

### 1. 启动依赖服务

```bash
# MySQL（确保 3306 端口已启动）
# Redis
redis-server
```

### 2. 配置环境变量

复制 `.env` 文件，填入 DeepSeek API Key：

```
DEEPSEEK_API_KEY=your_key_here
```

### 3. 启动后端

```bash
pip install -r requirements.txt
python app/main.py
```

后端启动在 `http://localhost:8000`

### 4. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端启动在 `http://localhost:5173`

### 5. Docker 一键部署

```bash
docker compose up -d
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/chat` | 同步聊天 |
| POST | `/api/chat/stream` | 流式聊天（SSE） |
| GET | `/api/tickets` | 工单列表 |
| GET | `/api/tickets/{id}` | 工单详情 |
| GET | `/api/knowledge` | 知识库列表 |
| POST | `/api/knowledge` | 添加知识 |
| POST | `/api/knowledge/upload` | 上传 .txt 文件 |
| POST | `/api/knowledge/crawl` | 爬取网页入库 |
| DELETE | `/api/knowledge/{id}` | 删除知识 |

## 知识库

内置 35 条飞书常见问题 FAQ，覆盖：

- 账号与登录
- 消息与沟通
- 文档与协作
- 会议与日程
- 管理后台
- 考勤与审批
- 功能与设置

支持上传 `.txt` 文件自动切分入库（固定窗口 200 字，重叠 50 字）。
