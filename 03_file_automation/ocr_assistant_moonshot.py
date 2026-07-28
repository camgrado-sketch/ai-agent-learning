import os
import base64
from pathlib import Path
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["MOONSHOT_API_KEY"], base_url="https://api.moonshot.cn/v1"
)

# 1.编码函数
def encode_image(image_path):
    with open(image_path,"rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
# 2.路径设置
image_file = Path("labels/label_sample.jpg")

if not image_file.exists():
    print(f"错误！找不到图片{image_file}")
else:
    print(f"正在通过 AI 读取标签信息：{image_file.name}...")
    base64_image = encode_image(image_file)
    
    # 3.发起 AI 调用
    completion = client.chat.completions.create(
        model="kimi-k2.6",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "你是一位专业的设计师助手。请识别这张图片中的文字，并将其整理为一份 Markdown 格式的家具规格笔记。要求包含：品牌、型号、参考价格、材质说明。如果图片中有其他关键信息（如设计师），也请一并列出。",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url":f"data:image/jpeg;base64,{base64_image}",
                            },
                    },
                ],
            }
        ],
        max_tokens=500,
            extra_body={
                "thinking":{
                "type":"disabled"
            }
        }
    )
    
    result_text = completion.choices[0].message.content
    
    # 4.自动保存为 markdown 笔记
    output_file = Path(f"labels/{image_file.stem}_note.md")
    with open(output_file,"w",encoding="utf-8") as f :
        f.write(result_text)
        
    print(f"识别并整理完成！笔记已保存至：{output_file}")
    print("\n--- 笔记浏览 ---")
    print(result_text)