"""
===========================================================================
 03 — aiohttp 网络请求 —— 入门基础版
===========================================================================
aiohttp 是异步版的 requests，用 async/await 发 HTTP 请求。

和 requests 的区别：
  requests：一条路走到黑，等的时候干等着
  aiohttp：等的时候去干别的事，不浪费 CPU

你会用它来并发调用 AI 接口（同时问 GPT 多个问题）。
但你得先学会基础：单次 GET、单次 POST。

安装（已装好）：
  pip install aiohttp
===========================================================================
"""

import asyncio  # 异步编程需要
import aiohttp  # 异步 HTTP 库

# ═══════════════════════════════════════════════════════════════════════════
# 重点理解：
# aiohttp 和 requests 最大的不同——
# requests：resp = requests.get(url)             ← 同步，卡住等
# aiohttp：resp = await session.get(url)         ← 异步，等的时候让出CPU
#
# 记住一个关键区别：
#   resp.text       →  await resp.text()      返回值变 await
#   resp.json()     →  await resp.json()
#   resp.status_code →  resp.status            属性名不同
#   写在一起就是：data = await (await session.get(url)).json()
# ═══════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════
# 第一部分：GET 请求（从服务器拿数据）
# ═══════════════════════════════════════════════════════════════════════════

# ─── 1. 最基础的 GET ───

async def demo_basic_get():
    """
    最简单的异步 GET 请求。

    和 requests 相比多了两样东西：
    1. async def 而不是 def
    2. async with aiohttp.ClientSession() as session：创建会话
       （session 会复用连接，性能更好）
    3. await session.get(...) 而不是 requests.get(...)
    """
    print("\n--- GET 请求 ---")

    # aiohttp 用 session 来发请求，类似 requests.Session
    # session 用完自动关闭（async with 的作用）
    async with aiohttp.ClientSession() as session:
        # await = 发出去，等回来。期间 CPU 可以干别的
        async with session.get("https://httpbin.org/get") as resp:
            print(f"状态码：{resp.status}")  # 注意是 .status 不是 .status_code

            # 拿到原始文本（await 别忘了）
            text = await resp.text()
            print(f"返回内容（前 100 字）：{text[:100]}")

            # 解析 JSON（也要 await）
            data = await resp.json()
            print(f"解析成字典后的 url 字段：{data['url']}")


# ─── 2. GET 带参数 ───

async def demo_get_with_params():
    """
    GET 请求带查询参数。

    和 requests 一摸一样的 params 参数，aiohttp 也支持。
    """
    print("\n--- GET 带参数 ---")

    params = {"name": "小明", "age": 18}

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://httpbin.org/get",
            params=params,
        ) as resp:
            data = await resp.json()
            print(f"服务器收到的参数：{data['args']}")


# ═══════════════════════════════════════════════════════════════════════════
# 第二部分：POST 请求（向服务器发数据）
# ═══════════════════════════════════════════════════════════════════════════

async def demo_post():
    """
    POST 请求：发送数据到服务器。

    和 requests 一样用 json= 传数据，但要加 await。
    """
    print("\n--- POST 请求 ---")

    payload = {"username": "小明", "message": "你好！"}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://httpbin.org/post",
            json=payload,
        ) as resp:
            data = await resp.json()
            print(f"服务器收到的 JSON 数据：{data['json']}")


# ═══════════════════════════════════════════════════════════════════════════
# 第三部分：统一模板（以后都用这个结构）
# ═══════════════════════════════════════════════════════════════════════════

