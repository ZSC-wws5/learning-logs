import openai
import requests
import dotenv
import os
import json
from datetime import datetime

# 加载环境变量
dotenv.load_dotenv()

# 从环境变量中获取APIKEY、model、base_url
APIKEY = os.getenv("DEEPSEEK_API_KEY")
MODEL = os.getenv("MODEL") 
BASE_URL = os.getenv("BASE_URL")


# 初始化openai客户端
client = openai.OpenAI(
    api_key=APIKEY,
    base_url = BASE_URL
)

# 工具定义
tools = [
    {
        # 工具类型
        "type" : "function",
        # 工具定义
        "function" : {
            # 工具名字-工具描述-参数定义(JSON Schema)
            "name" : "get_weather",
            "description" : "获取天气信息",
            "parameters" : {
                # 参数类型-具体参数-"required":["必填参数1","必填参数2"]
                "type" : "object",
                "properties" : {
                    # 具体参数:参数格式-参数描述-"enum":["可选值1","可选值2"]
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
    },
]

# 工具函数 - 接收LLM返回的tool-calls中的工具名,以及工具参数

def excute_tool(name, args):
    # 接收args中的中文城市名字,然后用params参数传参给request
    if name == "get_weather":
        # 从args中取出城市名字,args在外部已经转换为字典
        city = args.get("city") 
        '''
        # 关键：URL 里的中文必须编码，比如 "广州" → "%E5%B9%BF%E5%B7%9E"
        # requests 会自动处理，但用 params 参数传参更规范，编码也更可靠
        代码下的代码使用了 Open-Meteo 的地理编码 API 来获取城市的经纬度，然后再调用天气 API 获取当前天气信息。
        可以调用然后打印完成的返回json数据,再根据需要取出其中需要的数据
        '''
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

# 调用LLM函数，接收用户的问题，以及工会定义

def call_llm(messages,tools):
    # 以循环形式完成回答-ReAct模式
    while True:
        # openai.client.chat.completions.create() 方法,创建对话，传入模型、消息、工具定义、温度等参数
        response = client.chat.completions.create(
            model = MODEL,
            messages = messages,
            tools = tools,
            temperature=0.5
        )
        # response接收LLM返回的结果，包含choices、usage等信息
        # 取出LLM返回结果中的消息内容,并添加进函数的messages列表中,用于下一轮传给LLM
        assitant_message = response.choices[0].message
        messages.append(assitant_message)

        # 简单判断LLM返回结果中是否有tool_calls,如果没有就直接打印出choices[0].messages.content,并退出循环
        if not assitant_message.tool_calls:
            print(f"最终回答:{assitant_message.content}")
            break

        # 有tool_calls,就用循环遍历提取出的assitant_message(助手消息)中的tool_calls,
        # 并调用excute_tool()函数,从tool_call.function.arguments中取出参数,传给函数,
        # 用得到的结果自行构建成一个新的tool消息,并添加到messages列表中,用于下一轮传给LLM
        for tool_call in assitant_message.tool_calls:
            """
            tool_call.function.arguments 是 JSON 字符串，如 '{"city": "广州"}'
            需要用 json.loads() 转成 Python 字典，才能用 excute_tool()中的.get() 取值
            """
            args = json.loads(tool_call.function.arguments)
            result = excute_tool(tool_call.function.name, args)
            messages.append({
                "role" : "tool",
                "tool_call_id" : tool_call.id,
                "content" : json.dumps(result)
            })

# 程序主循环-用户输入问题后,把问题传给messages先构造好一个静态数据
# messages和tools是同级的消息
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