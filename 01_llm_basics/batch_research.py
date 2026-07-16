import os
from openai import OpenAI

# 1. 初始化 AI 客户端
client = OpenAI(
	api_key=os.environ.get("DEEPSEEK_API_KEY"),
	base_url="https://api.deepseek.com/v1"
)


# 2. 定义你的调研清单（你可以根据兴趣修改品牌名）
brands = ["Arper", "Viccarbe", "Walter Knoll"]

# 3. 开始循环加工
for brand in brands:
    print(f"正在调研品牌: {brand}...")
    
    # 调用 AI
    response = client.chat.completions.create(
        model="deepseek-chat", # 或 deepseek-chat
        messages=[
            {"role": "system", "content": "你是一位高端家具调研专家。"},
            {"role": "user", "content": f"请简述品牌 {brand} 的核心定位、代表作以及 CMF 特色。"}
        ]
    )
    
    content = response.choices[0].message.content
    
    # 4. 将结果保存到 research_outputs 文件夹下
    # 文件名会自动变成 Arper_report.md 等
    file_path = f"research_outputs/{brand}_report.md"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {brand} 调研报告\n\n")
        f.write(content)
        
    print(f"✅ {brand} 的报告已生成至 {file_path}")

print("\n--- 所有调研任务已完成！ ---")
