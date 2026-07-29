import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("KIMI_API_KEY")
base_url = os.getenv("KIMI_BASE_URL", "https://api.moonshot.cn/v1")
model = os.getenv("KIMI_MODEL", "moonshot-v1-8k")

if not api_key or api_key == "your_api_key_here":
    print("WARNING: KIMI_API_KEY is not set or is still the default value.")

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)

def ask_kimi(messages, temperature=1):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"API Error: {str(e)}"
