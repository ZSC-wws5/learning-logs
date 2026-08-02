# Python Agent 学习仓库

> 📚 **仅供个人学习使用**，所有代码均为学习过程中的练习与笔记，请勿用于生产环境。

本仓库记录了作者从 **Python 基础语法** 到 **调用大模型（LLM）API** 的完整学习过程，循序渐进地覆盖了：

- Python 基础（函数、类、推导式）
- 异步编程（`async` / `await`）
- 网络请求（`requests` 同步 / `aiohttp` 异步）
- 文件读写、异常处理
- 调用 DeepSeek API 构建简单的 LLM Agent 示例

---

## 📁 目录结构

```
Agent/
├── 基础/                    # 基础语法小练习（函数、类、异步、aiohttp）
│   ├── func.py              # 函数与推导式（列表/字典/集合推导式）
│   ├── class.py             # 类与 __init__ 基础
│   ├── async.py             # 异步协程初体验
│   └── aiohttp-demo.py      # aiohttp 通用请求封装（GET/POST）
├── learning/                # 系统化入门教程（带详细中文注释）
│   ├── 01_functions_and_classes.py  # 函数与类
│   ├── 02_async_programming.py      # 异步编程
│   ├── 03_network_requests.py       # aiohttp 网络请求
│   ├── 04_file_io.py                # 文件读写
│   ├── 05_exception_handling.py     # 异常处理
│   └── 06_call_deepseek.py          # 完整版：aiohttp 调用 DeepSeek API
├── Agent-demo/              # LLM Agent 示例（直接可运行）
│   ├── 00-Demo.py           # aiohttp 异步调用 + rich 美化输出
│   ├── 01-call_LLM.py       # requests 同步调用（情感分析师角色）
│   └── 02-chat_roles.py     # system 角色设定示例（翻译官）
├── requirements.txt         # Python 依赖
├── .env.example             # 环境变量配置示例
├── .gitignore
└── learning-plans/          # 📖 AI Agent 学习计划
    ├── learning-plan-annotated.md   # V3.0 官方文档标注版
    ├── learning-plan-v4-optimized.md # V4.0 重构优化版
    └── blocked-urls-mirrors.md      # 🔗 被墙链接 → 替代链接对照表
```

## 🚀 环境准备

**Python 版本：** 3.9（本项目在 Python 3.9.2 下开发验证）

```bash
# 1. 创建虚拟环境（Windows）
python -m venv venv
venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt
```

如果运行 `00-Demo.py` 需要额外安装 rich：

```bash
pip install rich
```

## 🔑 配置 API Key

本项目通过 DeepSeek API 调用大模型。调用 LLM 的示例（`learning/06_call_deepseek.py`、`Agent-demo/`）需要配置密钥：

1. 复制 `.env.example` 为 `.env`：

   ```bash
   cp .env.example .env   # Windows 下复制后重命名即可
   ```

2. 编辑 `.env`，填入你的真实配置：

   ```ini
   DEEPSEEK_API_KEY=你的_DeepSeek_API_Key
   BASE_URL=https://api.deepseek.com/v1/
   MODEL=deepseek-chat
   ```

> ⚠️ **注意**：`.env` 已加入 `.gitignore`，不会被提交到 Git，但请务必不要在任何渠道泄露你的 API Key。
>
> 不填 API Key 也能运行 `06_call_deepseek.py` —— 程序会进入"模拟模式"，打印假回复，方便你先看懂整个调用流程。

## ▶️ 运行示例

```bash
# 最简单的入口：完整版 LLM 调用演示（带详细注释）
python learning/06_call_deepseek.py

# Agent 示例（需要 .env 配置了真实 Key）
python Agent-demo/00-Demo.py        # aiohttp 异步 + rich 美化
python Agent-demo/01-call_LLM.py    # requests 同步 + 情感分析师角色
python Agent-demo/02-chat_roles.py  # system 角色设定：翻译官
```

## 🗺️ 建议学习路径

1. **`基础/` → `learning/01`**：先掌握函数、类、推导式
2. **`learning/05`**：学会异常处理，让程序更健壮
3. **`learning/04`**：文件读写，让程序能持久化数据
4. **`learning/02`、`learning/03`**：异步编程 + aiohttp 网络请求（调用 AI 接口的关键）
5. **`learning/06` → `Agent-demo/`**：实战 —— 调用 LLM，并用 system 角色让 AI 扮演不同角色

## 🗺️ 学习计划

本仓库包含完整的 AI Agent 开发学习计划（位于 `learning-plans/` 目录）：

| 文件 | 说明 |
| :--- | :--- |
| [learning-plan-annotated.md](learning-plans/learning-plan-annotated.md) | V3.0 原版计划 + 每步标注必读官方文档链接 |
| [learning-plan-v4-optimized.md](learning-plans/learning-plan-v4-optimized.md) | V4.0 重构版：优化节奏、增加调试/流式/复盘日、MCP 后置 |
| [blocked-urls-mirrors.md](learning-plans/blocked-urls-mirrors.md) | 🔗 被墙链接对照表：OpenAI/Anthropic 官方链接 → 国内可访问替代 |

> **V4.0 主要改进**：每天分三段（读文档→写代码→记笔记）、每周设复盘日、MCP 移至第 3 周（理解工具后再学）、新增流式输出和 Token 管理。
>
> 🇨🇳 **注意**：所有 OpenAI/Anthropic 官方文档链接已替换为国内可访问的替代来源。如需查阅原始文档，请参考 `blocked-urls-mirrors.md` 对照表挂代理访问。

## ⚖️ 免责声明

- 本仓库**仅供学习参考**，代码质量与工程实践均不保证，请勿直接用于生产。
- 代码中的注释为作者学习时的个人理解，可能存在错误或不准确之处，请批判性阅读。
- 任何调用 API 产生的费用与风险由使用者自行承担。
