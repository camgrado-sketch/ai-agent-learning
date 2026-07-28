# 动态网页识别插件
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
from datetime import datetime
import re

def clean_filename(filename):
    return re.sub(r'[\\/:*?"<>|]', '', filename)

async def scrape_website(target_url):
    output_dir =Path("outputs")
    output_dir.mkdir(exist_ok= True)
    print(f"正在使用 Playwright 访问网页：{target_url} ...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True) # headless = True 表示无头模式，不显示浏览器
        page = await browser.new_page()
        
        try:
            # 尝试使用 'domcontentloaded', 它在 DOM 结构加载完成后触发，不等待所有资源加载
            # 同时增加 timeout 到 60 秒，以应对加载较慢的网站
            await page.goto(target_url,wait_until = "domcontentloaded", timeout = 60000)
            print("网页内容加载成功！")
            
            # 获取整个页面的文本内容
            # 这里我们尝试获取 body 标签内的所有文本内容
            full_text_content = await page.evaluate("document.body.innerText")
            
            
            # 获取网页标题
            title = await page.title()
            safe_title = clean_filename(title)
            output_file = output_dir/f"{safe_title}_summary.md"
            
            
            # 写入 Markdown 文件
            with open(output_file,"w",encoding="utf-8") as f :
                f.write(f"# 网页标题：{title}\n\n")
                f.write(f"## 网址：{target_url}\n\n")
                f.write(f"### 提取内容摘要：\n\n")
                f.write(f">{full_text_content.strip()}\n")
                f.write(f"\n --- \n\n *抓取时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

            print(f"\n 提取内容保存至：{output_file}")
            
        except Exception as e:
            print(f"访问或提取网格失败：{e}")
        finally:
            await browser.close()

target_url = "https://www.arper.com"

if __name__ =="__main__":
    asyncio.run(scrape_website(target_url))





    
