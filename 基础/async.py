# 异步编程
import asyncio


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
    """
        await 后面接的是cpu的操作，比如拼接好一个请求POST
        拼接发送后await等待结果
        如果要接受返回的结果可以这样写
        response = await http_client.post(url, json=payload, headers=headers)
    """
    print(f"  {name} 完成！")
    return f"{name} 的结果"

"""
    一个任务/函数中如果只需要CPU运算立马就能得到返回结果就不需要异步
    如果调用的函数是async def那么前面必须交await进行异步
    普通的def函数不能用await
"""