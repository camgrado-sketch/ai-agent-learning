import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["MOONSHOT_API_KEY"],
    base_url="https://api.moonshot.cn/v1",
)

# 1. 加载角色设定
with open("persona_defintions.json", "r", encoding="utf-8") as f:
    personas = json.load(f)

# 2.定义待评审的初始方案
initial_proposal = "在奢饰品牌展厅vip区配置 4 把 Walter knoll FK椅子，采用最高阶皮革，底座为手工抛光铝合金。"

# 3. 构造多角色评审 prompt
prompt = f"""
请模拟一场专业的家具方案评审会。

**待评审方案**：{initial_proposal}

**参与角色**：
1. 设计总监：{personas['design_director']}
2. 成本经理：{personas['cost_manager']}
3. 技术工程师：{personas['technical_engineer']}

**评审流程**：
- 请先让三位角色分别发表简短意见。
- 随后，三位角色进行一轮简短辩论，针对皮革分级和维护性达成共识。
- 最后，由设计总监输出一份优化后的“最终执行建议”。

请以markdown 格式输出。
"""

print("评审委员会正在激烈讨论中，请稍后...\n")


# 答案回复的流式输出设置
response = client.chat.completions.create(
    model="kimi-k3",
    messages =[{"role": "user", "content": prompt}],
    stream = True
)

for chunk in response:
    content = chunk.choices[0].delta.content
    
    if content:
        print(content, end="", flush=True)



# 提取模型输出内容
answer = response.choices[0].message.content

# 保存为 Markdown 文件
md_filename = "家具选品讨论意见.md"
markdown_content = f"""
#{md_filename}

{answer}

---
生成模型：GPT
"""

with open(md_filename, "w",encoding="utf-8") as f:
    f.write(answer)