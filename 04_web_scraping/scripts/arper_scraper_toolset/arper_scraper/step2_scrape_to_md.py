# =============================================================
# step2_scrape_to_md.py
# Arper 项目详情页采集脚本
# 功能：读取 step1 生成的 CSV，逐一访问每个项目详情页，
#       提取项目名称、日期、图片、Info、相关产品，
#       输出为以项目名命名的 Markdown 文件
#
# 运行方式（Windows 命令行）：
#   python step2_scrape_to_md.py          ← 自动先运行 step1 生成 CSV
#   python step2_scrape_to_md.py --skip   ← 跳过 step1，直接使用已有 CSV
#
# 依赖安装：
#   pip install requests beautifulsoup4 selenium webdriver-manager pyyaml
#
# 输出文件：
#   output\项目名称.md（每个项目一个 MD 文件）
# =============================================================

import os
import re
import csv
import sys
import time
import yaml
import requests
from pathlib import Path
from bs4 import BeautifulSoup


# =============================================================
# ★ 可修改的变量区域
# =============================================================

# step1 生成的 CSV 文件路径（可修改）
INPUT_CSV = os.path.join(os.path.dirname(__file__), "arper_inspirations.csv")

# 详情页 Selector YAML 配置文件路径（可修改）
SELECTORS_YAML = os.path.join(os.path.dirname(__file__), "arper_detail_selectors.yaml")

# MD 文件输出目录（可修改为你想要的路径）
# Windows 路径示例："C:\\Users\\YourName\\Desktop\\arper_projects"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# 每次请求之间的间隔秒数（避免请求过快被封）
REQUEST_DELAY = 1.5

# 请求超时秒数
REQUEST_TIMEOUT = 20

# =============================================================


# 请求头，模拟正常浏览器访问
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    # ★ 如需登录后访问，将浏览器 Cookie 粘贴到下面这行（替换引号内内容）
    # "Cookie": "PHPSESSID=xxx; frontend=yyy;",
}


def load_selectors(yaml_path):
    """
    读取 YAML 配置文件，返回选择器字典。
    如果文件不存在，抛出错误提示。
    """
    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"找不到 YAML 配置文件：{yaml_path}")
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_csv(csv_path):
    """
    读取 step1 生成的 CSV，返回项目列表。
    每项为 {"title": ..., "url": ...}
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"找不到 CSV 文件：{csv_path}\n请先运行 step1_collect_list.py")
    projects = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            projects.append({"title": row["title"].strip(), "url": row["url"].strip()})
    print(f"  [CSV] 读取到 {len(projects)} 个项目")
    return projects


def fetch_page(url):
    """
    用 requests 静态抓取页面 HTML。
    Arper 详情页的核心数据（标题、日期、图片、Info）
    都在静态 HTML 里，无需 Selenium。
    返回 BeautifulSoup 对象，失败返回 None。
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        print(f"    [错误] 请求失败：{e}")
        return None


def get_text(soup, selector):
    """
    用 CSS 选择器找到元素，返回其文字内容（去除首尾空白）。
    找不到时返回空字符串。
    """
    el = soup.select_one(selector)
    return el.get_text(separator=" ", strip=True) if el else ""


def get_attrs(soup, selector, attr):
    """
    用 CSS 选择器找到所有匹配元素，返回指定属性值的列表。
    用于批量获取图片 src 或链接 href。
    """
    els = soup.select(selector)
    return [el.get(attr, "").strip() for el in els if el.get(attr, "").strip()]


def get_product_name(product_url):
    """
    访问产品详情页，从 h2.product-title 获取产品名称。
    产品名称不在灵感页里，需要二次请求产品页。
    失败时返回从 URL 解析的备用名称。
    """
    soup = fetch_page(product_url)
    if soup:
        name = get_text(soup, "h2.product-title")
        if name:
            return name
    # 备用：从 URL 中提取产品名（去掉 SKU 编号部分）
    slug = product_url.rstrip("/").split("/")[-1]
    slug = re.sub(r"-20article.*$", "", slug)
    slug = slug.replace("-20", " ").replace("-", " ").title()
    return slug


def sanitize_filename(name):
    """
    将项目名称转换为合法的文件名。
    去除 Windows 不允许的特殊字符，空格替换为下划线。
    """
    name = re.sub(r'[\\/:*?"<>|]', "", name)   # 去除非法字符
    name = name.strip().replace(" ", "_")        # 空格转下划线
    return name[:80]                             # 限制最大长度


