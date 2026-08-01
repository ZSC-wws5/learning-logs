import aiohttp
import asyncio


# res.text()：网页 HTML 文字源码；
# res.json()：接口 JSON 数据，直接转为 Python 字典；
# res.content()：二进制数据，用来下载图片、视频、文件；



async def call_api(
    session: aiohttp.ClientSession,
    method: str,
    url: str,
    data: dict = None,
    params: dict = None,
    headers: dict = None,
    timeout: int = 10,
):
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