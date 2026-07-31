# =============================================================
# step1_collect_list.py
# Arper Inspirations 项目案例列表采集脚本
# 功能：抓取所有灵感案例的项目名称和链接，导出为 CSV
#
# 运行方式（Windows 命令行）：
#   python step1_collect_list.py
#
# 依赖安装：
#   pip install selenium webdriver-manager
#
# 输出文件：
#   arper_inspirations.csv（与本脚本同目录）
# =============================================================

import csv
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, ElementClickInterceptedException
)
from webdriver_manager.chrome import ChromeDriverManager


# =============================================================
# ★ 可修改的变量区域
# =============================================================

# 目标列表页网址（可替换为其他分类页）
LIST_URL = "https://www.arper.com/us_EN/blog/category/arper_inspirations.html"

# 输出 CSV 文件路径（可修改文件名或路径）
# Windows 路径示例："C:\\Users\\YourName\\Desktop\\arper_inspirations.csv"
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "arper_inspirations.csv")

# 每次操作之间的等待秒数（网速慢时可适当调大）
WAIT_TIMEOUT = 15       # 等待元素出现的最长秒数
CLICK_DELAY  = 1.5      # 点击弹窗后等待内容加载的秒数
LOAD_MORE_DELAY = 2.0   # 点击 Load More 后等待新卡片加载的秒数

# =============================================================


def build_driver():
    """
    初始化 Chrome 浏览器（无头模式，不弹出窗口）
    webdriver-manager 会自动下载匹配的 ChromeDriver，无需手动配置
    """
    opts = Options()
    opts.add_argument("--headless=new")          # 无头模式，不显示浏览器窗口
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1440,900")
    opts.add_argument("--lang=en-US")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=opts)


def dismiss_cookie_banner(driver):
    """
    自动关闭 Cookie 同意弹窗。
    Arper 使用 iubenda 的 Cookie 横幅，按钮文字为 "Accept" 或类似字样。
    如果找不到按钮（已关闭或不存在），静默跳过。
    """
    try:
        # 等待最多 5 秒，找到 Accept 按钮并点击
        btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button#iubenda-cs-accept-btn, .iubenda-cs-accept-btn, [class*='accept']")
            )
        )
        btn.click()
        print("  [Cookie] 已自动关闭 Cookie 横幅")
        time.sleep(0.5)
    except TimeoutException:
        # 没有找到按钮，跳过
        print("  [Cookie] 未检测到 Cookie 横幅，跳过")


def click_load_more(driver):
    """
    循环点击 "Load More" 按钮，直到按钮消失为止。
    每次点击后等待新卡片加载完成。
    返回总点击次数。
    """
    click_count = 0
    while True:
        try:
            # 找到 Load More 按钮（.inspiration-load-more）
            btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.inspiration-load-more")
                )
            )
            # 滚动到按钮位置，确保可点击
            driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            time.sleep(0.5)
            btn.click()
            click_count += 1
            print(f"  [Load More] 第 {click_count} 次点击，等待新卡片加载...")
            time.sleep(LOAD_MORE_DELAY)
        except TimeoutException:
            # 按钮消失，说明已加载全部内容
            print(f"  [Load More] 所有内容已加载完毕，共点击 {click_count} 次")
            break
    return click_count


def collect_case_study_cards(driver):
    """
    采集 Case Study 类型卡片（.post.case_study）。
    这类卡片的标题和链接直接写在 HTML 里，无需点击弹窗。
    返回：[{"title": ..., "url": ...}, ...]
    """
    results = []
    cards = driver.find_elements(By.CSS_SELECTOR, ".inspirations-listing .post.case_study")
    for card in cards:
        try:
            # 标题在 a.thumbnail 的 title 属性里
            a = card.find_element(By.CSS_SELECTOR, "a.thumbnail")
            title = a.get_attribute("title").strip()
            url   = a.get_attribute("href").strip()
            if title and url:
                results.append({"title": title, "url": url})
        except NoSuchElementException:
            continue
    return results


