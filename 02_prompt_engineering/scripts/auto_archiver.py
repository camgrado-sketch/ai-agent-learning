from pathlib import Path

# 1.定义源目录和目标映射
source_dir = Path("messy_assets")

# 定义品牌关键词与文件名称的对应关系
brand_map = {
    "arper" : "Brand_Arper",
    "walter_knoll":"Brand_Walter_Knoll"
}

print(f"--- 启动自动归档系统 ---、\n")

#2. 遍历源文件夹
for file in source_dir.glob("*"):
    if file.is_file():
        filename_lower = file.name.lower()   ## 所有图片的名称字符转化为小写字母
        moved = False
        
        # 3.检查文件名是否包含我们定义的品牌关键词
        for keyword,folder_name in brand_map.item():
            # 定义目标文件夹路径
            target_dir = Path(folder_name)
            