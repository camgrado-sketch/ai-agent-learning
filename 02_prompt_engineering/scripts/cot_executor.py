import os
from openai import DefaultHttpxClient,OpenAI

client = OpenAI(
     timeout=30.0,
    max_retries=0,
    http_client=DefaultHttpxClient(
    proxy="http://127.0.0.1:4780",
     ),
api_key=os.environ.get("OPENAI_API_KEY")
)

# 定义复杂项目
comflex_scenario = "世界 500 强科技公司总部的大厅休息区，需要兼顾员工非正式会议和访客接待，要求耐用且具有极客感。"

# 读取思维模板
with open("cot_analysis_template.md","r",encoding = "utf-8") as f:
    cot_template = f.read()

# 构造 Prompt
prompt = f"""
{cot_template}

### 当前任务目标：
「具体场景」= {comflex_scenario}
"""

print("AI 正在按步骤进行深度思考，请稍等... \n")

response = client.chat.completions.create(
    model = "gpt-4o",
    messages = [
        {"role":"user","content": prompt }
        ],
    temperature = 0.3 # 降低随机性，保证逻辑紧密
)

print("--- 深度调研报告 ---")
print(response.choices[0].message.content)

# 提取模型输出内容
answer = response.choices[0].message.content

# 保存为 Markdown 文件
md_filename = "cot_analysis_report.md"
markdown_content = f"""
#{md_filename}

{answer}


---
生成模型：GPT-4o

 """


with open(md_filename, "w", encoding="utf-8") as md_file:
    md_file.write(answer)