import asyncio
import aiohttp
import os
import json
from rich.markdown import Markdown
from rich.console import Console
from dotenv import load_dotenv

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
MODEL = os.getenv("MODEL")
BASE_URL = os.getenv("BASE_URL")

async def call_ds(
    session: aiohttp.ClientSession, 
    user_message: str,
    system_prompt:str,
    temperature:float=0.7):
    """
    调用 DeepSeek API。
    """
    url = BASE_URL+"chat/completions"
    headers = { 
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model" : MODEL,
        "messages": [
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_message}
        ],
        "temperature": temperature
    }
    async with session.post(url,json=payload,headers=headers,timeout=aiohttp.ClientTimeout(total=30)) as res:
        res.raise_for_status()
        try:
            return await res.json()
        except aiohttp.ClientError as e:
            print(f"请求失败: {e}")
            return None
############测试###############
async def main():
    async with aiohttp.ClientSession() as session:
        # 在call_ds外创建session(对话),避免每次调用都创建新的对话浪费资源
        demo = await call_ds(
            session,
            user_message = "给我讲讲怎么用aiohttp调用llm的api",
            system_prompt = "你是一个专业的python看法人员,用中文回答"
        )
    print(json.dumps(demo, indent=2, ensure_ascii=False))
    answer = demo["choices"][0]["message"]["content"]
    console = Console()
    console.print("\nAI 回答：")
    console.print(Markdown(answer))

asyncio.run(main())
