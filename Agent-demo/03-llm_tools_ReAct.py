# =============================================================================
# 03-llm_tools_ReAct.py — LLM 工具调用（ReAct 模式）入门示例
# =============================================================================
# 这个文件演示了一个核心概念：让大语言模型（LLM）在需要时"调用工具"来获取信息。
#
# 举个生活类比：
#   你问助手"现在几点了？北京天气怎么样？"
#   助手不会凭空猜——它拿起手机查时间、打开天气App查天气，
#   拿到真实数据后再回答你。这就是"工具调用"。
#
# ReAct = Reasoning（推理）+ Acting（行动），模型先想清楚需要什么信息，
# 然后调用工具去获取，拿到结果后再综合回答。
# =============================================================================

# ---------------------------------------------------------------------------
# 第一部分：导入依赖库
# ---------------------------------------------------------------------------

# json：处理 JSON 格式的数据（这里虽导入了但实际用字符串模拟，后面你会用到 json.loads 等）
import json
# requests：发送 HTTP 请求（这里预留，实际调用外部 API 时会用到）
import requests
# openai：OpenAI 官方的 Python SDK，用来和大模型"对话"
#         DeepSeek 的 API 接口和 OpenAI 兼容，所以可以直接用这个库
import openai
# dotenv：从 .env 文件中读取敏感信息（如 API 密钥），避免把密码写死在代码里
import dotenv
# os：操作系统相关功能，这里用来读取环境变量
import os

# ---------------------------------------------------------------------------
# 第二部分：加载配置（API 密钥、模型名、接口地址）
# ---------------------------------------------------------------------------

# 从项目根目录的 .env 文件中加载配置
# .env 文件内容大概长这样（不含尖括号）：
#   DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
#   MODEL=deepseek-chat
#   BASE_URL=https://api.deepseek.com
dotenv.load_dotenv()

# os.getenv("变量名") 从环境变量中取值
# 为什么这样做？因为 API 密钥是敏感信息，不能直接写在代码里传到 git 上
APIKEY = os.getenv("DEEPSEEK_API_KEY")   # 你的 API 密钥
MODEL = os.getenv("MODEL")                # 使用的模型名称，如 deepseek-chat
BASE_URL = os.getenv("BASE_URL")          # API 接口地址，DeepSeek 的是 https://api.deepseek.com

# ---------------------------------------------------------------------------
# 第三部分：创建客户端
# ---------------------------------------------------------------------------

# 创建一个 OpenAI 客户端实例。
# 虽然类名叫 openai.OpenAI，但由于我们指定了 base_url，它会请求 DeepSeek 的服务器。
# 这是 OpenAI 兼容接口的好处：换一个 base_url 就能对接不同的模型服务商。
#
# 参数说明：
#   api_key  ：身份认证密钥，服务商通过它识别你是谁、扣谁的钱
#   base_url ：API 服务器的地址，所有请求都发往这里
client = openai.OpenAI(
    api_key=APIKEY,
    base_url=BASE_URL,
)

# ---------------------------------------------------------------------------
# 第四部分：定义"工具"（Tools）
# ---------------------------------------------------------------------------
# 这是最关键的部分！工具定义告诉模型："你可以用这些函数来获取信息"。
#
# 为什么要写成 JSON 这样的结构？
#   因为 LLM 是一个纯文本接口——它没有真正的"函数调用"能力。
#   我们需要用 JSON 这种结构化格式来描述：
#     - 有哪些工具可用
#     - 每个工具叫什么名字
#     - 每个工具需要什么参数
#     - 每个工具是干什么的
#
#   模型读完这段描述后，就会在需要时返回类似这样的"调用请求"：
#     "请帮我调用 get_weather，参数 city='北京'"
#
# JSON 字段含义逐层拆解：
#
# tools 是一个 Python 列表（list），每个元素是一个工具对象（dict）：
#   [
#     {工具1的定义},
#     {工具2的定义},
#     ...
#   ]
#
# 每个工具对象的固定结构（OpenAI 规定的格式）：
#   {
#     "type": "function",          ← 固定值，表示这是一个函数类型的工具
#     "function": { ... }          ← 函数的具体描述
#   }
#
# function 内部的字段：
#   {
#     "name": "函数名",            ← 模型用这个名字来指定调用哪个工具
#     "description": "功能描述",   ← 告诉模型这个工具是干什么的，描述越准确调用越精准
#     "parameters": {              ← 工具的参数定义（JSON Schema 格式）
#       "type": "object",          ← 参数整体是一个对象
#       "properties": { ... }      ← 具体有哪些参数，以及各自的类型和说明
#     }
#   }
# ---------------------------------------------------------------------------

