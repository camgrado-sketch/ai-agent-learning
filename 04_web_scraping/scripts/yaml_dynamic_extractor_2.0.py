import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
from datetime import datetime
import yaml
import re
import csv


# ======================================
# 1. 路径配置
# ======================================

CSV_PATH = Path("../data/arper_collection.csv")

YAML_PATH = Path(
    "../config/arper_selectors_simple.yaml"
)

OUTPUT_DIR = Path("../outputs")



# ======================================
# 2. 读取 YAML 配置
# ======================================

def load_selector_config():

    with open(
        YAML_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        return yaml.safe_load(f)



# ======================================
# 3. 清理文件名
# ======================================

def clean_filename(name):

    if not name:
        return "unknown_product"


    name = name.strip()

    # 删除Windows非法字符

    name = re.sub(
        r'[\\/:*?"<>|]',
        "",
        name
    )
    
    name = name.replace(".", "")

    name = re.sub(
        r'\s+',
        "_",
        name
    )

    name = re.sub(
        r'_+',
        "_",
        name
    )

    return name.strip("_")

    



# ======================================
# 4. 提取设计师
# ======================================

def extract_designer(text):

    match = re.search(
        r"Design\s+by\s*\n?\s*([A-Za-z\s]+?)(?:,\s*\d{4})?(?:\n|$)",
        text
    )


    if match:

        return match.group(1).strip()


    return "N/A"



# ======================================
# 5. 提取设计说明
# ======================================

def extract_description(text):

    description = re.sub(
        r"Design\s+by\s+.+\n?",
        "",
        text
    )


    return description.strip()



# ======================================
# 6. 单个产品抓取函数
# ======================================

async def scrape_product(
        page,
        product_url,
        product_name,
        config
):


    print("\n正在访问:")
    print(product_url)



    await page.goto(
        product_url,
        wait_until="domcontentloaded",
        timeout=60000
    )


    print(
        "网页标题:",
        await page.title()
    )

    

    # -----------------------------
    # 设计师信息
    # -----------------------------


    designer_selector = (
        config["product"]
        ["designer"]
        ["selector"]
    )


    designer_locator = page.locator(
        designer_selector
    )


    if await designer_locator.count()>0:

        detail_text = (
            await designer_locator
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



    # -----------------------------
    # 图片
    # -----------------------------


    image_selector = (
        config["product"]
        ["images"]
        ["selector"]
    )


    image_locator = page.locator(
        image_selector
    )


    if await image_locator.count()>0:


        images = await image_locator.evaluate_all(
            """
            imgs =>
            imgs.map(
                img=>img.getAttribute("src")
            )
            """
        )


    else:

        images=[]



    print(
        "图片数量:",
        len(images)
    )



    # 返回数据

    return {

        "name": product_name,

        "url": product_url,

        "designer": designer,

        "description": description,

        "images": images
    }




# ======================================
# 7. 保存 Markdown
# ======================================


def save_markdown(data):


    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
        
        
        
        
    )

    filename = clean_filename(
    data["name"]
    )


    timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)


    output_file = (
    OUTPUT_DIR /
    f"{filename}.md"
    )
   


    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:



        f.write(
            f"# 产品信息：{data['name']}\n\n"
        )


        f.write(
            f"- 产品网址:\n{data['url']}\n\n"
        )


        f.write(
            "## 设计师\n\n"
        )


        f.write(
            f"{data['designer']}\n\n"
        )


        f.write(
            "## 设计说明\n\n"
        )


        f.write(
            f"{data['description']}\n\n"
        )


        f.write(
            "## 产品图片\n\n"
        )



        for img in data["images"]:

            f.write(
                f"![]({img})\n\n"
            )



        f.write(
            "\n---\n"
        )


        f.write(
            "数据时间:"
            +
            datetime.now()
            .strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )



    print(
        "✅ 保存:",
        output_file
    )





# ======================================
# 8. 主程序
# ======================================


async def main():


    config = load_selector_config()



    async with async_playwright() as p:


        browser = await p.chromium.launch(
            headless=True
        )


        page = await browser.new_page()



        with open(
            CSV_PATH,
            "r",
            encoding="utf-8-sig"
        ) as f:



            products = csv.DictReader(f)



            for product in products:



                name = product["名称"]

                url = product["链接"]



                print(
                    "\n======================"
                )

                print(
                    "开始:",
                    name
                )



                try:


                    data = await scrape_product(
                        page,
                        url,
                        name,
                        config
                    )

                    print("原始名称:", name)

                    clean_name = clean_filename(name)

                    print("清理后:", clean_name)
                    
                    
                    save_markdown(
                            data
                        )


                except Exception as e:


                    print(
                        "❌失败:",
                        e
                    )



        await browser.close()




# ======================================
# 程序入口
# ======================================

if __name__ == "__main__":


    asyncio.run(
        main()
    )