def collect_popup_cards(driver):
    """
    采集 Popup 类型卡片（.post.popup_posts）。
    这类卡片需要逐一点击，等待弹窗出现后，
    从弹窗的 h1.modal-title 取标题，从 #projectBtn a 取链接。
    点击完成后关闭弹窗，继续下一张。
    返回：[{"title": ..., "url": ...}, ...]
    """
    results = []

    # 获取所有 popup 卡片（每次点击后页面可能刷新，需重新查找）
    cards = driver.find_elements(By.CSS_SELECTOR, ".inspirations-listing .post.popup_posts")
    total = len(cards)
    print(f"  [Popup] 共发现 {total} 张弹窗卡片，开始逐一点击...")

    for i in range(total):
        try:
            # 每次重新查找，避免 stale element 报错
            cards = driver.find_elements(By.CSS_SELECTOR, ".inspirations-listing .post.popup_posts")
            card  = cards[i]

            # 滚动到卡片位置
            driver.execute_script("arguments[0].scrollIntoView(true);", card)
            time.sleep(0.5)

            # 点击卡片，触发弹窗
            card.click()
            print(f"  [Popup] 点击第 {i+1}/{total} 张卡片，等待弹窗...")

            # 等待弹窗出现（aside.post-popup-container 变为可见）
            WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "aside.post-popup-container")
                )
            )
            time.sleep(CLICK_DELAY)

            # 从弹窗中提取项目名称
            title_el = driver.find_element(By.CSS_SELECTOR, "aside.post-popup-container h1.modal-title")
            title = title_el.text.strip()

            # 从弹窗中提取 "Go to Project" 链接
            url_el = driver.find_element(By.CSS_SELECTOR, "#projectBtn a")
            url = url_el.get_attribute("href").strip()

            print(f"    → {title}")
            results.append({"title": title, "url": url})

            # 关闭弹窗（点击 Close 按钮）
            close_btn = driver.find_element(
                By.CSS_SELECTOR, "aside.post-popup-container button.action-close"
            )
            close_btn.click()
            time.sleep(0.8)

        except (TimeoutException, NoSuchElementException) as e:
            print(f"  [Popup] 第 {i+1} 张卡片处理失败：{e}，跳过")
            # 尝试关闭可能残留的弹窗
            try:
                driver.find_element(
                    By.CSS_SELECTOR, "aside.post-popup-container button.action-close"
                ).click()
                time.sleep(0.5)
            except Exception:
                pass
            continue

    return results


def save_to_csv(data, filepath):
    """
    将采集结果保存为 CSV 文件。
    CSV 包含两列：title（项目名称）、url（详情页链接）
    使用 UTF-8 BOM 编码，确保 Windows Excel 直接打开不乱码。
    """
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "url"])
        writer.writeheader()
        writer.writerows(data)
    print(f"\n  [CSV] 已保存 {len(data)} 条记录到：{filepath}")


def run():
    """
    主流程：
    1. 打开列表页
    2. 关闭 Cookie 横幅
    3. 循环点击 Load More 直到加载全部
    4. 采集 Case Study 卡片（静态）
    5. 采集 Popup 卡片（动态点击）
    6. 合并去重，保存 CSV
    """
    print("=" * 55)
    print("  Arper Inspirations 列表采集脚本")
    print(f"  目标页面：{LIST_URL}")
    print("=" * 55)

    driver = build_driver()

    try:
        # ── 步骤 1：打开列表页 ──
        print("\n[1/5] 打开列表页...")
        driver.get(LIST_URL)

        # 等待卡片容器出现
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".inspirations-listing"))
        )

        # ── 步骤 2：关闭 Cookie 横幅 ──
        print("\n[2/5] 处理 Cookie 横幅...")
        dismiss_cookie_banner(driver)

        # ── 步骤 3：Load More ──
        print("\n[3/5] 加载全部内容（Load More）...")
        click_load_more(driver)

        # ── 步骤 4：采集 Case Study 卡片 ──
        print("\n[4/5] 采集 Case Study 卡片...")
        case_study_data = collect_case_study_cards(driver)
        print(f"  → 采集到 {len(case_study_data)} 条 Case Study")

        # ── 步骤 5：采集 Popup 卡片 ──
        print("\n[5/5] 采集 Popup 弹窗卡片...")
        popup_data = collect_popup_cards(driver)
        print(f"  → 采集到 {len(popup_data)} 条 Popup 项目")

    finally:
        driver.quit()

    # ── 合并 & 去重（以 url 为唯一键）──
    all_data = case_study_data + popup_data
    seen_urls = set()
    unique_data = []
    for item in all_data:
        if item["url"] not in seen_urls:
            seen_urls.add(item["url"])
            unique_data.append(item)

    print(f"\n  合计采集 {len(unique_data)} 个项目（去重后）")

    # ── 保存 CSV ──
    save_to_csv(unique_data, OUTPUT_CSV)

    print("\n  完成！")
    return unique_data


# 直接运行时执行主流程
if __name__ == "__main__":
    run()
