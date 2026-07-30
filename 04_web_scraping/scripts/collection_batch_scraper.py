import asyncio
import csv
from playwright.async_api import async_playwright
from pathlib import Path


async def run():
    url = "https://www.arper.com/us_EN/products/chairs-and-stools.html?id=6&collection_type=57&group_by_collection=0"  # 替换为你的目标系列页
    output_path = Path("../outputs/arper_collection.csv")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print(f"🚀 正在巡逻系列页面: {url}")

        await page.goto(url, wait_until="networkidle")

        # 1. 定位所有产品卡片 (请根据实际 F12 结果修改选择器)
        # 假设每个产品是一个带有 class="product-card" 的元素
        cards = await page.locator(".product-full-tile").all()
        print(f"📊 找到 {len(cards)} 个产品项目")

        # 导出真实的 HTML 架构
        for i, card in enumerate(cards[:3]):
            print(await card.evaluate("(el)=>el.tagName"))
            text = await card.inner_text()
            print(text)

            print("\n====== 第", i, "个产品 ======")

            html = await card.evaluate("(el)=>el.outerHTML")

            print(html[:1000])

        product_list = []

        # 2. 循环提取信息
        for card in cards:
            # 在每个卡片范围内寻找名称和链接
            name_el = card.locator(".product-item-link")  # 替换为实际选择器
            link_el = card.locator("a")  # 通常卡片本身或内部有链接

            name = (
                await name_el.text_content()
                if await name_el.count() > 0
                else "未知名称"
            )
            link = await card.get_attribute("href")

            # 补全完整 URL
            full_link = f"https://www.arper.com{link}" if link.startswith("/") else link

            product_list.append({"名称": name.strip(), "链接": full_link})

        # 3. 写入 CSV 文件
        with open(output_path, mode="w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["名称", "链接"])
            writer.writeheader()
            writer.writerows(product_list)

        print(f"✅ 成功！已将 {len(product_list)} 条数据导出至: {output_path}")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
