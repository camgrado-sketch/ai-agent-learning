import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ['DEEPSEEK_API_KEY'], 
    base_url="https://api.deepseek.com"
)

# 1. 初始错误信息
wrong_info = "Arper 的 Catifa 53 椅子是由德国品牌 Walter Knoll 生产的，其设计师是 Charles & Ray Eames。"

# 2. 读取核查协议规则
with open("verification_protocol.md","r",encoding="utf-8")as f:
    samples = f.read()

# 3. 构造具有“反思”步骤的prompt
prompt = f"""
请严格按照以下格式回答:

TITLE:
(这里写标题)
生成一个适合作为Markdown文件名的标题。

要求：
- 10~20个中文字符
- 简洁明确
- 不包含特殊符号
- 能概括本次分析主题

CONTENT:
(这里写正文)
你是一个极其严谨的家具行业档案归档员。
你需要参考核查协议去思考:{samples}

**待处理信息**：{wrong_info}

**执行步骤**：
1. 请指出上述信息存在的所有事实错误。
2. 请解释为什么这些信息是错误的（基于品牌历史和设计师作品集）
3.请给出最终准确的、可用于专业报告的描述。

请以md的表格形式输出核查结果。

"""

print("正在进行事实核查与逻辑验证... \n")

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[{"role": "user", "content": prompt}],
    reasoning_effort="low",
    temperature = 0 ,
    max_tokens=1000,
    stream=True,
)

answer = ""

for chunk in response:
    content = chunk.choices[0].delta.content

    if content:
        print(content, end="", flush=True)
        answer += content
# 增加保护机制
parts = answer.split("CONTENT:")

if len(parts) > 1:
    content = parts[1]
else:
    content = answer        
    
if "TITLE:" in answer:
    title = answer.split("TITLE:")[1].split("CONTENT:")[0].strip()
else:
    title = "AI分析报告"


# 设置输出内容保存文件
from pathlib import Path
from datetime import datetime
import re

# 保存目录
save_dir = Path(
    r"C:\Users\76526\ai-agent-learning\02_prompt_engineering\outputs"
)

# 如果不存在则创建
save_dir.mkdir(
    parents = True,
    exist_ok = True
)

# 文件名
title = title.replace("TITLE:","").strip()
date = datetime.now().strftime("%Y-%m-%d")

filename = f"{title}_{date}.md"

# 拼接完整路径
file_path =save_dir/filename


# 写入文件
with open(
    file_path,
    "w",
    encoding = "utf-8"
)as f:
    f.write(answer)
    