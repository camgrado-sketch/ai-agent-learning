import os
from pathlib import Path
import base64
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["MOONSHOT_API_KEY"], base_url="https://api.moonshot.cn/v1"
)

def encode_image(image_path):
    with open(image_path,"rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
# 1.定义源文件夹和输出文件夹
input_dir = Path("labels")
output_dir = Path("research_notes")
output_dir.mkdir(exist_ok = True)


# 2.获取所有图片列表
image_files = list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.png"))
total_files = len(image_files)

print(f"启动自动化工厂，共发现 {total_files} 张图片待处理...\n")

# 3.开始循环处理
for index, img_path in enumerate(image_files,1):
    print(f"{index}/{total_files} 正在处理：{img_path.name}")
    
    try:
        # 编码图片
        base64_image =encode_image(img_path)
        
        # 调用AI(复用昨天的prompt)
        completion = client.chat.completions.create(
            model="kimi-k2.6",
            messages = [
                {
                    "role":"user",
                    "content":[
                        {"type":"text",
                                "text":"严格请识别图中的家具文字，整理为 Markdown 规格笔记。先做图片中的文字提炼分析，再对包含品牌、型号、参考价格、材质进行梳理记录。如若没有则为空"
                                },
                        {"type":"image_url",
                         "image_url":{
                             "url":f"data:image/jpeg;base64,{base64_image}"
                             },
                         },
                    ],
                }
            ],
            max_tokens= 500,
                extra_body={
                    "thinking":{
                        "type":"disabled"
                }
            }
        )
        
        note_content = completion.choices[0].message.content
        
        # 4.自动生成笔记文件名（图片 + .md）
        note_filename = output_dir/f"{img_path.stem}_note.md"
        
        print("AI返回内容：")
        print(note_content)
        
        with open(note_filename,"w",encoding= "utf-8") as f:
            f.write(note_content)
            
        print(f"已完成笔记：{note_filename.name}")
        
    except Exception as e:
        print(f"处理{img_path.name}时发生错误：{e}")
        continue #发生错误时进行处理下一张
    
print(f"全部任务完成！请在{output_dir.name}文件夹中查看结果！")

        
        