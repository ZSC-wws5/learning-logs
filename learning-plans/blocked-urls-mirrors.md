# 🔗 被墙链接 → 替代链接 对照表

> 这份清单记录了学习计划中所有被中国大陆防火墙屏蔽的原始链接，以及对应的国内可访问替代方案。
>
> **使用方式**：日常学习用替代链接；想查阅原始官方文档时，挂代理后访问"原始链接"列。

---

## OpenAI 平台（`platform.openai.com` ← 被墙）

| 用途 | 原始链接（需代理） | 替代链接（国内可直连） | 说明 |
|:---|:---|:---|:---|
| API 参考总览 | <https://platform.openai.com/docs/api-reference> | <https://api-docs.deepseek.com/> | DeepSeek 与 OpenAI 格式完全兼容 |
| Chat API 创建对话 | <https://platform.openai.com/docs/api-reference/chat/create> | <https://api-docs.deepseek.com/api/chat-completions> | 参数含义完全一致 |
| 消息结构（roles） | <https://platform.openai.com/docs/api-reference/chat/create#chat-create-messages> | <https://api-docs.deepseek.com/api/chat-completions> | system/user/assistant/tool 四种 role |
| Function Calling 总览 | <https://platform.openai.com/docs/guides/function-calling> | <https://api-docs.deepseek.com/guides/function_calling> | JSON Schema 定义方式相同 |
| Function Calling 分步教程 | <https://platform.openai.com/docs/guides/function-calling?lang=python> | <https://api-docs.deepseek.com/guides/function_calling> | DeepSeek 无 Python tab，看代码示例即可 |
| Function Calling 最佳实践 | <https://platform.openai.com/docs/guides/function-calling#function-definition-best-practices> | <https://api-docs.deepseek.com/guides/function_calling> | 描述撰写的技巧通用 |
| Embeddings API | <https://platform.openai.com/docs/guides/embeddings> | <https://www.sbert.net/docs/quickstart.html> | 本地 Sentence-Transformers，无需 API Key |
| Streaming 流式输出 | <https://platform.openai.com/docs/api-reference/streaming> | <https://api-docs.deepseek.com/guides/streaming> | SSE 协议一致 |
| Error Codes 错误码 | <https://platform.openai.com/docs/guides/error-codes> | <https://api-docs.deepseek.com/quick_start/error_codes> | HTTP 状态码通用（429/401/503） |
| Tokenizer 可视化 | <https://platform.openai.com/tokenizer> | <https://github.com/openai/tiktoken> | 本地 Python 库，功能更强 |

---

## Anthropic 文档（`docs.anthropic.com` ← 被墙）

| 用途 | 原始链接（需代理） | 替代链接（国内可直连） | 说明 |
|:---|:---|:---|:---|
| Anthropic API 总览 | <https://docs.anthropic.com/en/api> | <https://github.com/anthropics/anthropic-cookbook> | GitHub 仓库含完整 Jupyter Notebook 示例 |
| System Prompts 指南 | <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts> | <https://github.com/anthropics/anthropic-cookbook> | Cookbook 中的 prompt-engineering 目录 |
| Tool Use 文档 | <https://docs.anthropic.com/en/docs/build-with-claude/tool-use> | <https://github.com/anthropics/anthropic-cookbook> | Cookbook 中的 tool-use 目录 |
| Tool Use 工作原理 | <https://docs.anthropic.com/en/docs/build-with-claude/tool-use#how-tool-use-works> | <https://github.com/anthropics/anthropic-cookbook> | 同上 |

---

## OpenAI Cookbook（`cookbook.openai.com` ← 被墙）

| 用途 | 原始链接（需代理） | 替代链接（国内可直连） | 说明 |
|:---|:---|:---|:---|
| Cookbook 主页 | <https://cookbook.openai.com/> | <https://github.com/openai/openai-cookbook> | 同一仓库，GitHub 渲染 Markdown |
| Tool Calling 示例 | <https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models> | <https://github.com/openai/openai-cookbook> | examples 目录中找同名文件 |

---

## Anthropic 博客（`www.anthropic.com` ← 可能被墙/很慢）

这些是 Anthropic 官方博客文章，内容独特，没有一对一替代。建议挂代理访问。

| 用途 | 链接 | 国内替代建议 |
|:---|:---|:---|
| MCP 协议发布公告 | <https://www.anthropic.com/news/model-context-protocol> | 读 [MCP 官方文档](https://modelcontextprotocol.io/) 即可替代 |
| Contextual Retrieval 技术博客 | <https://www.anthropic.com/news/contextual-retrieval> | 国内技术社区搜"上下文检索"有大量中文解读 |
| Evaluating Agents 最佳实践 | <https://www.anthropic.com/engineering/evaluating-agents> | 搜"Agent 评估"或读 [RAGAS 文档](https://docs.ragas.io/) |

---

## 其他始终可直连的资源

这些链接在国内一直可以正常访问，不需要代理：

| 资源 | 链接 | 说明 |
|:---|:---|:---|
| DeepSeek API 文档 | <https://api-docs.deepseek.com/> | 首选 API 文档 |
| DeepSeek 平台 | <https://platform.deepseek.com/> | API Key 管理 |
| MCP 协议文档 | <https://modelcontextprotocol.io/> | MCP 官方站 |
| MCP Python SDK | <https://github.com/modelcontextprotocol/python-sdk> | GitHub |
| LangGraph 文档 | <https://langchain-ai.github.io/langgraph/> | LangChain 系 |
| FastAPI 文档 | <https://fastapi.tiangolo.com/> | 独立站 |
| E2B 文档 | <https://e2b.dev/docs> | 沙箱服务 |
| ChromaDB 文档 | <https://docs.trychroma.com/> | 向量数据库 |
| Sentence-Transformers | <https://www.sbert.net/> | 本地 Embedding |
| pytest 文档 | <https://docs.pytest.org/> | Python 测试 |
| Docker 文档 | <https://docs.docker.com/> | 容器化 |
| Prometheus 文档 | <https://prometheus.io/> | 监控 |
| Mermaid 文档 | <https://mermaid.js.org/> | 画图 |
| ArXiv 论文 | <https://arxiv.org/> | 学术论文，始终可访问 |
| GitHub（主站） | <https://github.com/> | 代码托管，基础访问正常 |

---

## 📌 速记规则

> - **OpenAI 官方文档被墙** → 用 **DeepSeek 文档**替代（API 格式 100% 兼容）
> - **Anthropic 文档被墙** → 用 **GitHub Anthropic Cookbook** 替代（同内容的 Jupyter Notebook）
> - **OpenAI Cookbook 被墙** → 用 **GitHub OpenAI Cookbook** 替代（完全相同的仓库）
> - **博客文章**（`www.anthropic.com/news`）→ 挂代理或搜中文解读
> - **GitHub 仓库** → 基本都能直连，偶尔慢但不会完全断
