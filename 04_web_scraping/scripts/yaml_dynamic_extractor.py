import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
from datetime import datetime
import yaml
import re

# ==============================
# 读取目标网站 YAML 配置文件
# ==============================
def load_selector_config():

    config_path = Path(r"..\config\arper_selectors_simple.yaml") # 这里做目标网站的架构 YAML配置清单

    with open(config_path, "r", encoding="utf-8") as f:

        return yaml.safe_load(f)



# ==============================
# 2. 清理文件名
# ==============================
def clean_filename(name):
    if not name:
        return"unknown_product"
    
    name = name.strip()
    # 删除Windows不允许的字符
    name = re.sub(r'[\\/:*?"<>|]', "", name)
    name = name.replace(
     " ",
        "_"
     )
    return name


# ==============================
# 3. 提取设计师
# ==============================

def extract_designer(text):

    match = re.search(
        r"Design\s+by\s*\n?\s*([A-Za-z\s]+?)(?:,\s*\d{4})?(?:\n|$)",
        text
    )


    if match:
        return match.group(1).strip()

    return "N/A"
    
    
# ==============================
# 4. 提取设计说明
# ==============================

def extract_description(text):

    description = re.sub(
        r"Design\s+by\s+.+\n?",
        "",
        text
    )


    return description.strip()
    
    
# ==============================
# 5. 主爬虫函数
# ==============================
async def scrape_arper_product_page(product_url):
    selectors = load_selector_config()
    output_dir = Path("../outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n启动 Playwright...")



    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # 无头模式
        page = await browser.new_page()

        try:
            await page.goto(product_url, wait_until="domcontentloaded", timeout=60000)
            print("✅ 网页内容加载成功！")
            print(
                "当前网址:",
                page.url
            )
            
            print(
                "网页标题:",
                await page.title()
            )

            # --- 在这里使用 Playwright 的 locator 和 evaluate 提取数据 ---
            # 请根据你在 Step 1 中找到的实际 CSS 选择器进行替换和添加

            # 示例：提取产品名称
            # 演示如何通过 selector变量去调用yaml文件中的标签
            name_selector = selectors["product"]["name"]["selector"]
            product_name_locator = page.locator(name_selector)
            product_name = (
                await product_name_locator.text_content()
                if await product_name_locator.count() > 0
                else "N/A"
            )
            
                # 根据yaml自动去命名
            print(f"🔍 正在使用 Playwright 访问产品页面: {product_name}...")
            print(f"产品名称: {product_name}")
            
            product_name = await product_name_locator.text_content()
            filename = clean_filename(product_name)
            output_file = output_dir / f"{filename}_data.md"

            # 示例：提取设计师 和设计描述
            # 假设设计师信息在 class 为 "designer-name" 的 div 内部的 a 标签中
            detail_selector = (
                selectors["product"]
                ["designer"]
                ["selector"]
            )


            detail_locator = page.locator(
                detail_selector
            )


            if await detail_locator.count() > 0:


                detail_text = (
                    await detail_locator
                    .first
                    .inner_text()
                )


            else:

                detail_text = ""



            designer = extract_designer(
                detail_text
            )


            description = extract_description(
                detail_text
            )



            print(
                "设计师:",
                designer
            )


            print(
                "设计说明:",
                description[:2000]
            )

            
        
            image_selector = selectors["product"]["images"]["selector"]
            #图片读取测试debug
            print(
                "图片selector:",
                image_selector
            )


            print(  
                "图片元素数量:",
            await page.locator(image_selector).count()
            )

            # 示例：提取产品图片链接 (通常在 img 标签的 src 属性中)
            # 假设主图的 img 标签有一个特定的 class，例如 "product-main-image"
            image_locator = page.locator(image_selector)  # 请替换为实际的选择器
            images = (
                await image_locator
                .evaluate_all(
                    """
                    imgs => imgs.map(
                        img => img.getAttribute("src")
                    )
                    """
                )
                if await image_locator.count() > 0
                else []
            )
            print(
                "图片数量:",
                len(images)
            )



            # 写入 Markdown 文件
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(
                    f"# 产品信息：{product_name}\n\n"
                )


                f.write(
                    f"- 产品网址: {product_url}\n\n"
                )


                f.write(
                    f"## 设计师\n\n"
                )


                f.write(
                    f"{designer}\n\n"
                )


                f.write(
                    "## 设计说明\n\n"
                )


                f.write(
                    f"{description}\n\n"
                )


                f.write(
                    "## 产品图片\n\n"
                )


                for img in images:

                    f.write(
                        f"![]({img})\n\n"
                    )


                f.write(
                    "\n---\n"
                )


                f.write(
                    f"\n数据时间："
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )



            print(
                "\n✅ 文件保存:",
                output_file
            )

        except Exception as e:
            print(f"❌ 访问或提取网页内容失败: {e}")
        finally:
            await browser.close()


# ==============================
# 6. 测试入口
# ==============================

if __name__ == "__main__":


    test_url = (
        "https://www.arper.com/us_EN/6100-20article-206100.html"
    )


    asyncio.run(
        scrape_arper_product_page(
            test_url
        )
    )


