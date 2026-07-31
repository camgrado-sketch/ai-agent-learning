from playwright.sync_api import sync_playwright


# ============================
# 网页地址
# ============================

URL = "https://www.arper.com/us_EN/blog/category/arper_inspirations.html"



# ============================
# 批量测试 selector
# ============================

SELECTORS = {

    "项目卡片": "a.thumbnail",

    "加载更多": ".load-more-btn",

    "Cookie按钮": ".iubenda-cs-accept-btn"

}



# ============================
# 测试函数
# ============================


def test_selectors():


    with sync_playwright() as p:


        browser = p.chromium.launch(
            headless= True
        )


        page = browser.new_page()


        print("打开网页...")


        page.goto(
            URL,
            wait_until="networkidle",
            timeout=60000
        )


        print(
            "网页加载完成\n"
        )



        # ============================
        # Cookie关闭
        # ============================

        try:

            cookie = page.locator(
                ".iubenda-cs-accept-btn"
            )


            if cookie.count() > 0:

                cookie.click()

                print(
                    "Cookie关闭成功"
                )


        except Exception:

            pass



        print("\n开始测试 selector")
        print("="*50)



        # ============================
        # 循环测试
        # ============================

        for name, selector in SELECTORS.items():

            locator = page.locator(selector)


            print("\n====================")

            print(
                "名称:",
                name
            )

            print(
                "Selector:",
                selector
            )


            count = locator.count()


            print(
                "数量:",
                count
            )

            count = locator.count()


            if count == 0:

                print(
                    "❌ 未找到"
                )


            else:


                visible = locator.first.is_visible()


                print(
                    "✅ 找到"
                )


                print(
                    "是否可见:",
                    visible
                )



                # 打印第一个文本

                try:

                    text = (
                        locator.first
                        .inner_text()
                    )

                    print(
                        "示例:",
                        text[:100]
                    )


                except:

                    print(
                        "无文本"
                    )



                # 打印HTML片段

                html = locator.first.evaluate(
                    "(el)=>el.outerHTML"
                )


                print(
                    "HTML:",
                    html[:200]
                )


            print(
                "-"*50
            )



        input(
            "\n按Enter关闭..."
        )


        browser.close()



if __name__ == "__main__":

    test_selectors()