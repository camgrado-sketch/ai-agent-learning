import os
from openai import OpenAI

client = OpenAI(
	api_key=os.environ.get("DEEPSEEK_API_KEY"),
	base_url="https://api.deepseek.com",
)

def get_research(brand,mode="unlimited"):
	if mode == "strict":
		# 严格模式；低温度，严格限制字数
		temp = 0.0
		max_t = 100
		prompt = f"仅用3句话总结「{brand}」的核心材质特色。"
	else:
		# 默认模式；允许输出更多内容
		temp = 0.7
		max_t = 1000
		prompt = f"请详细分析「{brand}」的材质特色。"

	response = client.chat.completions.create(
		model="deepseek-chat",
		messages=[
			{"role": "user", "content": prompt}
		],
		temperature=temp,
		max_tokens=max_t
	)

	return response.choices[0].message.content, response.usage

# 测试品牌
brand_to_test = "walter knoll"

print(f"--- 模式 A：无限制调研 ---")
content_a, usage_a = get_research(brand_to_test, "unlimited")
print(content_a)
print(f"消耗 Token：{usage_a.total_tokens}\n")

print(f"--- 模式 B：严格成本控制 ---")
content_b, usage_b = get_research(brand_to_test, "strict")
print(content_b)
print(f"消耗 Token：{usage_b.total_tokens}")

savings = (1 - usage_b.total_tokens / usage_a.total_tokens)*100
print(f"\n严格模式帮你节省约{savings:.1f}%的 Token 消耗。")
