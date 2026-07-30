import asyncio
from playwright.async_api import async_playwright
from pathlib import Path


async def run():
    url = "http://arper.com/us_EN/products/planning-ideas.html"  # 以空间配置方案页为例

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print(f"🚀 正在启动全量巡逻: {url}")

        await page.goto(url, wait_until="networkidle", timeout=60000)
       
       
        # 跳过cookie
        try:
            accept_button = page.locator(
                ".iubenda-cs-accept-btn"
            )

            # <button class="iubenda-cs-accept-btn iubenda-cs-btn-primary" tabindex="0" role="button">Save and continue</button>

            if await accept_button.count() > 0:

                await accept_button.click()
                print("Cookie 已关闭")

        except:
            pass

        
        # =====================
        # 保存所有项目
        # =====================
        
        all_titles = []
        
        page_number = 1
        
        # selector 变量设置（根据实际 F12 vs结果修改）
        load_more_selector = ".action.next"  
        item_button = ".product-full-tile"
        
        while True:
            
            print(
                f"📄 正在抓取第 {page_number} 页"
            )
            
            # 当前页抓取
            titles = await page.locator(
               item_button
            ).all_text_contents()
            
            print(
                f"当前页发现 {len(titles)} 个项目"
            )
            
             # 累加
            all_titles.extend(titles)
            
            
             # 找下一页
            next_button = page.locator(
                load_more_selector
            )
            
            if await next_button.count() == 0:

                print(
                    "🏁 已经是最后一页"
                )

                break
            
            
            
            # 点击下一页
            # 加入跳过cookie机制？
            next_url = await next_button.get_attribute(
                "href"
            )

            await page.goto(
                next_url,
                wait_until="domcontentloaded"
            )

            await page.wait_for_timeout(
                2000
            )


            page_number += 1
            
        print(
            "\n📊 最终总项目数量:",
            len(all_titles)
        )

        # 打印前十的项目信息
        for i, title in enumerate(
            all_titles[:10],
            1
        ):
        
            print(
                f"{i}. {title.strip()}"
            )


        await browser.close()


if __name__ == "__main__":
    asyncio.run(run())




#旧代码
''' # 1. 循环点击“加载更多”
        load_more_selector = ".action.next"  # 请根据实际 F12 vs结果修改

        # maincontent > div > div.column.main > div.products-pagination > div > div.pages > ul > li.item.pages-item-next > a

        click_count = 0
        while True:
            load_more_button = page.locator(load_more_selector)

            # 检查按钮是否可见且可用
            if await load_more_button.is_visible():
                print(f"🖱️ 发现加载按钮，正在点击第 {click_count + 1} 次...")
                await load_more_button.click()
                click_count += 1
                # 等待新内容加载（简单等待 2 秒）
                await page.wait_for_timeout(2000)
            else:
                print("🏁 没有更多内容可以加载了。")
                break

        # 2. 此时页面已完全展开，开始抓取
        # 假设新闻标题的 class 是 .product-full-tile
        titles = await page.locator(".product-full-tile").all_text_contents()

        print(f"\n📊 最终收割成果：共抓取到 {len(titles)} 条空间项目")
        for i, title in enumerate(titles[:10], 1):  # 只打印前10个预览
            if False:  # 调试跳过
                print(f"  {i}. {title.strip()}")

        await browser.close()'''