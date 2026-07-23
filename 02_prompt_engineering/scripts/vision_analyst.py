import os
import base64
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["MOONSHOT_API_KEY"], base_url="https://api.moonshot.cn/v1"
)



# 1. 设置图片路径（请确保图片位置正确）
image_path = r"C:\Users\76526\ai-agent-learning\02_prompt_engineering\images\chair.jpg"


if not os.path.exists(image_path):
    print(f"❌错误:找不到文件图片{image_path}，请确认文件放入 images 文件夹中。")
    exit()
    
with open(image_path,"rb")as f:
    image_data = f.read()

# 2. 定义图片编码函数（将照片转为数字电报）
image_url = (
    "data:image/jpeg;base64,"
    + base64.b64encode(image_data).decode()
)



print("AI 正在观察图片，请稍后...")

 # 3.发起多模态调用
completion = client.chat.completions.create(
        model="kimi-k2.6",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "你是一个资深家具 CMF 专家。请分析这张图中的家具，给出详细的材料、颜色和工艺分析报告。",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url":image_url,
                            },
                    },
                ],
            }
        ],
        max_tokens=500
    )

print("---视觉分析报告 ---")

print(completion.choices[0].message.reasoning_content)

        
# 设置输出内容保存文件
from pathlib import Path
from datetime import datetime
import re

# 保存目录
save_dir = Path(
    r"C:\Users\76526\ai-agent-learning\02_prompt_engineering\.gitignore\outputs"
)

# 如果不存在则创建
save_dir.mkdir(
    parents = True,
    exist_ok = True
)

# 文件名
title = "视觉分析报告"
date = datetime.now().strftime("%Y-%m-%d")

filename = f"{title}_{date}.md"

# 拼接完整路径
file_path =save_dir/filename


answer = completion.choices[0].message.reasoning_content
# 写入文件
with open(
    file_path,
    "w",
    encoding = "utf-8"
)as f:
    f.write(answer)
    
