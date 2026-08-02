# 🚀 AI Agent 开发工程师 · V3.0（官方文档标注版）

> **核心法则**：不要只看不敲。每天必须产出**可运行的** **`.py`** **文件**或 **Git 提交记录**。
> **技术栈替换**：把教程里的 OpenAI 换成 **DeepSeek API**（便宜/国内友好）或 **SiliconFlow**（聚合平台）。
>
> ⚠️ **本书标注说明**：📖 = 必读官方文档 | 🔧 = API 参考 | 🧪 = 动手实验
>
> 🇨🇳 **中国地区可用性**：本文中 OpenAI/Anthropic 官方文档链接均已替换为国内可访问的替代来源 —— DeepSeek 文档（兼容 OpenAI 格式）或 GitHub 仓库。如确需查阅原始文档，请自备代理工具。

---

## 🔥 第 1 周：裸写 ReAct + MCP 启蒙（手撕内功）

> **本周哲学**：不用任何框架，纯 `while True` 理解 Agent 灵魂。

- [X] **Day 1 (API 调通)** ：写 `call_llm.py`。用 `requests` 库调用 DeepSeek API，打印出 `choices[0].message.content`。**代码量 ≤ 20 行**。
    > 📖 **必读文档**：
    > - [DeepSeek API 官方文档](https://platform.deepseek.com/api-docs/) — 看 `/chat/completions` 端点
    > - [DeepSeek Chat API 参考](https://api-docs.deepseek.com/api/chat-completions) — DeepSeek 兼容 OpenAI 格式，理解 `messages`、`model`、`temperature` 字段的含义（国内可直连）
    > - [requests 库快速入门](https://requests.readthedocs.io/en/latest/user/quickstart/) — 看 POST 请求和 headers 怎么传

- [X] **Day 2 (角色扮演)** ：写 `chat_roles.py`。封装一个函数，分别传入 `system`（你是个翻译官）和 `user`（你好），观察输出差异。理解"系统提示词"的绝对控制权。
    > 📖 **必读文档**：
    > - [DeepSeek 消息结构文档](https://api-docs.deepseek.com/api/chat-completions) — 理解 `role` 字段的四种取值：`system`、`user`、`assistant`、`tool`（DeepSeek 与 OpenAI 消息格式完全兼容）
    > - [Prompt Engineering 指南（GitHub）](https://github.com/anthropics/anthropic-cookbook) — Anthropic 官方 Cookbook 中的提示词示例（GitHub 国内可直连）
    > - [DeepSeek 提示词指南](https://platform.deepseek.com/api-docs/) — 看 Prompting 章节

- [X] **Day 3 (工具定义)** ：写 `tools.py`。定义 2 个 JSON Schema 格式的工具：`get_current_time` 和 `calculator`。**重点**：把 Schema 写成严格的 JSON 结构。
    > 📖 **必读文档**：
    > - [OpenAI Function Calling / Tools 官方指南](https://api-docs.deepseek.com/guides/function_calling) — **极其重要！** 这是理解 `tools` 参数和 `tool_calls` 响应的核心文档。每一个 JSON 字段（`type`、`function`、`parameters`、`required`）为什么要这么写，这里全有解释
    > - [JSON Schema 规范](https://json-schema.org/learn/getting-started-step-by-step) — 理解 `type`、`properties`、`required` 的 JSON Schema 语法
    > - [DeepSeek Tool Calling 文档](https://platform.deepseek.com/api-docs/guides/function-calling) — DeepSeek 的工具调用兼容 OpenAI 格式

- [X] **Day 4 (手撕 ReAct 循环)** ：写 `react_loop.py`（核心！）。一个 `while` 循环：① 拼装消息列表 ② 调 API ③ 若返回 `tool_calls` 则执行本地函数 ④ 追加结果再次调 API。**代码量 150 行**。
    > 📖 **必读文档**：
    > - [OpenAI Tool Calling 完整流程](https://api-docs.deepseek.com/guides/function_calling) — 看 "Step-by-step" 部分，理解 ① send→② receive tool_call→③ append result→④ send again 这个循环
    > - [ReAct 原始论文 (Yao et al., 2022)](https://arxiv.org/abs/2210.03629) — 读 Abstract + Figure 1 即可，理解 Reasoning + Acting 交替的核心思想
    > - [Anthropic Tool Use 示例（GitHub）](https://github.com/anthropics/anthropic-cookbook) — 对比 Anthropic 的实现方式，理解不同模型工具调用的异同，看官方 Cookbook 中的示例

- [ ] **Day 5 (MCP 初体验)** ：安装 Node.js，跑通官方 MCP `filesystem` Server。在终端输入 `npx -y @modelcontextprotocol/server-filesystem /tmp` 看它是否启动成功。
    > 📖 **必读文档**：
    > - [MCP 协议官方文档](https://modelcontextprotocol.io/introduction) — **第一优先级！** 理解 MCP 是什么、Client/Server 架构、三大核心概念（Tools、Resources、Prompts）
    > - [MCP 快速入门](https://modelcontextprotocol.io/quickstart) — 跟着官方 Quickstart 走一遍
    > - [MCP Filesystem Server 源码](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) — 看看官方 Server 是怎么实现的
    > - [Node.js 下载页](https://nodejs.org/) — 如果没有装 Node.js，从这里下载 LTS 版本

- [ ] **Day 6 (MCP Client 嫁接)** ：写 `mcp_client.py`。用 Python `subprocess` 启动 Day 5 的 MCP Server，并发送 `list_tools` 请求。**不需要调通完整调用，只要能连上就行**。
    > 📖 **必读文档**：
    > - [MCP Python SDK 文档](https://github.com/modelcontextprotocol/python-sdk) — **核心！** Python 端的 MCP 实现，看 `README.md` 的 Client 示例
    > - [MCP 协议规范 - JSON-RPC 传输层](https://spec.modelcontextprotocol.io/specification/2025-03-26/basic/transports/) — 理解 stdio 传输协议，知道 MCP 消息是怎么通过 stdin/stdout 传递的
    > - [Python subprocess 官方文档](https://docs.python.org/3/library/subprocess.html) — 理解 `Popen`、`stdin`、`stdout` 的用法

- [ ] **Day 7 (实验与笔记)** ：跑通路线图 B 的"实验 1-1"，故意去掉工具结果传给模型，记录模型"胡言乱语"的截图。在 GitHub 建仓库，提交 `week1` 文件夹。
    > 📖 **必读文档**：
    > - [API 错误处理](https://api-docs.deepseek.com/quick_start/error_codes) — DeepSeek 错误码说明：429（限流）、401（认证失败）、503（服务过载）
    > - [Git 入门 - 廖雪峰教程](https://www.liaoxuefeng.com/wiki/896043488029600) — 如果 Git 还不熟，看前 6 章

---

## 📚 第 2 周：2026 新范式 RAG + 轻量评估

> **本周哲学**：不再死磕分块大小，直接上混合检索和上下文检索。

- [ ] **Day 8 (向量化基础)** ：写 `embedding_demo.py`。用 `sentence-transformers/all-MiniLM-L6-v2` 将 3 句话转成向量，用 `numpy` 计算两两之间的余弦相似度。
    > 📖 **必读文档**：
    > - [Sentence-Transformers 官方文档](https://www.sbert.net/docs/quickstart.html) — 看 "Quickstart" 和 "Computing Sentence Embeddings"
    > - [Sentence-Transformers 文档 - Embeddings 概念](https://www.sbert.net/docs/quickstart.html) — 理解什么是 embedding 向量、为什么用余弦相似度（本地运行，无需 API）
    > - [余弦相似度 - 维基百科](https://en.wikipedia.org/wiki/Cosine_similarity) — 理解数学公式及为什么用余弦而非欧氏距离
    > - [NumPy 快速入门](https://numpy.org/doc/stable/user/quickstart.html) — 看数组运算和 `np.dot` 用法

- [ ] **Day 9 (混合检索实战)** ：用 `pip install rank_bm25`。写一个 `HybridSearcher` 类，输入问题，分别取 BM25 结果和 向量结果，用 `Reciprocal Rank Fusion (RRF)` 合并排序。
    > 📖 **必读文档**：
    > - [BM25 算法 - Elasticsearch 解释](https://www.elastic.co/blog/practical-bm25-part-1-how-shards-affect-relevance-scoring-in-elasticsearch) — 理解词频/逆文档频率
    > - [rank_bm25 库文档](https://github.com/dorianbrown/rank_bm25) — 看用法示例
    > - [RRF 论文/算法解释](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) — 理解为什么 RRF 比简单加权排序更好
    > - [ChromaDB 官方文档](https://docs.trychroma.com/getting-started) — 轻量向量数据库，后续要用

- [ ] **Day 10 (Contextual Retrieval)** ：读 Anthropic 关于上下文检索的官方博客。取一篇长文档，把每个分块的前面加上"这段文本的上下文是：..."（手动或调用 LLM 生成），重新建索引。
    > 📖 **必读文档**：
    > - [Anthropic Contextual Retrieval 博客](https://www.anthropic.com/news/contextual-retrieval) — **本周核心！** 理解为什么给 chunk 加上下文前缀能大幅提升检索质量
    > - [LangChain Text Splitters 文档](https://python.langchain.com/docs/how_to/#text-splitters) — 看看有哪些分块策略（RecursiveCharacterTextSplitter、SemanticChunker等）
    > - [Chunking 策略对比 (Pinecone 博客)](https://www.pinecone.io/learn/chunking-strategies/) — 理解不同分块策略的优劣

- [ ] **Day 11 (文档加载器)** ：写 `pdf_loader.py`。用 `pypdf` 或 `docling` 读取一份本地 PDF，按标题层级切分（而不是固定字符数），输出结构化的 JSON。
    > 📖 **必读文档**：
    > - [pypdf 官方文档](https://pypdf.readthedocs.io/en/stable/) — 看 "Extracting Text" 章节
    > - [Docling (IBM) 官方文档](https://ds4sd.github.io/docling/) — 支持 PDF → Markdown/JSON 高级转换
    > - [LangChain Document Loaders](https://python.langchain.com/docs/how_to/#document-loaders) — 了解各种文档加载器（PDF、CSV、HTML等），但不要依赖 LangChain，理解原理后自己写

- [ ] **Day 12 (评估脚本 - LLM as Judge)** ：写 `eval_script.py`。准备 10 个"问题-标准答案"对。调 LLM 给 RAG 回答打分（1-10 分），计算平均分和命中率。
    > 📖 **必读文档**：
    > - [OpenAI Evals 框架](https://github.com/openai/evals) — 看评估方法论
    > - [RAGAS 评估框架文档](https://docs.ragas.io/en/stable/) — **重点！** 理解 RAG 的三个评估维度：Faithfulness（忠实度）、Answer Relevancy（答案相关性）、Context Precision（上下文精确度）
    > - [LLM-as-Judge 论文 (Zheng et al., 2023)](https://arxiv.org/abs/2306.05685) — 理解用 LLM 做评估的可靠性

- [ ] **Day 13 (挂载 RAG 工具)** ：将 Day 9-12 做的检索器，封装成 `rag_query` 工具函数。在控制台手动测试：输入问题 -> 检索 -> 调 LLM 回答。
    > 📖 **必读文档**：
    > - [DeepSeek Tool Schema 定义最佳实践](https://api-docs.deepseek.com/guides/function_calling) — 写工具描述时，如何让 LLM 更好地理解和使用工具
    > - [RAG 管道设计模式](https://www.llamaindex.ai/blog/a-cheat-sheet-and-some-recipes-for-building-advanced-rag-803a9d94c41) — LlamaIndex 的 RAG Cheat Sheet

- [ ] **Day 14 (集成测试)** ：把上周的 `react_loop.py` 拉过来，把 `rag_query` 加入工具列表。测试一个"需要查资料的数学题"（比如"2024年诺贝尔物理学奖得主是谁？计算他年龄的平方"）。
    > 🧪 **实验记录**：
    > 记录以下内容到笔记：
    > 1. Agent 先调了哪个工具？为什么？
    > 2. 工具返回结果后，Agent 的推理过程是什么？
    > 3. 有没有出现死循环？如果有，在哪一步？

---

## ⚙️ 第 3 周：LangGraph + 完整项目（研究助手）

> **本周哲学**：放弃 LCEL 链，拥抱 StateGraph（有状态图）。

- [ ] **Day 15 (LangGraph 入门)** ：跑通 LangGraph 官方"Agent with Tools"教程。不要复制，手动敲一遍 `StateGraph`、`Node`、`Edge` 的定义。
    > 📖 **必读文档**：
    > - [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/) — **本周圣经！** 先看 "Quick Start" 和 "Tutorials"
    > - [LangGraph 概念指南（State、Nodes、Edges）](https://langchain-ai.github.io/langgraph/concepts/low_level/) — 理解 `StateGraph`、`Node`、`Edge`、`ConditionalEdge` 的核心概念
    > - [LangGraph 源码 (GitHub)](https://github.com/langchain-ai/langgraph) — 如果文档看不懂，直接看源码中的 examples

- [ ] **Day 16 (状态设计)** ：设计自己的 `AgentState` 字典，包含 `messages`（历史）、`step_count`（步数）、`intermediate_steps`（中间轨迹）。
    > 📖 **必读文档**：
    > - [LangGraph State 管理文档](https://langchain-ai.github.io/langgraph/concepts/low_level/#state) — 理解 `TypedDict` vs `Pydantic` 两种 State 定义方式
    > - [LangGraph Reducer 函数](https://langchain-ai.github.io/langgraph/concepts/low_level/#reducers) — 理解 `add_messages` reducer 如何自动合并消息列表
    > - [Python TypedDict 官方文档](https://docs.python.org/3/library/typing.html#typing.TypedDict) — 基础语法

- [ ] **Day 17 (项目骨架)** ：创建 `fastapi_research_assistant` 目录。写 `main.py`，挂载 3 个路由：`/chat`（流式响应）、`/history`、`/health`。
    > 📖 **必读文档**：
    > - [FastAPI 官方文档](https://fastapi.tiangolo.com/) — **必读！** 看 "First Steps"、Path Parameters、Request Body、Streaming Response
    > - [FastAPI Streaming Response](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse) — 理解 SSE（Server-Sent Events）实现流式输出
    > - [Pydantic V2 文档](https://docs.pydantic.dev/latest/) — FastAPI 使用 Pydantic 做数据校验，理解 `BaseModel`
    > - [uvicorn 文档](https://www.uvicorn.org/) — ASGI 服务器，理解热重载、worker 数量等参数

- [ ] **Day 18 (工具集成)** ：注册 3 个工具：① **Tavily/Bocha 搜索 API** ② **`requests.get`** **抓取网页内容** ③ **`pathlib`** **写 Markdown 文件**。在本机调试工具函数。
    > 📖 **必读文档**：
    > - [Tavily Search API 文档](https://docs.tavily.com/) — Agent 专用搜索引擎，理解 `search_depth`（basic vs advanced）
    > - [Bocha (博查) API 文档](https://open.bochaai.com/) — 国内替代，中文搜索更好
    > - [BeautifulSoup 4 文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) — 解析网页 HTML，提取正文内容
    > - [httpx 文档](https://www.python-httpx.org/) — 现代化的 HTTP 客户端，支持 async
    > - [LangGraph ToolNode 文档](https://langchain-ai.github.io/langgraph/how-tos/tool-calling/) — 看 LangGraph 如何管理工具

- [ ] **Day 19 (记忆模块)** ：引入 `langgraph.checkpoint` 或手动维护 `dict` 存储 session_id。让 Agent 记住前 3 轮对话。
    > 📖 **必读文档**：
    > - [LangGraph Persistence / Checkpoint 文档](https://langchain-ai.github.io/langgraph/concepts/persistence/) — **核心！** 理解 `MemorySaver` 和 `SqliteSaver` 的区别
    > - [LangGraph 多轮对话教程](https://langchain-ai.github.io/langgraph/how-tos/memory/manage-conversation-history/) — 管理对话历史
    > - [对话记忆设计模式 (LangChain Memory 文档)](https://langchain-ai.github.io/langgraph/concepts/memory/) — 理解 short-term vs long-term memory

- [ ] **Day 20 (E2B 沙箱执行 - 高分亮点)** ：注册 `python_repl` 工具。**不要用** **`exec`**！去 `e2b.dev` 拿 SDK，让 Agent 生成的代码在远端隔离沙箱运行。**简历必写这一条**。
    > 📖 **必读文档**：
    > - [E2B 官方文档](https://e2b.dev/docs) — **本周亮点！** 看 Python SDK 的 Code Interpreter 章节
    > - [E2B Code Interpreter 快速入门](https://e2b.dev/docs/code-interpreter/overview) — 理解沙箱的生命周期（create → run → get output → close）
    > - [E2B Python SDK API 参考](https://e2b.dev/docs/code-interpreter/api-reference) — 在沙箱中如何安装包、执行代码、获取文件
    > - [安全最佳实践：代码执行的隔离策略](https://e2b.dev/docs/security) — 理解 E2B 的隔离机制（网络隔离、超时、资源限制）

- [ ] **Day 21 (项目打包)** ：写 `Dockerfile`，把项目装进容器。在本地跑通 `docker build -t agent-api .`。
    > 📖 **必读文档**：
    > - [Docker 官方文档 - Get Started](https://docs.docker.com/get-started/) — 理解 Image、Container、Dockerfile 的概念
    > - [Dockerfile 最佳实践](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) — **必读！** 多阶段构建、层级缓存、`.dockerignore`
    > - [Python Docker 官方镜像](https://hub.docker.com/_/python) — 了解不同 tag（slim、alpine）的含义

---

## 🚦 第 4 周：生产化轻量化（缓存+监控+回归）

> **本周哲学**：让项目看起来像"线上服务"，而非"Jupyter Notebook"。

- [ ] **Day 22 (Redis 缓存)** ：用 Docker 跑起 Redis。写装饰器 `@cache(ttl=300)`，缓存 LLM 的重复请求（比如同样的"什么是 Agent"问两次，第二次直接走缓存）。
    > 📖 **必读文档**：
    > - [Redis 官方文档](https://redis.io/docs/latest/) — 看数据结构（string、hash）和 TTL
    > - [redis-py 文档](https://redis-py.readthedocs.io/en/stable/) — Python Redis 客户端
    > - [Redis Docker 镜像](https://hub.docker.com/_/redis) — `docker run -d -p 6379:6379 redis`
    > - [LLM 缓存模式 - GPTCache 项目](https://github.com/zilliztech/GPTCache) — 了解语义缓存 vs 精确缓存的区别

- [ ] **Day 23 (异步改造)** ：把 `main.py` 中的路由全改成 `async def`。把搜索 API 调用、网页抓取改成 `httpx.AsyncClient`。对比改造前后的响应时间。
    > 📖 **必读文档**：
    > - [FastAPI 异步指南](https://fastapi.tiangolo.com/async/) — **必读！** 理解 `async def` vs `def`、什么时候用 async
    > - [httpx AsyncClient 文档](https://www.python-httpx.org/async/) — 异步 HTTP 请求的正确姿势
    > - [Python asyncio 官方文档](https://docs.python.org/3/library/asyncio.html) — 理解事件循环、`await`、`asyncio.gather`
    > - [asyncio 并发 vs 并行](https://docs.python.org/3/library/asyncio-dev.html) — 理解 GIL 和 async 的适用场景

- [ ] **Day 24 (LangSmith 追踪)** ：注册 LangSmith 账号（免费）。在环境变量设置 `LANGCHAIN_TRACING_V2=true`，跑一次对话，去官网查看完整的"Chain/LLM/Tool"调用瀑布图。
    > 📖 **必读文档**：
    > - [LangSmith 官方文档](https://docs.smith.langchain.com/) — **必读！** 注册后看 Tracing 和 Projects
    > - [LangSmith Quickstart](https://docs.smith.langchain.com/tracing/quickstart) — 5 分钟上手追踪
    > - [LangSmith Tracing 概念](https://docs.smith.langchain.com/tracing/concepts) — 理解 Run、Trace、Span 的关系
    > - [OpenTelemetry 基础](https://opentelemetry.io/docs/concepts/observability-primer/) — 理解 Traces、Metrics、Logs 三支柱（可选，进阶）

- [ ] **Day 25 (Prometheus 指标)** ：用 `prometheus-client` 暴露 `/metrics` 端点。打上 3 个自定义指标：`agent_requests_total`、`llm_token_usage`、`tool_call_errors_total`。
    > 📖 **必读文档**：
    > - [Prometheus Client Python 官方文档](https://github.com/prometheus/client_python) — Counter、Histogram、Gauge 三种指标类型
    > - [Prometheus 指标命名最佳实践](https://prometheus.io/docs/practices/naming/) — 指标怎么命名才规范
    > - [FastAPI 集成 Prometheus](https://github.com/trallnag/prometheus-fastapi-instrumentator) — 开箱即用的 FastAPI 指标采集
    > - [Prometheus 查询语言 PromQL 入门](https://prometheus.io/docs/prometheus/latest/querying/basics/) — 理解怎么查指标

- [ ] **Day 26 (自动化回归测试)** ：写 `test_regression.py`。固定 10 条高频提问。调用你的 API，判断输出的 JSON 是否包含"result"字段，且耗时 < 20 秒。**未来改代码后跑一遍，防劣化**。
    > 📖 **必读文档**：
    > - [pytest 官方文档](https://docs.pytest.org/en/stable/) — 测试框架，看 fixtures 和 parametrize
    > - [pytest-asyncio](https://pytest-asyncio.readthedocs.io/en/latest/) — 测试异步 API
    > - [pytest-timeout](https://github.com/pytest-dev/pytest-timeout) — 设置测试超时
    > - [CI/CD 中的回归测试](https://docs.github.com/en/actions/automating-builds-and-tests) — GitHub Actions 自动化运行测试

- [ ] **Day 27 (Docker Compose 全家桶)** ：写 `docker-compose.yml`，里面包含：`api`（你的 FastAPI）+ `redis` + `chromadb`。一键 `docker-compose up -d` 拉起全部服务。
    > 📖 **必读文档**：
    > - [Docker Compose 官方文档](https://docs.docker.com/compose/) — 理解 services、networks、volumes
    > - [Compose File 参考](https://docs.docker.com/compose/compose-file/) — **必读！** 理解每个配置项的含义（`depends_on`、`healthcheck`、`environment`）
    > - [Docker Compose 最佳实践](https://docs.docker.com/compose/production/) — 生产环境注意事项

- [ ] **Day 28 (项目文档与截图)** ：写 `README.md`，必须包含：① 系统架构图（用 Mermaid 画）；② 性能压测数据（Day 23 异步前后的对比表格）；③ 1 分钟 Demo 录屏的链接（传 B站/YouTube 私有）。
    > 📖 **必读文档**：
    > - [Mermaid 语法指南](https://mermaid.js.org/intro/) — **非常实用！** 画架构图、流程图、时序图
    > - [GitHub Mermaid 支持](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) — GitHub 直接渲染 Mermaid 图
    > - [开源项目 README 最佳实践](https://www.makeareadme.com/) — 写一个专业的 README

---

## 🎯 第 5 周：面试冲刺与简历核弹

> **本周哲学**：把"做过"变成"讲得清、问不倒"。

- [ ] **Day 29 (深挖 - MCP 题)** ：准备面试回答："MCP 相比 Function Calling 有什么优势？"（答：解耦工具与模型、标准化协议、本地资源访问安全）。
    > 📖 **必读文档**：
    > - [MCP 协议架构设计](https://modelcontextprotocol.io/docs/concepts/architecture) — 理解 Client/Server 架构
    > - [MCP vs Function Calling 对比分析 (Anthropic 官方博客)](https://www.anthropic.com/news/model-context-protocol) — MCP 的设计初衷
    > - [MCP 安全模型](https://modelcontextprotocol.io/docs/concepts/security) — 理解权限控制、数据隔离

- [ ] **Day 30 (深挖 - 安全题)** ：准备面试回答："Agent 执行代码时如何防止注入攻击？"（答：E2B 沙箱隔离 + 限制网络端口 + 超时自动 Kill）。
    > 📖 **必读文档**：
    > - [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) — **必读！** LLM 应用的十大安全风险
    > - [E2B 安全架构](https://e2b.dev/docs/security) — 沙箱隔离的具体机制
    > - [Prompt Injection 防御指南](https://learnprompting.org/docs/prompt_hacking/intro) — 理解间接注入、越狱攻击

- [ ] **Day 31 (深挖 - 评估题)** ：准备面试回答："你怎么知道 Agent 变好了还是变坏了？"（答：建立轨迹评估 + 端到端成功率监控，每次发布前跑回归测试集）。
    > 📖 **必读文档**：
    > - [LLM Evaluation 综述 (Hugging Face 博客)](https://huggingface.co/blog/clefourrier/llm-evaluation) — 评估方法论全景
    > - [Agent 评估最佳实践 (Anthropic 博客)](https://www.anthropic.com/engineering/evaluating-agents) — 业界标准做法
    > - [RAGAS 评估框架](https://docs.ragas.io/en/stable/) — RAG 特定评估

- [ ] **Day 32 (简历 STAR 重写)** ：按格式写项目：
    *S（背景）：投研报告依赖人工，效率低。* 
    *T（任务）：构建自动化研究助手。* 
    *A（行动）：基于 LangGraph + MCP协议 + E2B沙箱。* 
    *R（结果）：任务成功率 90%，平均耗时从 15分钟 降至 15秒。*
    > 📖 **推荐阅读**：
    > - [STAR 面试法详解](https://www.themuse.com/advice/star-interview-method) — 理解 Situation/Task/Action/Result
    > - [技术简历写作指南](https://www.careercup.com/resume) — 硅谷技术简历标准

- [ ] **Day 33 (模拟面试 1)** ：找朋友/同学，让他对着简历问"你遇到过最大的技术挑战是什么？"。你回答"Agent 死循环"或"PDF 表格解析乱码"并讲出排查过程。
    > 🧪 **准备清单**：
    > 1. 准备 3 个你亲手 Debug 过的技术难题
    > 2. 每个难题用 STAR 格式写出回答
    > 3. 录下来回听，确保逻辑清晰

- [ ] **Day 34 (模拟面试 2)** ：打开手机录音，自问自答"请用 3 分钟介绍你的研究助手项目"。录完后回听，删掉所有"嗯、啊、然后"，做到流畅无卡顿。
    > 🧪 **自检清单**：
    > - [ ] 开头 15 秒说清楚项目是什么
    > - [ ] 中间 1.5 分钟讲技术架构（用 Mermaid 图）
    > - [ ] 中间 1 分钟讲遇到的挑战和解决方案
    > - [ ] 最后 15 秒总结成果和收获

- [ ] **Day 35 (投递启动)** ：在牛客网、BOSS直聘、各大厂招聘官网，搜索"AI应用开发实习生"、"大模型应用开发"、"Agent开发"批量投递。**把 Day 32 的简历文字复制到附件第一页**。
    > 📖 **投递渠道**：
    > - [牛客网](https://www.nowcoder.com/) — 校招/实习
    > - [BOSS直聘](https://www.zhipin.com/) — 社招
    > - [各大厂校招官网](https://github.com/ByteByteGoHq/system-design-101) — 各公司招聘进度跟踪

---

## 🛠️ 核心参考链接速查表（贴在你的显示器旁）

| 类别 | 名称 | 直达链接/命令 |
| :--- | :--- | :--- |
| **大模型 API** | DeepSeek (首选) | `https://platform.deepseek.com/api-docs` |
| **大模型 API** | DeepSeek API 文档（兼容 OpenAI 格式） | `https://api-docs.deepseek.com/` |
| **大模型 API** | Anthropic Cookbook（GitHub，国内可直连） | `https://github.com/anthropics/anthropic-cookbook` |
| **MCP 协议** | MCP 官方文档 | `https://modelcontextprotocol.io/introduction` |
| **MCP 协议** | MCP 协议规范 | `https://spec.modelcontextprotocol.io/` |
| **MCP Server** | 本地文件系统 (测试用) | 终端执行 `npx -y @modelcontextprotocol/server-filesystem /tmp` |
| **MCP Python** | Python SDK | `https://github.com/modelcontextprotocol/python-sdk` |
| **编排框架** | LangGraph 官方教程 | `https://langchain-ai.github.io/langgraph/` |
| **编排框架** | LangGraph GitHub | `https://github.com/langchain-ai/langgraph` |
| **编排框架** | LangSmith 追踪 | `https://smith.langchain.com/` |
| **Web 框架** | FastAPI 官方文档 | `https://fastapi.tiangolo.com/` |
| **沙箱执行** | E2B Code Interpreter | `https://e2b.dev/docs/code-interpreter/overview` |
| **向量库** | ChromaDB 官方文档 | `https://docs.trychroma.com/getting-started` |
| **向量模型** | Sentence-Transformers | `https://www.sbert.net/docs/quickstart.html` |
| **搜索 API** | Tavily Search API | `https://docs.tavily.com/` |
| **搜索 API** | Bocha (博查) | `https://open.bochaai.com/` |
| **HTTP 客户端** | httpx 文档 | `https://www.python-httpx.org/` |
| **测试** | pytest 官方文档 | `https://docs.pytest.org/en/stable/` |
| **监控** | Prometheus Python Client | `https://github.com/prometheus/client_python` |
| **Docker** | Docker 入门 | `https://docs.docker.com/get-started/` |
| **Git** | 廖雪峰 Git 教程 | `https://www.liaoxuefeng.com/wiki/896043488029600` |
| **绘图** | Mermaid 语法 | `https://mermaid.js.org/intro/` |
| **安全** | OWASP LLM Top 10 | `https://genai.owasp.org/llm-top-10/` |
| **评估** | RAGAS 框架 | `https://docs.ragas.io/en/stable/` |
