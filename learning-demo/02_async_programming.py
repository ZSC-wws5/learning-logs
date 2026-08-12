"""
===========================================================================
 02 — 异步编程 —— 入门基础版
===========================================================================
异步编程是 Python 中"同时做多件事"的技术。

重要提示：
  刚开始学 Python 时，你基本用不上异步。
  等你需要同时调用多个 AI 接口时才会真正用到它。

  这个文件只讲核心概念和最简单的写法，
  能看懂 + 知道怎么用就够，不用深究底层。

安装：Python 自带，不需要额外装任何东西。
===========================================================================
"""

import asyncio  # 异步编程的标准库
import time     # 用来对比同步和异步的区别

# ═══════════════════════════════════════════════════════════════════════════
# 第一部分：为什么要有异步？（理解动机比学语法更重要）
# ═══════════════════════════════════════════════════════════════════════════

# ─── 1. 先看同步版本：一件事做完才能做下一件 ───

def task_sync(name, seconds):
    """
    模拟一个耗时任务（比如请求 AI 接口）。
    同步版本：必须等 seconds 秒才能返回。
    """
    print(f"  {name} 开始...需要 {seconds} 秒")
    time.sleep(seconds)  # time.sleep 会"阻塞"——整个程序停在这里等
    print(f"  {name} 完成！")
    return f"{name} 的结果"

def sync_demo():
    """同步版本：3 个任务依次执行，总耗时 = 3 秒。"""
    print("\n--- 同步执行 ---")
    start = time.time()

    r1 = task_sync("任务A", 1.0)
    r2 = task_sync("任务B", 1.0)
    r3 = task_sync("任务C", 1.0)

    elapsed = time.time() - start
    print(f"总耗时：{elapsed:.1f} 秒")  # 约 3 秒


# ─── 2. 再看异步版本：等待的时候去做别的事 ───

async def task_async(name, seconds):
    """
    异步版本：await 时"交出控制权"，去做别的事。
    等 seconds 秒后回来继续。

    重点理解：
    - async def 定义的是"协程函数"
    - await 像在说"我去等，你先做别的"
    - asyncio.sleep 是"不阻塞的等"
    """
    print(f"  {name} 开始...需要 {seconds} 秒")
    await asyncio.sleep(seconds)  # ⬅ await 交出控制权
    print(f"  {name} 完成！")
    return f"{name} 的结果"

async def async_demo():
    """异步版本：3 个任务"同时等待"，总耗时 ≈ 1 秒。"""
    print("\n--- 异步执行 ---")
    start = time.time()

    # gather = "收集"，同时运行多个协程
    # 三个任务同时开始等，所以总耗时 ≈ 最慢的那个
    r1, r2, r3 = await asyncio.gather(
        task_async("任务A", 1.0),
        task_async("任务B", 1.0),
        task_async("任务C", 1.0),
    )

    elapsed = time.time() - start
    print(f"总耗时：{elapsed:.1f} 秒")  # 约 1 秒


# ═══════════════════════════════════════════════════════════════════════════
# 第二部分：必须掌握的语法（就这 3 个）
# ═══════════════════════════════════════════════════════════════════════════

# ─── async def：定义协程 ───
async def fetch_data(item_id):
    """模拟从某个地方获取数据。"""
    print(f"  正在获取数据 #{item_id}...")
    await asyncio.sleep(0.5)  # 模拟网络延迟
    return {"id": item_id, "value": f"数据{item_id}"}

# ─── await：等待协程完成 ───
async def demo_await():
    """await 等待一个协程执行完，拿到返回值。"""
    print("\n--- await 基础用法 ---")
    result = await fetch_data(1)  # 等 fetch_data 执行完
    print(f"  结果：{result}")

    # 也可以一个一个来（但这不是并发）
    r1 = await fetch_data(2)
    r2 = await fetch_data(3)
    print(f"  一个一个来：{r1}, {r2}")

# ─── asyncio.gather：并发执行 ───
async def demo_gather():
    """gather = 让多个协程同时跑，一起等结果。"""
    print("\n--- gather 并发执行 ---")
    results = await asyncio.gather(
        fetch_data(4),
        fetch_data(5),
        fetch_data(6),
    )
    # results 保持传入顺序
    for r in results:
        print(f"  {r}")


# ═══════════════════════════════════════════════════════════════════════════
# 第三部分：超时控制（防止程序卡死）
# ═══════════════════════════════════════════════════════════════════════════

async def demo_timeout():
    """给任务设一个最晚等待时间，超时就放弃。"""
    print("\n--- 超时控制 ---")

    async def slow_task():
        """模拟一个非常慢的任务。"""
        await asyncio.sleep(10)  # 要等 10 秒
        return "终于完成了"

    try:
        # wait_for：最多等 2 秒，超时抛 TimeoutError
        result = await asyncio.wait_for(slow_task(), timeout=2)
        print(f"结果：{result}")
    except asyncio.TimeoutError:
        print("超时了！任务花费超过 2 秒，已取消")


# ═══════════════════════════════════════════════════════════════════════════
# 第四部分：必须记住的 3 点（避坑指南）
# ═══════════════════════════════════════════════════════════════════════════

"""
1. 异步函数必须用 asyncio.run() 来启动
   不能直接调用 async def 函数，必须用 await 或 asyncio.run()

   ❌ fetch_data(1)          ← 这样不行，返回的是协程对象，不是结果
   ✅ await fetch_data(1)    ← 这样才行
   ✅ asyncio.run(fetch_data(1))  ← 入口处用这个

2. 不要在 async 函数里用 time.sleep()
   time.sleep 会卡住整个程序，用 await asyncio.sleep() 替代

   ❌ time.sleep(1)    ← 卡住所有人
   ✅ await asyncio.sleep(1)  ← 只等不卡

3. 只有需要"同时等很多 I/O 操作"时才用异步
   普通脚本、计算密集的任务不需要异步，用了反而更慢
"""

# 标准使用模板：
"""
import asyncio

async def my_task():
    # 做点什么
    await asyncio.sleep(1)
    return "完成"

async def main():
    # 同时做多个任务
    results = await asyncio.gather(
        my_task(),
        my_task(),
    )
    return results

# 入口
if __name__ == "__main__":
    result = asyncio.run(main())
"""


# ═══════════════════════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 50)
    print("02 — 异步编程 入门基础")
    print("=" * 50)

    sync_demo()          # 同步：3 秒
    asyncio.run(async_demo())  # 异步：1 秒

    asyncio.run(demo_await())
    asyncio.run(demo_gather())
    asyncio.run(demo_timeout())

    print("\n===== 异步编程 基础演示结束 =====")
    print("牢记：await 说'我去等，你先做别的'")
    print("      gather 说'你们同时做，我一起等结果'")
