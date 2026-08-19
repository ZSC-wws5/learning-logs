from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import requests
from datetime import datetime

load_dotenv()

KEY = os.getenv("DEEPSEEK_API_KEY")
URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")

client = OpenAI(
    api_key = KEY,
    base_url = URL
)

tools = [
    
]

