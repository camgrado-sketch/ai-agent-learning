import os
from openai import OpenAI
from datetime import datetime



# 初始化客户端，它会自动读取你刚才设定的环境变量
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
    # 如果你用的是 DeepSeek 或其他国内转发，请修改 base_url
    # base_url="https://api.deepseek.com" 
 )

# 定义你的调研品牌
brand_name = "Arper"

# 发起调用
response = client.chat.completions.create(
    model="deepseek-chat", # 或者使用 deepseek-chat
    messages=[
        {"role": "system", "content": """
你是一位高端家具品牌研究专家。

请针对家具品牌进行系统化CMF研究。

输出结构必须包含：

# 品牌定位
- 品牌背景
- 核心设计理念
- 市场定位

# 设计语言
- 设计风格
- 代表设计师
- 产品特点

# 核心CMF特征

## Color 色彩
分析：
- 主色体系
- 常用配色
- 色彩表达方式

## Material 材料
分析：
- 常用材料
- 材料组合方式
- 材料选择逻辑

## Finish 表面处理
分析：
- 木材处理
- 金属工艺
- 织物皮革工艺
- 特殊工艺

# 代表产品案例
列举代表产品并分析其CMF特点。

# 品牌差异化
分析该品牌与Cassina、Minotti、B&B Italia等高端家具品牌的区别。

要求：
- 使用Markdown格式
- 内容适合建立家具设计知识库
- 保持专业但易阅读
"""},
        {"role": "user", "content": f"请简述品牌 {brand_name} 的核心 CMF 特征。"}
    ]
)


# ==============================
# 5. 获取AI返回内容
# ==============================

report = response.choices[0].message.content


# ==============================
# 6. 设置保存路径
# ==============================

# 修改这里即可改变保存位置
base_path = r"C:\Users\76526\Furniture_Knowledge_Base\Brands"


# 创建品牌文件夹
brand_folder = os.path.join(
    base_path,
    brand_name
)

os.makedirs(
    brand_folder,
    exist_ok=True
)


# ==============================
# 7. 设置文件名（带日期）
# ==============================

date = datetime.now().strftime("%Y%m%d")

filename = os.path.join(
    brand_folder,
    f"{brand_name}_CMF研究报告_{date}.md"
)


# ==============================
# 8. 写入Markdown文件
# ==============================

with open(
    filename,
    "w",
    encoding="utf-8"
) as f:
    f.write(report)


# ==============================
# 9. 输出完成信息
# ==============================

print("--------------------------------")
print(f"{brand_name} 调研完成")
print(f"文件保存位置：")
print(filename)
print("--------------------------------")



