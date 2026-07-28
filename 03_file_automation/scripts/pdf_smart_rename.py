import os
from pathlib import Path
from PyPDF2 import PdfReader

#1. 设置目标文件
pdf_path = Path("unknown_catalog.pdf")

if not pdf_path.exists():
    print(f"错误：找不到文件{pdf_path.absolute()}，请先准备一个测试 PDF 。")
else:
    print(f"正在读取 PDF 内容：{pdf_path.name}...")
    
    try:
        #2. 读取PDF
        reader = PdfReader(pdf_path)
        # 获取第一页
        first_page = reader.pages[0]
        # 提取文本（转为小写方便匹配）
        content = first_page.extract_text().lower()
        
        #3.匹配品牌关键词
        new_name = ""
        if "arper" in content:
            new_name = "Arper_Official_Catalog.pdf"
        elif "walter knoll" in content or "walterknoll" in content:
            new_name = "Walter_Knoll_Catalog.pdf"
            
        # 4.执行重命名
        if new_name:
            # 构造新路径（在同一文件夹下）
            new_path = pdf_path.with_name(new_name)
            
            # 注意：在重命名前确保文件对象已释放（PyPDF2 读取完会自动释放，但最好确认）
            pdf_path.rename(new_path)
            print(f"识别成功！已重命名为{new_name}")
        else:
            print("? 未在 PDF 第一页找到已知品牌关键词。")
            
    except Exception as e:
        print(f"读取出错：{e}")
        
    print("--- 任务结束 ---")