def scrape_detail(url, selectors):
    """
    抓取单个项目详情页，提取所有目标字段。
    返回字典，包含：title / date / images / info / products
    """
    sel = selectors["project"]
    soup = fetch_page(url)
    if not soup:
        return None

    # ── 项目名称 ──
    title = get_text(soup, sel["title"]["selector"])

    # ── 发布日期 ──
    date = get_text(soup, sel["date"]["selector"])

    # ── 项目图片（正文现场照）──
    images = get_attrs(soup, sel["images"]["selector"], "src")

    # ── Info 区块 ──
    location  = get_text(soup, sel["info"]["location"]["selector"])
    architect = get_text(soup, sel["info"]["architect"]["selector"])
    photo     = get_text(soup, sel["info"]["photo_credit"]["selector"])

    # ── 相关产品（需二次请求产品页获取名称）──
    product_links = get_attrs(
        soup, sel["specified_products"]["product_links"]["selector"], "href"
    )
    products = []
    for purl in product_links:
        time.sleep(REQUEST_DELAY * 0.5)   # 产品页请求间隔（较短）
        pname = get_product_name(purl)
        products.append({"name": pname, "url": purl})
        print(f"      产品：{pname}")

    return {
        "title":     title,
        "date":      date,
        "images":    images,
        "location":  location,
        "architect": architect,
        "photo":     photo,
        "products":  products,
        "source_url": url,
    }


def render_markdown(data):
    """
    将采集到的数据渲染为 Markdown 格式字符串。
    MD 结构：
      # 项目名称
      日期
      ## 项目图片（图片嵌入）
      ## Info
      ## 相关产品
    """
    lines = []

    # 标题
    lines.append(f"# {data['title']}\n")

    # 日期
    if data["date"]:
        lines.append(f"**日期：** {data['date']}\n")

    # 来源链接
    lines.append(f"**来源：** [{data['source_url']}]({data['source_url']})\n")

    lines.append("---\n")

    # 项目图片
    lines.append("## 项目图片\n")
    if data["images"]:
        for src in data["images"]:
            # Markdown 图片语法：![alt](src)
            lines.append(f"![]({src})\n")
    else:
        lines.append("_暂无图片_\n")

    lines.append("")

    # Info
    lines.append("## Info\n")
    if data["location"]:
        lines.append(f"- **Location:** {data['location']}")
    if data["architect"]:
        lines.append(f"- **Architect:** {data['architect']}")
    if data["photo"]:
        lines.append(f"- **Photo:** {data['photo']}")
    lines.append("")

    # 相关产品
    lines.append("\n## 相关产品\n")
    if data["products"]:
        for p in data["products"]:
            # 产品名称 + 链接
            lines.append(f"- [{p['name']}]({p['url']})")
    else:
        lines.append("_暂无指定产品_")

    lines.append("")

    return "\n".join(lines)


def save_markdown(content, title, output_dir):
    """
    将 Markdown 内容保存为文件。
    文件名 = 项目名称（特殊字符已处理）.md
    使用 UTF-8 编码，Windows Obsidian / VS Code 均可正常打开。
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = sanitize_filename(title) + ".md"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def run(skip_step1=False):
    """
    主流程：
    1. （可选）调用 step1 生成 CSV
    2. 读取 CSV 和 YAML 配置
    3. 逐一访问详情页，提取数据
    4. 渲染为 MD 并保存
    """
    print("=" * 55)
    print("  Arper 项目详情页采集脚本")
    print("=" * 55)

    # ── 步骤 1：生成 CSV（可跳过）──
    if not skip_step1:
        print("\n[1/4] 调用 step1 生成项目列表 CSV...")
        # 动态导入 step1，确保两个脚本在同一目录
        sys.path.insert(0, os.path.dirname(__file__))
        import step1_collect_list
        step1_collect_list.run()
    else:
        print("\n[1/4] 跳过 step1，直接使用已有 CSV")

    # ── 步骤 2：读取 CSV 和 YAML ──
    print("\n[2/4] 读取配置文件...")
    projects  = load_csv(INPUT_CSV)
    selectors = load_selectors(SELECTORS_YAML)

    # ── 步骤 3 & 4：逐一抓取并保存 ──
    print(f"\n[3/4] 开始逐一抓取 {len(projects)} 个项目详情页...")
    print(f"      输出目录：{OUTPUT_DIR}\n")

    success = 0
    failed  = []

    for i, proj in enumerate(projects, 1):
        print(f"  [{i}/{len(projects)}] {proj['title']}")
        print(f"      URL: {proj['url']}")

        data = scrape_detail(proj["url"], selectors)

        if data is None:
            print(f"      [跳过] 抓取失败\n")
            failed.append(proj["title"])
            continue

        # 如果详情页标题为空，用 CSV 里的标题补充
        if not data["title"]:
            data["title"] = proj["title"]

        md_content = render_markdown(data)
        filepath   = save_markdown(md_content, data["title"], OUTPUT_DIR)
        print(f"      [完成] 已保存：{filepath}\n")
        success += 1

        # 请求间隔，避免触发反爬
        time.sleep(REQUEST_DELAY)

    # ── 汇总 ──
    print("=" * 55)
    print(f"  完成！成功 {success} 个，失败 {len(failed)} 个")
    if failed:
        print("  失败列表：")
        for f in failed:
            print(f"    - {f}")
    print(f"  MD 文件保存在：{OUTPUT_DIR}")
    print("=" * 55)


# 直接运行时执行主流程
if __name__ == "__main__":
    # 检查是否传入 --skip 参数（跳过 step1）
    skip = "--skip" in sys.argv
    run(skip_step1=skip)
