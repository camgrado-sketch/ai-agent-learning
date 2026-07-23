import os
from openai import OpenAI

client = OpenAI (
    api_key=os.environ['DEEPSEEK_API_KEY'],
    base_url ="https://api.deepseek.com" 
    )


# 1.读取长文本文件
with open(r"C:\Users\76526\ai-agent-learning\brand_research\2026米兰家具设计趋势深度研究报告.md","r",encoding="utf-8")as f:
    report_content = f.read()
    
# 2.构造提取prompt
prompt= f"""
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
你是一个资深的家具 CMF 专家。请阅读以下趋势报告，并提取关键信息。

**报告内容**：
{report_content}

**提取要求**：
1.请以 Markdown 表格形式列出文中提到的所有“品牌”、“核心材质”及“目标场景”。
3.如果文中提及了具体的设计师，请单独列出,并简要说明他们文章提及的相关情况。

请直接输出结果
"""

print("正在分析长文本并提取关键设计要素...\n")

response = client.chat.completions.create(
    model ="deepseek-v4-flash",
    messages=[{"role":"user","content":prompt}],
    temperature=0.2 ,#低温度避免幻觉
    stream = True
)


answer = ""

for chunk in response:
    content = chunk.choices[0].delta.content
    
    if content:
        print(content,end="",flush=True)
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
file_path = save_dir/filename

# 写入文件
with open(
    file_path,
    "w",
    encoding = "utf-8"
)as f:
    f.write(answer)