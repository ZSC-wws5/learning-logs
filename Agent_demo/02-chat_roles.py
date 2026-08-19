import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
APIKEY = os.getenv("DEEPSEEK_API_KEY")
MODEL = os.getenv("MODEL")
BASE_URL = os.getenv("BASE_URL")

def call_llm_roles(user_message):
    url = BASE_URL + "chat/completions"
    header = {
        "Authorization" : f"Bearer {APIKEY}",
        "Content-type" : "application/json"
    }
    data = {
        "model" : MODEL,
        "messages" : [
            {"role" : "system", "content" : "你是一个翻译官,除了翻译的问题,其他的,你只回答'无法回答'"},
            {"role" : "user", "content" : user_message}
        ],
        "temperature" : 0.7
    }

    try:
        response = requests.post(url=url,headers=header, json = data)
    except Exception as e:
        print(f"出错:{e}")
        return None
    else:
        return response.json()


res1 = call_llm_roles("你好")
res2 = call_llm_roles("你好世界,翻译成英语")

print(f"回答一:\n{res1['choices'][0]['message']['content']}")
print("---------------------------------------------------------")
print(f"回答二:\n{res2['choices'][0]['message']['content']}")