from pathlib import Path

#1. 定义源文件和目标映射
source_dir = Path("messy_assets")

#定义品牌关键词和文件夹名称的对应关系
brand_map = {
    "arper" :"Brand_Arper",
    "walter_knoll":"Brand_Walter_Knoll"
}

print("--- 自动归档启动线 ---\n")

#2.遍历源文件夹
for file in source_dir.glob("*"):
    if file.is_file():
        filename_lower = file.name.lower()
        moved = False
        
        #3. 检查文件名称是否包含我们定义的品牌关键词
        for keyword,folder_name in brand_map.items():
            if keyword in filename_lower:
                # 定义目标文件夹路径
                target_dir = Path(folder_name)
                # 如果文件夹不存在则创建
                target_dir.mkdir(exist_ok=True)
                
                
                #定义文件新路径
                new_path = target_dir/file.name
                
                # 执行移动操作
                print(f"正在归档：{file.name} ->{folder_name}")
                file.rename(new_path)
                moved =True
                break
            
        if not moved:
            print(f"? 未识别品牌，跳过文件：{file.name}")
        
print("\n--- 归档任务完成！ ---")
