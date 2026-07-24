from pathlib import Path

# 1.定义我要扫描的路径（使用 Path 对象，它会自动处理 windows 路径）
# . 代表当前文件夹
base_path = Path("messy_assets")


print(f"--- 正在扫描文件夹：{base_path.absolute()}---\n")


# 2.初始统计数据
stats = {".jpg": 0, ".pdf": 0, ".md": 0, "others": 0}


# 3.开始遍历文件夹中所有文件
# rglob（"*") 代表递归搜索所有文件
for file in base_path.rglob("*"):
    if file.is_file():  # 确保我们处理的是文件而不是文件夹
        suffix = file.suffix.lower()  # 获取文件后缀，如 .jpg

        if suffix in stats:
            stats[suffix] += 1
        else:
            stats["others"] += 1
        print(f"发现文件：{file.name}(类型：{suffix})")
        

# 4.输出统计报告
print("\n--- 素材库统计报告 ---")
print(f"图片（JPG):{stats['.jpg']}个")
print(f"文档（PDF）:{stats['.pdf']}个")
print(f"笔记（MD）:{stats['.md']}个")
print(f"其他：{stats['others']}个")