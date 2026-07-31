# Arper Inspirations 项目案例爬虫工具集

这是一套专门用于抓取 Arper 官网 [Inspirations（灵感案例）](https://www.arper.com/us_EN/blog/category/arper_inspirations.html) 页面的自动化脚本工具。

由于 Arper 的案例列表页混合了**静态跳转卡片**和**动态弹窗卡片**（需要点击才能看到标题和链接），且包含 `Load More` 按钮，因此工具被拆分为两步，并结合了 `Selenium`（动态点击）与 `requests`（静态解析）。

---

## 📂 文件结构

- `step1_collect_list.py`：脚本一，负责在列表页点击弹窗和加载按钮，导出所有案例的名称与链接到 CSV。
- `step2_scrape_to_md.py`：脚本二，负责根据 CSV 逐一访问详情页，提取图文信息并生成 Markdown 文档。
- `arper_inspirations_selectors.yaml`：列表页的选择器配置（初学版参考）。
- `arper_detail_selectors.yaml`：详情页的选择器配置（供脚本二调用）。

---

## ⚙️ 环境配置（Windows）

1. **安装 Python**（建议 3.9+）
2. **打开命令提示符（CMD）或 PowerShell**，安装所需依赖库：

```cmd
pip install requests beautifulsoup4 selenium webdriver-manager pyyaml
```

*注：`webdriver-manager` 会自动帮你下载匹配当前电脑 Chrome 版本的驱动，无需手动配置环境。*

---

## 🚀 使用方法

### 方法 A：一键执行完整工作流（推荐）

直接运行第二个脚本，它会自动先调用第一个脚本生成 CSV，然后再生成 MD 文件：

```cmd
python step2_scrape_to_md.py
```

### 方法 B：分步执行

如果你只想先看看抓到的 CSV 列表对不对，可以先运行：

```cmd
python step1_collect_list.py
```
这会在当前目录下生成一个 `arper_inspirations.csv` 文件。

确认无误后，再运行第二个脚本（加上 `--skip` 参数表示跳过第一步，直接用刚才的 CSV）：

```cmd
python step2_scrape_to_md.py --skip
```

所有生成的 Markdown 文件都会保存在自动创建的 `output` 文件夹中。

---

## 🛠️ 如何修改脚本中的变量

每个 Python 脚本的开头都有一个明确的 **★ 可修改的变量区域**。

### 在 `step1_collect_list.py` 中：

```python
# 目标列表页网址（如果你想抓取 Country 或 Space 分类的页面，改这里）
LIST_URL = "https://www.arper.com/us_EN/blog/category/arper_inspirations.html"

# 输出的 CSV 文件路径
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "arper_inspirations.csv")
```

### 在 `step2_scrape_to_md.py` 中：

```python
# MD 文件的输出文件夹名称
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# 如果 Arper 以后要求登录才能看详情，把你在浏览器里登录后的 Cookie 填到这里
HEADERS = {
    "User-Agent": "Mozilla/5.0 ...",
    # "Cookie": "PHPSESSID=xxx; frontend=yyy;",  <-- 取消注释并替换为你的 Cookie
}
```

---

## 📝 Markdown 输出示例

生成的 `.md` 文件会自动包含以下结构，可直接拖入 Obsidian 等笔记软件：

```markdown
# Centro Medico SYNLAB Manifattura Firenze

**日期：** 21 April 2026
**来源：** [https://www.arper.com/us_EN/blog/centro-medico-synlab-manifattura-firenze.html](...)

---
## 项目图片
![](https://www.arper.com/media/wysiwyg/InspirationsPage/Arper_CentroMedicoSYNLAB_2.jpg)
![](https://www.arper.com/media/wysiwyg/InspirationsPage/Arper_CentroMedicoSYNLAB_1.jpg)

## Info
- **Location:** Firenze / Italy
- **Architect:** Frontini Architetti
- **Photo:** Courtesy of SYNLAB Italia

## 相关产品
- [Kiik](https://www.arper.com/us_EN/60220-20kiik-20composition-20-2315.html)
- [Kiik](https://www.arper.com/us_EN/60235-20kiik-20composition-20-233.html)
```

*(注意：由于 Arper 详情页中只显示产品缩略图，脚本二会自动访问产品链接去获取产品的真实名称，这会稍微增加一点抓取时间，但能保证数据完整。)*
