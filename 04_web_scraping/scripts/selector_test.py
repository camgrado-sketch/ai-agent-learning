from playwright.sync_api import sync_playwright

# ============================
# 修改这里
# ============================

URL = "https://www.arper.com/us_EN/products/planning-ideas.html"


# 你要测试的 selector
SELECTOR = ".iubenda-cs-accept-btn"

# <button class="iubenda-cs-accept-btn iubenda-cs-btn-primary" tabindex="0" role="button">Save and continue</button>
# .product-full-tilE

# ============================
# 测试程序
# ============================


def test_selector():

    with sync_playwright() as p:

        # 启动浏览器
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        print("正在打开网页...")

        page.goto(URL, wait_until="networkidle", timeout=60000)

        print("\n网页打开完成")

        # ============================
        # 测试 selector
        # ============================

        locator = page.locator(SELECTOR)

        count = locator.count()

        print("---------------------------")
        print("测试 selector:")
        print(SELECTOR)

        print("---------------------------")

        print(f"找到元素数量: {count}")

        if count == 0:

            print("❌ selector 无效，没有找到元素")

        else:

            print("✅ selector 有效")

            print("\n前5个元素内容:")

            for i in range(min(count, 5)):

                text = locator.nth(i).inner_text()

                print(f"{i+1}: {text}")

            print("\n第一个元素HTML:")

            html = locator.first.evaluate("(el)=>el.outerHTML")

            print(html)

        input("\n按Enter关闭浏览器...")

        browser.close()


if __name__ == "__main__":

    test_selector()
