"""
===========================================================================
 一个完整的 AI 调用示例 —— 用 aiohttp 调 DeepSeek API
===========================================================================
用法：
  1. 复制 .env.example 为 .env
  2. 在 .env 里填上你的 DEEPSEEK_API_KEY
  3. 运行本文件：python 06_call_deepseek.py

不填 key 也能跑——程序会打印"假装"的回复，让你看流程。
===========================================================================
"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

# ── 加载 .env 文件中的环境变量 ──
# 先去 .env 里读 DEEPSEEK_API_KEY，如果没有就用 None
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")


async def call_deepseek(
    user_message: str,
    system_prompt: str = "You are a helpful assistant.",
    model: str = "deepseek-chat",
    temperature: float = 0.7,
) -> str:
    """
    用 aiohttp 调用 DeepSeek API 的核心函数。

    参数说明
    --------
    user_message : str
        用户说的话，比如"用 Python 实现一个冒泡排序"。
    system_prompt : str
        给 AI 设定的角色，比如"你是一个 Python 导师"。
    model : str
        模型名字，"deepseek-chat" 是通用对话模型。
    temperature : float (0~2)
        创造力程度。0 = 保守稳定，1 = 有创意，2 = 放飞。
        写代码用 0.3，写文案用 0.8。

    返回
    -------
    str : AI 的回复文本。
    """
    # ── 1. 拼接请求 ──
    # 这是发出 POST 请求需要的一切
    url = "https://api.deepseek.com/chat/completions"

    headers = {
        # Bearer 后面有个空格，千万别漏
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            # system 消息：告诉 AI 它的角色（可选但推荐）
            {"role": "system", "content": system_prompt},
            # user 消息：用户的输入
            {"role": "user", "content": user_message},
            # 如果要支持多轮对话，就在这里继续加 assistant/user 消息
        ],
        "temperature": temperature,
        # max_tokens 限制回复的最大长度
        "max_tokens": 2048,
        # stream=False 表示等全部生成完再返回
        "stream": False,
    }

    # ── 2. 没有 API Key 时的模拟模式 ──
    if not API_KEY:
        print("  [模拟] 没有 API Key，假装调用了 DeepSeek...")
        await asyncio.sleep(0.5)
        return f"[模拟回复] 你问的是：'{user_message[:30]}...'"

    # ── 3. 发送请求 + 处理响应 ──
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload,
                                    timeout=aiohttp.ClientTimeout(total=30)) as resp:
                # 检查状态码（4xx 或 5xx 会抛异常）
                resp.raise_for_status()

                # 解析返回的 JSON
                data = await resp.json()

                # 从嵌套结构中提取 AI 的回复文本
                # data 的结构：
                # {
                #   "choices": [
                #     {
                #       "message": {
                #         "content": "这是 AI 的回复..."
                #       }
                #     }
                #   ]
                # }
                reply = data["choices"][0]["message"]["content"]

                # 可选：打印 token 用量（方便查账）
                usage = data.get("usage", {})
                print(f"  [用量] 输入 {usage.get('prompt_tokens', '?')} tokens，"
                      f"输出 {usage.get('completion_tokens', '?')} tokens")

                return reply

    except asyncio.TimeoutError:
        return "[错误] 请求超时（超过 30 秒没有响应）"
    except aiohttp.ClientResponseError as e:
        if e.status == 401:
            return "[错误] API Key 无效，请检查 .env 文件中的 DEEPSEEK_API_KEY"
        elif e.status == 429:
            return "[错误] 请求太频繁了（限流），等一会儿再试"
        elif e.status == 400:
            return f"[错误] 请求参数有误：{e.message}"
        else:
            return f"[错误] 服务器返回 {e.status}：{e.message}"
    except aiohttp.ClientConnectorError:
        return "[错误] 网络连接失败，检查网络或 API 地址"
    except Exception as e:
        return f"[错误] {type(e).__name__}：{str(e)}"


async def demo():
    """演示：用同一个函数调三次，展示不同用法。"""
    print("=" * 55)
    print("用 aiohttp 调用 DeepSeek API")
    print("=" * 55)

    # ── 调用 1：简单问答 ──
    print("\n━━━ 对话 1：简单问答 ━━━")
    reply = await call_deepseek(
        "请用 Python 写一个冒泡排序",
        system_prompt="你是一位 Python 编程导师，回复简洁清晰。",
    )
    print(f"AI：{reply}")

    # ── 调用 2：翻译 ──
    print("\n━━━ 对话 2：翻译 ━━━")
    reply = await call_deepseek(
        "将这句话翻译成英文：学编程最好的方法是动手写代码。",
        system_prompt="你是一个翻译助手。",
        temperature=0.3,  # 翻译用低温度，更准确
    )
    print(f"AI：{reply}")

    # ── 调用 3：总结 ──
    print("\n━━━ 对话 3：文本总结 ━━━")
    long_text = """
    Python 是一种广泛使用的编程语言，由 Guido van Rossum 在 1991 年创建。
    它设计哲学强调代码的可读性，使用缩进来组织代码块。
    Python 支持多种编程范式，包括面向对象、命令式、函数式等。
    它拥有庞大的标准库和第三方生态，在 Web 开发、数据分析、人工智能、
    自动化脚本等领域都有广泛应用。近年来，随着 AI 技术的爆发，
    Python 成为了机器学习和深度学习领域的事实标准语言。
    """
    reply = await call_deepseek(
        f"用 50 字以内总结以下内容：{long_text}",
        system_prompt="你是一个总结助手，回复要简短。",
    )
    print(f"AI：{reply}")

    print("\n===== 演示完成 =====")
    if not API_KEY:
        print("提示：以上是模拟回复。填上 API Key 就能收到真实的 AI 回复。")
        print("配置方法：复制 .env.example 为 .env，填入你的 DEEPSEEK_API_KEY")


if __name__ == "__main__":
    asyncio.run(demo())
