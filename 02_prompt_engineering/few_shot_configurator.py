import os
from openai import DefaultHttpxClient,OpenAI

client = OpenAI(
    timeout=30.0,
    max_retries=0,
    http_client=DefaultHttpxClient(
        proxy="http://127.0.0.1:4780",
     ),
     api_key=os.getenv("OPENAI_API_KEY")
     )

# 1. 读取你的专业样板
with open("my_style_samples.md", "r",encoding="utf-8") as f:
    samples = f .read()

# 2. 定义新任务
new_client_need = "科技公司创始人办公室，追求敏捷、现代与自然氛围的结合。"

# 3.构造 Few-Shot Prompt 
prompt = f"""
你是一个顶级的家具配置专家。请参考一下我的专业案例风格，为新客户提供建议。

### 我的专业案例参考：
「{samples}

### 当前新任务：
**客户需求**：{new_client_need}」
**选品逻辑**：
**推荐方案**：
**设计评述**：
"""

print("正在生成配置建议……")

response = client.chat.completions.create(
    model = "gpt-4o",
    messages = [
        {"role": "user", "content": prompt}
    ],
    temperature = 0.7, # 稍微给一点创意空间
    max_tokens = 1000
)

print("\n --- AI 生成的专业建议 ---")
print(response.choices[0].message.content)

# 提取模型输出内容
answer = response.choices[0].message.content


# 保存为 Markdown 文件
md_filename = "科技公司家具配置建议.md"
markdown_content = f"""
#{md_filename}

{answer}

---
生成模型：GPT
"""

with open(md_filename, "w",encoding="utf-8") as f:
    f.write(answer)