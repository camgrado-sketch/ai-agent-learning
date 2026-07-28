import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime

# 1.定义目标URL
# 这里以arper的官网举例，可以替换成任意网站
url = "https://www.arper.com/us_EN/"

# 2.发送HTTP请求，获取网页内容
print(f"正在访问网页：{url}...")
try:
    response = requests.get(url)
    response.raise_for_status() # 检查请求是否成功（200 ok）
    html_content = response.text
    print("网页内容获取成功！")
except requests.exceptions.RequestException as e:
    print(f"访问网页失败：{e}")
    exit()
    
    
# 3. 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(html_content,"html.parser")

#  4.提取网页标题
title = soup.find("title").get_text() if soup.find("title") else "无标题"
print(f"\n --- 网页标题 ---")
print(title)

# 5.提取网页的第一个段落内容（作为示例）
# 这里我们尝试找到第一个 <p> 标签的内容
first_paragraph = soup.find("p").get_text() if soup.find("p") else "无内容"
print(f"\n --- 网页第一个段落内容 ---")
print(first_paragraph.strip())

# 6.将提取的内容保存到 markdown 文件
output_dir =Path("outputs")
output_dir.mkdir(parents =True,exist_ok= True)
output_file = output_dir/"arper_homepage_summary.md"


with open(output_file,"w",encoding="utf-8") as f :
    f.write(f"# 网页标题：{title}\n\n")
    f.write(f"## 网址：{url}\n\n")
    f.write(f"### 提取内容摘要：\n\n")
    f.write(f">{first_paragraph.strip()}\n")
    f.write(f"\n --- \n\n *抓取时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
print(f"\n 提取内容保存至：{output_file}")