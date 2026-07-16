import os
import json
from openai import OpenAI

client = OpenAI(
	api_key=os.environ.get("DEEPSEEK_API_KEY"),
	base_url="https://api.deepseek.com"
)

# 定义我们要提取的产品
product_name = "Arper Catifa 53"

# 构造一个极度严谨的 System Prompt
system_instruction = """
你是一位家具数据分析师。请分析指定产品的参数，并严格以 JSON 格式输出。
JSON 必须包含以下字段：
- product_name (字符串)
- designer (字符串)
- materials (数组)
- is_stackable (布尔值)
- primary_scene (字符串，如 Office/Home/Retail)
- price_level (字符串，用 $ 到 $$$$$ 表示)

不要输出任何多余的解释文字，只输出 JSON。
"""

print(f"正在提取 {product_name} 的结构化数据...")

response = client.chat.completions.create(
    model="deepseek-chat",
    # 部分模型支持 response_format={"type": "json_object"}
    # 如果使用该设置，Prompt 中必须包含 "json" 字样
    messages=[
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": f"请提取产品 {product_name} 的数据。"}
    ]
)

# 获取原始字符串
raw_json = response.choices[0].message.content

# 尝试解析并保存
try:
    # 验证是否为合法 JSON
    data = json.loads(raw_json)
    
    file_path = f"furniture_data/{product_name.replace(' ', '_')}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"✅ 成功！数据已保存至 {file_path}")
    print("提取到的内容：")
    print(json.dumps(data, indent=2, ensure_ascii=False))

except Exception as e:
    print(f"❌ 错误：AI 输出的内容不是合法 JSON。报错信息：{e}")
    print("原始输出如下：")
    print(raw_json)
