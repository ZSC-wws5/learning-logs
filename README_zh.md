# Python Agent 学习仓库

> 📚 **仅供个人学习使用**，所有代码均为学习过程中的练习与笔记，请勿用于生产环境。

本仓库记录了作者从 **Python 基础语法** 到 **构建 LLM Agent（工具调用 / ReAct 模式）** 的完整学习过程，循序渐进地覆盖了：

- Python 基础（函数、类、推导式、集合操作）
- 异步编程（`async` / `await`）
- 网络请求（`requests` 同步 / `aiohttp`、`httpx` 异步）
- 文件读写、异常处理
- 调用 DeepSeek API（OpenAI SDK）
- 工具定义（Tool Schema）+ ReAct 循环（手写推理-行动循环）
- Python 工程化（`uv` 依赖管理、包结构、`console script` 入口点）
- Web 框架（FastAPI）

---

## 📁 目录结构

```
Agent/
├── 示例代码/                      # 基础语法小练习
│   ├── async.py                 # 异步协程初体验
│   ├── aiohttp-demo.py          # aiohttp 通用请求封装（GET/POST）
│   └── 草稿.py                   # 草稿笔记
├── Agent_demo/                   # LLM Agent 示例（直接可运行）
│   ├── 00-Demo.py               # aiohttp 异步调用 + rich 美化输出
│   ├── 01-call_LLM.py           # requests 同步调用（情感分析师角色）
│   ├── 02-chat_roles.py         # system 角色设定示例（翻译官）
│   ├── 03-llm_tools_ReAct.py    # 🔧 工具调用入门：ReAct 模式详解
│   ├── 03.1-llm_tools_ReAct.py  # 🔧 工具调用进阶：get_weather + get_time
│   └── react_loop.py            # ReAct 循环（OpenAI SDK + 工具调用）
├── FastAPI/                      # FastAPI Web 框架练习
│   └── first_app.py             # 第一个 FastAPI 应用（GET 接口 + 路径参数）
├── file_report/                  # 📦 Python 包：集合操作 + httpx 请求练习
│   ├── __init__.py              # 包初始化
│   ├── config.py                # pydantic-settings 配置（从 .env 读取）
│   ├── client.py                # httpx 请求 GitHub API（重试 + 指数退避）
│   ├── func.py                  # 集合操作（词频/过滤/分组/扁平化/反转映射）
│   └── main.py                  # 生成 GitHub 仓库报告 + 入口点 main()
├── pyproject.toml                # 项目配置（uv 管理 + 依赖 + 入口点）
├── uv.lock                       # 依赖锁定文件（由 uv 生成）
├── .env.example                  # 环境变量配置示例
└── .gitignore
```

---

## 🚀 环境准备

**Python 版本：** 3.11+

本项目使用 [uv](https://docs.astral.sh/uv/) 管理依赖与运行环境：

```bash
# 1. 同步依赖（自动创建虚拟环境并安装）
uv sync

# 2. 运行入口点（见下方「file_report 包」）
uv run file-report
```

主要依赖：

| 库 | 用途 |
|:---|:---|
| `openai` | OpenAI SDK，用于调用 DeepSeek API（兼容接口） |
| `aiohttp` | 异步 HTTP 客户端 |
| `httpx` | 现代 HTTP 客户端（openai SDK 底层使用，`file_report` 请求 GitHub） |
| `requests` | 同步 HTTP 客户端 |
| `pydantic` / `pydantic-settings` | 数据校验与 `.env` 配置读取 |
| `python-dotenv` | 从 `.env` 文件加载环境变量 |
| `rich` | 终端美化输出 |
| `certifi` | 提供 CA 根证书，解决 HTTPS 校验问题 |
| `fastapi` / `uvicorn` | Web 框架与 ASGI 服务器 |
| `ruff`（dev） | 代码检查与格式化 |

---

## 🔑 配置 API Key

本项目通过 DeepSeek API 调用大模型，调用 LLM 的示例（`Agent_demo/`）需要配置密钥：

1. 复制 `.env.example` 为 `.env`：

   ```bash
   cp .env.example .env   # Windows 下复制后重命名即可
   ```

2. 编辑 `.env`，填入你的真实配置：

   ```ini
   DEEPSEEK_API_KEY=你的_DeepSeek_API_Key
   BASE_URL=https://api.deepseek.com/
   MODEL=deepseek-flash
   TEMPERATURE=0.7
   MAX_TOKENS=4096
   ```

> ⚠️ **注意**：`.env` 已加入 `.gitignore`，不会被提交到 Git，但请务必不要在任何渠道泄露你的 API Key。

---

## ▶️ 运行示例

```bash
# Agent 示例（需要 .env 配置了真实 Key）
uv run python Agent_demo/00-Demo.py              # aiohttp 异步 + rich 美化
uv run python Agent_demo/01-call_LLM.py          # requests 同步 + 情感分析师角色
uv run python Agent_demo/02-chat_roles.py        # system 角色设定：翻译官
uv run python Agent_demo/03-llm_tools_ReAct.py   # 🔧 工具调用入门：ReAct 模式详解
uv run python Agent_demo/03.1-llm_tools_ReAct.py # 🔧 工具调用进阶：多工具协作

# FastAPI 示例（先进入 FastAPI 目录，再以模块名启动）
cd FastAPI
uv run uvicorn first_app:app --reload            # 启动开发服务器

# file_report 包（通过入口点运行，见下方说明）
uv run file-report
```

---

## 📦 file_report 包

`file_report/` 是一个**标准的 Python 包**，用于练习「集合操作 + httpx 请求」的组合，并以 **console script 入口点**方式运行。

### 模块职责

| 模块 | 职责 |
|:---|:---|
| `config.py` | `Settings` 类（pydantic-settings）从 `.env` 读取配置，含 `github_api_base` / `timeout` / `repo` 默认值 |
| `client.py` | `fetch_repo()` 用 httpx 请求 GitHub 仓库信息，带 `User-Agent`、`certifi` 证书校验、**重试 + 指数退避** |
| `func.py` | 集合操作练习：词频统计、过滤、按长度分组、列表扁平化、dict 反转映射 |
| `main.py` | `build_report()` 汇总仓库 stars / 语言 / 描述 / 高频词，`main()` 用 logging 输出报告 |

### 运行方式

入口点在 `pyproject.toml` 中声明：

```toml
[project.scripts]
file-report = "file_report.main:main"
```

```bash
uv run file-report        # 默认抓取 pallets/flask 仓库并生成报告
```

可通过 `.env` 覆盖目标仓库（也可直接用默认值）：

```ini
REPO=psf/requests        # 自定义仓库
TIMEOUT=15.0             # 请求超时
```

---

## ⚖️ 免责声明

- 本仓库**仅供学习参考**，代码质量与工程实践均不保证，请勿直接用于生产。
- 代码中的注释为作者学习时的个人理解，可能存在错误或不准确之处，请批判性阅读。
- 任何调用 API 产生的费用与风险由使用者自行承担。
