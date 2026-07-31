import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
from datetime import datetime

async def run():
    # 目标：Arper 灵感分类页
    url = "https://www.arper.com/us_EN/blog/category/arper_inspirations.html"
    output_path = Path("../outputs/arper_inspirations.md" )
    
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print(f"🚀 正在进入 Arper 灵感空间: {url}")
        
        await page.goto(url, wait_until="networkidle")
        
        # 1. 自动点击“Load More” 3 次（你可以根据需要调整次数）
        load_more_selector = ".load-more-btn"
        max_clicks = 3 
        
        # selector: #maincontent > div.columns > div > div:nth-child(3) > div.arperlab-listing-load-more-btn-container > button
        
        cookie_btn = page.locator(".iubenda-cs-accept-btn")

        
        
        for i in range(max_clicks):
            load_more_button = page.locator(load_more_selector)
            
            if await cookie_btn.count() > 0:
                        await cookie_btn.click()
                        await page.wait_for_timeout(1000)
                        
            if await load_more_button.is_visible():
                print(f"🖱️ 发现更多灵感，正在加载第 {i + 1} 组...")
                await load_more_button.click()
                # 关键：给动态内容一点渲染时间
                await page.wait_for_timeout(2500) 
            else:
                print("🏁 已加载全部内容。")
                break
        
        # 2. 此时页面已展开，收割所有标题
        # 根据分析，标题在 p.description 中
        title_locators = page.locator("a.thumbnail")
        titles = await title_locators.all_inner_texts()
        
        # 3. 整理并保存为 Markdown
        print(f"\n📊 调研成果：共抓取到 {len(titles)} 个灵感案例")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# Arper Inspirations 灵感调研报告\n\n")
            f.write(f"- **调研来源**: {url}\n")
            f.write(f"- **案例总数**: {len(titles)}\n")
            f.write(f"- **提取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## 案例清单\n\n")
            for i, title in enumerate(titles, 1):
                f.write(f"{i}. {title.strip()}\n")
                if i <= 10: print(f"  {i}. {title.strip()}") # 终端预览前10个

        print(f"\n✅ 报告已生成: {output_path}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