async def call_api(
    session: aiohttp.ClientSession,
    method: str,
    url: str,
    data: dict = None,
    params: dict = None,
    headers: dict = None,
    timeout: int = 10,
):
    """
    通用的异步 API 调用函数。

    注意多了个 session 参数，因为 aiohttp 推荐复用 session。
    在实际项目中，你会创建一个 session 然后用到底。

    Parameters
    ----------
    session : aiohttp.ClientSession
        复用的 HTTP 会话。
    method : str
        "GET" 或 "POST"。
    url : str
        API 地址。
    data : dict, optional
        POST 时发送的数据。
    params : dict, optional
        GET 时的查询参数。
    headers : dict, optional
        自定义请求头（如 API Key）。
    timeout : int
        超时秒数。

    Returns
    -------
    dict 或 str
        服务器返回的数据。
    """
    try:
        # 发起请求（根据 method 选择）
        if method.upper() == "GET":
            async with session.get(url, params=params, headers=headers,
                                   timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
                resp.raise_for_status()
                try:
                    return await resp.json()
                except Exception:
                    return await resp.text()

        elif method.upper() == "POST":
            async with session.post(url, json=data, headers=headers,
                                    timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
                resp.raise_for_status()
                try:
                    return await resp.json()
                except Exception:
                    return await resp.text()

        else:
            raise ValueError(f"不支持的 method：{method}")

    except asyncio.TimeoutError:
        return {"error": "请求超时"}
    except aiohttp.ClientConnectorError:
        return {"error": "网络连接失败"}
    except aiohttp.ClientResponseError as e:
        return {"error": f"HTTP 错误：{e.status}"}
    except Exception as e:
        return {"error": f"其他错误：{str(e)}"}


async def demo_template():
    """展示统一模板的用法。"""
    print("\n--- 统一模板用法 ---")

    async with aiohttp.ClientSession() as session:
        # GET 请求
        result = await call_api(session, "GET", "https://httpbin.org/get", params={"test": 1})
        print(f"GET 结果：{result.get('url', '无url')}")

        # POST 请求
        result = await call_api(session, "POST", "https://httpbin.org/post", data={"msg": "你好"})
        print(f"POST 结果：{result.get('json', '无数据')}")


# ═══════════════════════════════════════════════════════════════════════════
# 第四部分：超时（必须设！）
# ═══════════════════════════════════════════════════════════════════════════

async def demo_timeout():
    """
    超时的作用：防止程序卡死。

    aiohttp 的超时用 ClientTimeout 设置，
    和 requests 的 timeout= 是一个意思。
    """
    print("\n--- 超时演示 ---")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                "https://httpbin.org/delay/5",
                timeout=aiohttp.ClientTimeout(total=2),
            ) as resp:
                print(f"成功：{resp.status}")
        except asyncio.TimeoutError:
            print("超时了！（2 秒没返回，程序没卡死）")


# ═══════════════════════════════════════════════════════════════════════════
# 第五部分：并发请求（aiohttp 的杀手锏）
# ═══════════════════════════════════════════════════════════════════════════

async def demo_concurrent():
    """
    aiohttp + asyncio.gather = 同时发多个请求。
    这是 requests 做不到的。

    这里同时请求 3 个接口，总耗时 ≈ 最慢的那个。
    """
    print("\n--- 并发请求（这是 aiohttp 相比 requests 的核心优势） ---")

    async def fetch_one(session, url, name):
        """单个请求。"""
        async with session.get(url) as resp:
            data = await resp.json()
            print(f"  {name} 完成：{data.get('url', 'ok')[:40]}")
            """
            # data 是一个字典，包含 url 字段,.get()方法可以通过键获取值，如果键不存在，返回 None 或默认值。
            # 这里用 get() 方法获取 url 字段，如果 url 字段不存在，返回默认值 'ok'，避免了程序崩溃
            # 例如：data.get('url', 'ok')
            """
            return data

    urls = [
        ("任务A", "https://httpbin.org/get"),
        ("任务B", "https://httpbin.org/get"),
        ("任务C", "https://httpbin.org/get"),
    ]

    async with aiohttp.ClientSession() as session:
        # 三个请求同时发出
        tasks = [fetch_one(session, url, name) for name, url in urls]
        results = await asyncio.gather(*tasks)
        print(f"  全部完成，共 {len(results)} 个结果")


# ═══════════════════════════════════════════════════════════════════════════
# 第六部分：入门总结
# ═══════════════════════════════════════════════════════════════════════════

"""
requests vs aiohttp 对照表（记这个就够了）：

                requests                     aiohttp
                ────────                     ───────
  导入          import requests              import aiohttp
  函数定义      def                          async def
  发 GET        requests.get(url)            await session.get(url)
  发 POST       requests.post(url, json=d)   await session.post(url, json=d)
  状态码        resp.status_code             resp.status
  读 JSON       resp.json()                  await resp.json()
  读文本        resp.text                    await resp.text()
  异常          requests.exceptions.*        aiohttp.* + asyncio.TimeoutError

  aiohttp 固定写法（记住这个模板）：
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

  刚开始会觉得多了 async/await 很麻烦，
  但当你需要同时发很多请求时，优势就出来了。
"""


# ═══════════════════════════════════════════════════════════════════════════
# 主入口：asyncio.run() 启动所有异步演示
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 50)
    print("03 — aiohttp 网络请求 入门基础")
    print("=" * 50)

    # asyncio.run() 是异步程序的入口
    asyncio.run(demo_basic_get())
    asyncio.run(demo_get_with_params())
    asyncio.run(demo_post())
    asyncio.run(demo_template())
    asyncio.run(demo_timeout())
    asyncio.run(demo_concurrent())

    print("\n===== 网络请求 基础演示结束 =====")
    print("核心三句话：")
    print("  1. async with session.get(url) as resp  ← 发请求")
    print("  2. data = await resp.json()              ← 拿结果")
    print("  3. await asyncio.gather(*tasks)          ← 并发")
