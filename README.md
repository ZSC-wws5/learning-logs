# Python Agent 学习仓库

> 📚 **仅供个人学习使用**，所有代码均为学习过程中的练习与笔记，请勿用于生产环境。

本仓库记录了作者从 **Python 基础语法** 到 **构建 LLM Agent（工具调用 / ReAct 模式）** 的完整学习过程，循序渐进地覆盖了：

- Python 基础（函数、类、推导式）
- 异步编程（`async` / `await`）
- 网络请求（`requests` 同步 / `aiohttp` 异步）
- 文件读写、异常处理
- 调用 DeepSeek API（OpenAI SDK）
- 工具定义（Tool Schema）+ ReAct 循环（手写推理-行动循环）

---

## 📁 目录结构

```
Agent/
├── 基础/                          # 基础语法小练习（函数、类、异步、aiohttp）
│   ├── func.py                    # 函数与推导式（列表/字典/集合推导式）
│   ├── class.py                   # 类与 __init__ 基础
│   ├── async.py                   # 异步协程初体验
│   └── aiohttp-demo.py            # aiohttp 通用请求封装（GET/POST）
├── learning-demo/                 # 系统化入门教程（带详细中文注释）
│   ├── 01_functions_and_classes.py  # 函数与类
│   ├── 02_async_programming.py      # 异步编程
│   ├── 03_network_requests.py       # aiohttp 网络请求
│   ├── 04_file_io.py                # 文件读写
│   ├── 05_exception_handling.py     # 异常处理
│   └── 06_call_deepseek.py          # 完整版：aiohttp 调用 DeepSeek API
├── Agent-demo/                    # LLM Agent 示例（直接可运行）
│   ├── 00-Demo.py                 # aiohttp 异步调用 + rich 美化输出
│   ├── 01-call_LLM.py             # requests 同步调用（情感分析师角色）
│   ├── 02-chat_roles.py           # system 角色设定示例（翻译官）
│   ├── 03-llm_tools_ReAct.py      # 🔧 工具调用入门：ReAct 模式详解
│   └── 03.1-llm_tools_ReAct.py    # 🔧 工具调用进阶：get_weather + get_time
├── learning-plans/                # 📖 AI Agent 学习计划
│   ├── learning-plan-v4-optimized.md  # V4.0 重构优化版（当前使用）
│   └── blocked-urls-mirrors.md        # 🔗 链接对照表
├── requirements.txt               # Python 依赖
├── .env.example                   # 环境变量配置示例
└── .gitignore
```

---

## 🚀 环境准备

**Python 版本：** 3.9+

```bash
# 1. 创建虚拟环境（Windows）
python -m venv venv
venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt
```

主要依赖：

| 库 | 用途 |
|:---|:---|
| `openai` | OpenAI SDK，用于调用 DeepSeek API（兼容接口） |
| `aiohttp` | 异步 HTTP 客户端 |
| `requests` | 同步 HTTP 客户端 |
| `httpx` | 现代 HTTP 客户端（openai SDK 底层使用） |
| `python-dotenv` | 从 `.env` 文件加载环境变量 |
| `rich` | 终端美化输出 |
| `pydantic` | 数据校验（openai SDK 依赖） |

---

## 🔑 配置 API Key

本项目通过 DeepSeek API 调用大模型。调用 LLM 的示例（`learning-demo/06_call_deepseek.py`、`Agent-demo/`）需要配置密钥：

1. 复制 `.env.example` 为 `.env`：

   ```bash
   cp .env.example .env   # Windows 下复制后重命名即可
   ```

2. 编辑 `.env`，填入你的真实配置：

   ```ini
   DEEPSEEK_API_KEY=你的_DeepSeek_API_Key
   BASE_URL=https://api.deepseek.com/
   MODEL=deepseek-chat
   TEMPERATURE=0.7
   MAX_TOKENS=4096
   ```

> ⚠️ **注意**：`.env` 已加入 `.gitignore`，不会被提交到 Git，但请务必不要在任何渠道泄露你的 API Key。
>
> 不填 API Key 也能运行 `06_call_deepseek.py` —— 程序会进入"模拟模式"，打印假回复，方便你先看懂整个调用流程。

---

## ▶️ 运行示例

```bash
# 最简单的入口：完整版 LLM 调用演示（带详细注释）
python learning-demo/06_call_deepseek.py

# Agent 示例（需要 .env 配置了真实 Key）
python Agent-demo/00-Demo.py              # aiohttp 异步 + rich 美化
python Agent-demo/01-call_LLM.py          # requests 同步 + 情感分析师角色
python Agent-demo/02-chat_roles.py        # system 角色设定：翻译官
python Agent-demo/03-llm_tools_ReAct.py   # 🔧 工具调用入门：ReAct 模式详解
python Agent-demo/03.1-llm_tools_ReAct.py # 🔧 工具调用进阶：多工具协作
```

---

## 🗺️ 建议学习路径

```
第 1 步：Python 基础
├── 基础/func.py、class.py              → 函数、类、推导式
├── learning-demo/01_functions_and_classes.py
└── learning-demo/05_exception_handling.py  → 异常处理

第 2 步：异步 + 网络请求
├── 基础/async.py                       → 异步协程初体验
├── learning-demo/02_async_programming.py
├── 基础/aiohttp-demo.py                → aiohttp 请求封装
└── learning-demo/03_network_requests.py

第 3 步：文件 IO
└── learning-demo/04_file_io.py

第 4 步：调用 LLM
├── learning-demo/06_call_deepseek.py   → 完整调用流程
├── Agent-demo/00-Demo.py              → aiohttp + rich 美化
├── Agent-demo/01-call_LLM.py          → 情感分析师（角色扮演）
└── Agent-demo/02-chat_roles.py        → 翻译官（system 角色）

第 5 步：Agent 核心 — 工具调用 & ReAct
├── Agent-demo/03-llm_tools_ReAct.py   → 理解 Tool Schema + ReAct 循环
└── Agent-demo/03.1-llm_tools_ReAct.py → 多工具协作（天气 + 时间）
```

---

## 🗺️ 学习计划

本仓库包含完整的 AI Agent 开发学习计划（位于 `learning-plans/` 目录）：

| 文件 | 说明 |
|:---|:---|
| [learning-plan-v4-optimized.md](learning-plans/learning-plan-v4-optimized.md) | V4.0 重构版：优化节奏、增加调试/流式/复盘日、MCP 后置 |
| [blocked-urls-mirrors.md](learning-plans/blocked-urls-mirrors.md) | 🔗 链接对照表：OpenAI/Anthropic 官方链接 → 国内可访问替代 |

---

## ⚖️ 免责声明

- 本仓库**仅供学习参考**，代码质量与工程实践均不保证，请勿直接用于生产。
- 代码中的注释为作者学习时的个人理解，可能存在错误或不准确之处，请批判性阅读。
- 任何调用 API 产生的费用与风险由使用者自行承担。
