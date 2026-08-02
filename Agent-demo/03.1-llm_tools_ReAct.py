import openai
import requests
import dotenv
import os
import json
from datetime import datetime

dotenv.load_dotenv()

APIKEY = os.getenv("DEEPSEEK_API_KEY")
MODEL = os.getenv("MODEL") 
BASE_URL = os.getenv("BASE_URL")

client = openai.OpenAI(
    api_key=APIKEY,
    base_url = BASE_URL
)


tools = [
    {
        "type" : "function",
        "function" : {
            "name" : "get_weather",
            "description" : "获取天气信息",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "city" : {
                        "type" : "string",
                        "description" : "城市名称"
                    }
                }
            } 
        }
    },
    {
        "type" : "function",
        "function" :{
            "name" : "get_time",
            "description" : "获取当前时间",            
        }
    }
]


def excute_tool(name, args):
    if name == "get_weather":
        city = args.get("city")
        # 关键：URL 里的中文必须编码，比如 "广州" → "%E5%B9%BF%E5%B7%9E"
        # requests 会自动处理，但用 params 参数传参更规范，编码也更可靠
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {"name": city, "count": 1, "format": "json", "language": "zh"}
        try:
            res1 = requests.get(url, params=params)
        except Exception as e:
            print(f"请求地理编码API失败: {e}")
            return f"获取天气失败: {e}"

        # 打印 API 返回内容，方便排查问题
        data1 = res1.json()
        print(f"[DEBUG] 地理编码API返回: {json.dumps(data1, ensure_ascii=False)}")

        # 检查 API 返回是否正常
        if "results" not in data1 or len(data1["results"]) == 0:
            return f"未找到城市'{city}'的坐标信息"

        lat = data1["results"][0]["latitude"]
        lon = data1["results"][0]["longitude"]
        country = data1["results"][0].get("country", "")

        print(f"[DEBUG] 城市: {city}, 国家: {country}, 坐标: ({lat}, {lon})")

        url2 = "https://api.open-meteo.com/v1/forecast"
        params2 = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        }
        try:
            res2 = requests.get(url2, params=params2)
        except Exception as e:
            print(f"请求天气API失败: {e}")
            return f"获取天气失败: {e}"

        weather_data = res2.json()
        print(f"[DEBUG] 天气API返回: {json.dumps(weather_data, ensure_ascii=False)}")
        return weather_data["current_weather"]

    elif name == "get_time":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def call_llm(messages,tools):
    while True:
        response = client.chat.completions.create(
            model = MODEL,
            messages = messages,
            tools = tools,
            temperature=0.5
        )

        assitant_message = response.choices[0].message
        messages.append(assitant_message)

        if not assitant_message.tool_calls:
            print(f"最终回答:{assitant_message.content}")
            break

        for tool_call in assitant_message.tool_calls:
            # tool_call.function.arguments 是 JSON 字符串，如 '{"city": "广州"}'
            # 需要用 json.loads() 转成 Python 字典，才能用 .get() 取值
            args = json.loads(tool_call.function.arguments)
            result = excute_tool(tool_call.function.name, args)
            messages.append({
                "role" : "tool",
                "tool_call_id" : tool_call.id,
                "content" : json.dumps(result)
            })


while True:
    user_input = input("请输入问题:")
    if user_input.lower() == "quit":
        break
    messages = [
        {
            "role" : "system",
            "content" : "你是一个智能助理,可以调用工具获取信息"
        },
        {
            "role" : "user",
            "content" : user_input
        }
    ]
    call_llm(messages,tools)
    print("--------------------------------------------------\n")