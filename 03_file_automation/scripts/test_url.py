from openai import OpenAI
import time


print("开始连接")

client = OpenAI(
    api_key="OPENAI_API_KEY",
    timeout=15
)

start = time.time()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "你好"
        }
    ]
)

print("耗时:", time.time()-start)
print(response.choices[0].message.content)