tools = [
    # ===== 工具1：获取当前时间 =====
    {
        # 声明这是一个"函数"类型的工具（OpenAI 还支持其他类型，但绝大多数情况下用 function）
        "type": "function",
        "function": {
            # name：工具的唯一标识。模型返回 tool_calls 时会带上这个名字，
            #       你的代码根据 name 决定去执行哪个真实的 Python 函数。
            "name": "get_current_time",
            # description：功能描述，模型会根据这个描述判断"用户的问题是否需要这个工具"。
            #   写中文或英文都可以，关键是准确。
            "description": "获取当前时间",
            # parameters：参数定义，使用 JSON Schema 格式。
            #   JSON Schema 就是一种"描述 JSON 数据长什么样"的标准格式。
            "parameters": {
                "type": "object",           # 参数整体是一个 JSON 对象（花括号包裹的键值对）
                "properties": {              # properties = 属性列表，列出这个对象里有哪些字段
                    "timezone": {             # 参数名：timezone（时区）
                        "type": "string",    # 参数类型：字符串
                        "description": "时区,例如:Asia/Shanghai"  # 参数说明，模型据此知道传什么值
                    }
                }
            }
        }
    },

    # ===== 工具2：获取天气 =====
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {                # 参数1：city（城市名称）
                        "type": "string",
                        "description": "城市名称,例如:北京"
                    },
                    "unit": {                # 参数2：unit（温度单位）
                        "type": "string",
                        # enum 表示"只能从这两个值里选一个"，模型会严格从列表中挑一个传给你
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位,可选值为celsius或fahrenheit"
                    }
                }
            }
        }
    }
]

# ---------------------------------------------------------------------------
# 第五部分：工具的实际执行函数
# ---------------------------------------------------------------------------
# 上面定义的 JSON 只是"工具说明书"，这里才是工具真正的实现逻辑。
#
# 当模型说"我想调用 get_weather，参数是 city='北京'"时，
# 你的代码收到这个请求，就调用这个函数去真正执行。
#
# 参数：
#   name      ：模型要调用的工具名称（对应上面 function.name）
#   arguments ：模型传的参数（是一个 JSON 字符串，注意是字符串不是 dict！）
#               比如：'{"city": "北京", "unit": "celsius"}'
#
# 返回值必须是字符串（通常是 JSON 字符串），因为这个结果要拼接回对话里给模型看。
# ---------------------------------------------------------------------------

def excute_tool(name, arguments):
    """
    根据工具名称分发执行。
    目前是模拟数据（Mock），实际项目中应该替换成真实的 API 调用。
    比如 get_weather 可以用 requests.get("https://api.weather.com/...") 来获取真实天气。
    """
    if name == "get_current_time":
        # 返回模拟的时间数据（JSON 字符串格式）
        # 真实场景：import datetime; return json.dumps({"datetime": datetime.datetime.now().isoformat()})
        return '{"datetime": "2024-06-01 12:00:00", "day_of_week": "Saturday"}'
    elif name == "get_weather":
        # 返回模拟的天气数据（JSON 字符串格式）
        # 真实场景：api_result = requests.get(f"https://api.weather.com/?city=...")
        #          return json.dumps(api_result)
        return '{"weather": "晴朗", "temperature": 25, "unit": "celsius", "humidity": 60, "wind_speed": 5}'

# ---------------------------------------------------------------------------
# 第六部分：构建对话消息
# ---------------------------------------------------------------------------
# messages 是一个列表，存放多轮对话的完整历史。
# 每条消息是一个字典，固定有 "role"（角色）和 "content"（内容）两个字段。
#
# 为什么要把历史消息都带上？
#   因为 LLM 是"无状态"的——它不会记住上一轮聊了什么。
#   你需要把之前的对话全部重新发过去，它才知道上下文。
#
# role 的常见取值：
#   "system"  ：系统指令，设定助手的"人设"和行为规则
#   "user"    ：用户说的话
#   "assistant"：模型的回复（包括它说"我要调工具"的请求）
#   "tool"    ：工具执行后的返回值（告诉模型"这是你刚才要的数据"）
# ---------------------------------------------------------------------------

