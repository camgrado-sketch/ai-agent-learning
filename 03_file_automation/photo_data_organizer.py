import os
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS

# 1.设置照片文件夹路径
photo_dir = Path("photos")


print("--- 正在打印照片原数据 ---\n")

# 2.遍历文件夹中的 jpg 图片
for photo_path in photo_dir.iterdir():
    if photo_path.suffix.lower() in [".jpg",".jpeg"]:
        
        try:
            # 先定义默认值
            date_folder = None
            
            
            # 3.打开图片
            with Image.open(photo_path) as img:
                #提取exif格式
                exif_data = img._getexif()
                
                
                if exif_data:
                    # 4.寻找拍摄时间标签（TAG ID 为 36867 或名称为 DateTimeOriginal）
                    photo_info ={}
                    for tag_id , value in exif_data.items():
                        tag_name = TAGS.get(tag_id,tag_id)
                        photo_info[tag_name]=value
                        
                    # 获取拍摄日期
                    capture_time = photo_info.get("DateTimeOriginal")
                    
                    if capture_time:
                        # capture_time 格式通常是“2026：04：15 10：30：00”
                        # 我们只取日期部分，并将冒号换成横杠
                        date_folder = capture_time.split()[0].replace(":","-")
                    else:
                        print(f"? 照片{photo_path.name}没有 EXIF 信息。")
                        
                        
                    #==================
                    #第二阶段：移动文件
                    #=================
                    
            if date_folder:
                print(f"照片：{photo_path.name} | 拍摄时间 {date_folder}")
                        
                target_dir = Path(date_folder)
                target_dir.mkdir(exist_ok=True)
                photo_path.rename(target_dir/photo_path.name) 
                    
                        # 5.自动化建议：你可以根据这个日期创建文件夹并移动他
                        # target_dir = Path(date_folder)
                        # target_dir.mkdir(exist_ok=True)
                        # photo_path.rename(target_dir / photo_path.name)
            else:
                print(f"? 照片{photo_path.name}没有记录拍摄时间。")
                
            
                            
        except Exception as e:
            print(f"处理{photo_path.name}时出错：{e}")
        
 

                        
print("\n--- 任务结束 ---")