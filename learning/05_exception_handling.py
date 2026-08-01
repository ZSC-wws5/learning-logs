"""
===========================================================================
 05 — 异常处理 —— 入门基础版
===========================================================================
异常 = 程序运行中出现的错误。

学会处理异常，你的程序就不会因为一个小错误而整个崩溃。
这是专业代码和业余代码的分水岭。

你只需要记住：try - except 就够用了。
===========================================================================
"""

# ═══════════════════════════════════════════════════════════════════════════
# 第一部分：如果不管异常会怎样？
# ═══════════════════════════════════════════════════════════════════════════

def demo_no_handling():
    """
    不处理异常：程序直接崩溃。

    运行下面的代码，程序会中断，后面的代码都不执行了。
    我们把这个函数用 try 包起来，不然整个演示文件会停在这里。
    """
    print("\n--- 不处理异常的后果 ---")

    try:
        # 这句会出错：0 不能做除数
        result = 10 / 0
        print(result)  # 这行不会执行到
    except ZeroDivisionError:
        print("（上面演示了程序为什么需要异常处理）")


# ═══════════════════════════════════════════════════════════════════════════
# 第二部分：基本语法 —— try / except
# ═══════════════════════════════════════════════════════════════════════════

# ─── 1. 最基础的用法 ───

def demo_basic():
    """
    try / except 的基本结构。

    try:
        可能出错的代码
    except:
        出错后执行的代码
    """
    print("\n--- try/except 基础 ---")

    try:
        number = int(input("请输入一个数字："))  # 用户可能输入"abc"
        result = 10 / number                     # 用户可能输入 0
        print(f"10 / {number} = {result}")
    except:
        # 任何错误都会走到这里
        print("出错了！请确保输入的是非零数字")


# ─── 2. 捕获特定类型的异常 ───

def demo_specific():
    """
    捕获不同类型的异常，分别处理。

    不同的错误有不同的原因，应该有不同的处理方法。
    """
    print("\n--- 捕获特定异常 ---")

    try:
        num = int(input("请输入一个数字："))
        result = 10 / num
        print(f"结果：{result}")

    except ValueError:
        # ValueError：值错误，比如 int("abc")
        print("输入的不是有效数字！")

    except ZeroDivisionError:
        # ZeroDivisionError：除以零
        print("不能除以零！")

    # 拿到的异常信息
    except Exception as e:
        # Exception 是所有异常的父类，兜底用
        # 把 as e 可以把异常信息存到变量 e 里
        print(f"发生了未知错误：{type(e).__name__} - {e}")


# ─── 3. else 和 finally ───

def demo_else_finally():
    """
    else：没出错时执行。
    finally：无论有没有错都执行（收尾工作）。
    """
    print("\n--- else 和 finally ---")

    try:
        num = int("42")  # 正常转换
    except ValueError as e:
        print(f"出错：{e}")
    else:
        # try 没出错才执行这里
        print(f"转换成功，数字是 {num}")
    finally:
        # 不管有没有错，都执行这里
        # 常用于关闭文件、关闭连接等清理工作
        print("finally：这里的代码一定会执行")


# ═══════════════════════════════════════════════════════════════════════════
# 第三部分：最常见的异常类型
# ═══════════════════════════════════════════════════════════════════════════

def demo_common_exceptions():
    """
    演示你平时会遇到的最常见的几种异常。
    """
    print("\n--- 常见异常类型 ---")

    examples = [
        ("除零错误", "ZeroDivisionError", lambda: 1 / 0),
        ("值错误", "ValueError", lambda: int("abc")),
        ("索引越界", "IndexError", lambda: [1, 2, 3][100]),
        ("键不存在", "KeyError", lambda: {"name": "小明"}["age"]),
        ("类型错误", "TypeError", lambda: len(123)),
        ("文件不存在", "FileNotFoundError", lambda: open("不存在的文件.txt")),
    ]

    for desc, name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"  {desc} -> {name}: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# 第四部分：实际场景 —— 调用 API 时的异常处理
# ═══════════════════════════════════════════════════════════════════════════

import requests

def demo_real_scenario():
    """
    真实场景：调用一个可能出错的 API。

    网络请求最常遇到 3 种问题：
    1. 连不上（网络断了）
    2. 超时（服务器太慢）
    3. 拒绝访问（地址错了 / 没权限）
    """
    print("\n--- 实际场景：API 调用 ---")

    urls = [
        "https://httpbin.org/get",           # 正常
        "https://httpbin.org/status/404",    # 不存在
        "https://不存在-的网站-123.com",      # 连不上
    ]

    for url in urls:
        try:
            response = requests.get(url, timeout=3)

            # raise_for_status()：如果状态码 >= 400，抛出异常
            response.raise_for_status()

            data = response.json()
            print(f"  ✅ {url} -> 成功")

        except requests.exceptions.ConnectionError:
            print(f"  ❌ {url} -> 网络连接失败")
        except requests.exceptions.Timeout:
            print(f"  ⏰ {url} -> 请求超时")
        except requests.exceptions.HTTPError as e:
            print(f"  ⚠️  {url} -> HTTP 错误 {e.response.status_code}")
        except Exception as e:
            # 兜底
            print(f"  ❓ {url} -> 未知错误：{type(e).__name__}")


# ═══════════════════════════════════════════════════════════════════════════
# 第五部分：必须记住的代码模板
# ═══════════════════════════════════════════════════════════════════════════

"""
标准模板 1：最常用（记住这个就够了）

    try:
        # 可能出错的代码
        result = 可能会出错的操作()
    except ValueError as e:
        print(f"值错误：{e}")
    except Exception as e:
        print(f"其他错误：{e}")


标准模板 2：完整版（专业代码）

    try:
        result = 可能会出错的操作()
    except ValueError as e:
        print(f"输入不合法：{e}")
        result = None           # 给个默认值
    except TimeoutError:
        print("超时了")
        result = None
    except Exception as e:
        print(f"未预期的错误：{type(e).__name__} - {e}")
        result = None
    else:
        print("没有出错！")      # 只有成功才执行
    finally:
        print("收尾工作")        # 不管成不成功都执行


重要原则：
1. 先捕获具体的异常，最后用 Exception 兜底
2. 不要用空的 except:（会连 Ctrl+C 都抓）
3. 能用 else/finally 就用，能更精确地控制流程
"""


# ═══════════════════════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 50)
    print("05 — 异常处理 入门基础")
    print("=" * 50)

    demo_no_handling()
    demo_basic()
    demo_specific()
    demo_else_finally()
    demo_common_exceptions()
    demo_real_scenario()

    print("\n===== 异常处理 基础演示结束 =====")
    print("记住一句话：try 可能出错的代码，except 处理出错的情况")