messages = [
    # system 消息：给模型设定角色和行为
    {"role": "system", "content": "你是一个智能助理,可以调用工具获取当前时间和天气信息"},
    # user 消息：用户的提问
    {"role": "user", "content": "请告诉我现在的时间和北京的天气"}
]

# ---------------------------------------------------------------------------
# 第七部分：ReAct 循环（核心逻辑）
# ---------------------------------------------------------------------------
# 这是一个 while True 死循环，为什么需要循环？
#
# 因为模型可能不会一次性回答完——它的流程是这样的：
#
#   第1轮：用户问"现在几点？北京天气如何？"
#         → 模型想："我不知道时间，需要调 get_current_time；
#                   我也不知道天气，需要调 get_weather"
#         → 模型返回的不是文字回答，而是一个 tool_calls 请求
#         → 你的代码执行 get_current_time 和 get_weather
#         → 把结果作为 tool 消息塞回 messages
#
#   第2轮：messages 现在包含了工具返回的数据
#         → 模型拿到时间和天气数据后，综合成自然语言回复
#         → "现在是2024年6月1日12点，北京天气晴朗，气温25°C..."
#         → 此时没有 tool_calls，循环结束，输出最终答案
#
# 如果不用循环，模型第一次返回 tool_calls 时你就停住了，
# 用户永远看不到最终的回答。
# ---------------------------------------------------------------------------

while True:
    # ----- 7.1 调用 LLM -----
    # client.chat.completions.create() 是 OpenAI SDK 的核心方法，
    # 把整个 messages 列表发给模型，拿到模型的回复。
    #
    # 参数：
    #   model       ：用哪个模型
    #   messages    ：完整的对话历史
    #   tools       ：可用工具列表（就是上面定义的那两个）
    #                 模型看到这些工具后，会自行判断"要不要用、用哪个"
    #   temperature ：控制随机性，0~2 之间。
    #                 0  = 几乎不随机，每次回答一样（适合严肃场合）
    #                 0.7= 适度创意（适合聊天）
    #                 1+ = 越来越离谱
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        temperature=0.7
    )

    # ----- 7.2 提取模型的回复 -----
    # response.choices[0] 是模型的第一个（通常也是唯一一个）回复选项
    # .message 包含了回复的具体内容
    assitant_message = response.choices[0].message

    # ----- 7.3 把模型的回复加入对话历史 -----
    # 无论模型是返回文字还是返回 tool_calls，都要把它加进 messages
    # 这样下一轮对话时模型能看到自己说了什么
    messages.append(assitant_message)

    # ----- 7.4 判断：模型是想回答问题，还是想调工具？-----
    # assitant_message.tool_calls 为 None 或空  → 模型给了最终答案，可以结束了
    # assitant_message.tool_calls 不为空         → 模型想调工具，需要我们先执行工具
    if not assitant_message.tool_calls:
        # 没有工具调用 → 这就是最终回答，打印出来并退出循环
        print(f"最终回答:\n{assitant_message.content}")
        break

    # ----- 7.5 执行模型请求的所有工具调用 -----
    # 模型可能同时请求多个工具（比如又要查时间又要查天气），
    # 所以这里用 for 循环逐一处理。
    for tool_call in assitant_message.tool_calls:
        # tool_call 对象结构：
        #   .id              ：本次调用的唯一 ID（用于关联"谁返回的数据"）
        #   .function.name   ：要调用的工具名（如 "get_weather"）
        #   .function.arguments：模型生成的参数（JSON 字符串，如 '{"city":"北京"}'）

        # 调用我们写的 excute_tool 函数，执行真实的工具逻辑
        result = excute_tool(tool_call.function.name, tool_call.function.arguments)

        # ----- 7.6 把工具执行结果加入对话历史 -----
        # 这条消息的 role 是 "tool"，告诉模型："这是你刚才要的那个工具的结果"
        #
        # 字段说明：
        #   role          : "tool"，固定值，OpenAI 规定的角色名
        #   tool_call_id  : 关联的调用 ID，模型靠这个 ID 对应"哪个结果属于哪个调用"
        #   content       : 工具返回的数据（字符串），模型会阅读这个内容来生成最终答案
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })

    # 循环回到开头，把带工具结果的 messages 再次发给模型，
    # 模型会基于工具返回的数据生成最终答案。
    # 如果模型觉得还需要调更多工具，会继续返回 tool_calls，循环继续。
