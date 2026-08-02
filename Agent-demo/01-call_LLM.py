import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
MODEL = os.getenv("MODEL")
BASE_URL = os.getenv("BASE_URL")


def call_llm(user_message):
    url = BASE_URL+"chat/completions"
    header = {
        "Authorization" : f"Bearer {DEEPSEEK_API_KEY}",
        "Content-type" : "application/json" 
    }

    data = {
        "model" : MODEL,
        "messages" : [
            {"role" : "system", "content":"你是一个情感分析师，你的工作是分析用户的情感"},
            {"role" : "user", "content":user_message}
        ],
        "temperature" : 0.7
    }


    try:
        response = requests.post(url,headers=header,json=data)
    except Exception as e:
        print(f"出错了{e}")
        return None
    else:
        res = response.json()
        return res["choices"][0]["message"]["content"]

res = call_llm("晚上不开心怎么办？")
print(f"回答:\n{res}")
