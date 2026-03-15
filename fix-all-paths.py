#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整路径修复 - 将所有中文路径转为英文
"""

import os
import shutil
import re

def clean_filename(filename):
    """清理文件名，移除特殊字符"""
    # 移除书名号、替换空格为下划线
    cleaned = filename.replace('《', '').replace('》', '')
    cleaned = cleaned.replace(' ', '_').replace('（', '_').replace('）', '_')
    cleaned = cleaned.replace('/', '_').replace('\\', '_')
    # 移除多余的下划线
    cleaned = re.sub(r'_+', '_', cleaned)
    cleaned = cleaned.strip('_')
    return cleaned

def create_clean_structure():
    """创建清理后的文件结构"""
    
    src_base = 'deploy-github' if os.path.exists('deploy-github') else '.'
    dst_base = 'deploy-clean'
    
    if os.path.exists(dst_base):
        shutil.rmtree(dst_base)
    os.makedirs(dst_base)
    
    # 复制主文件
    shutil.copy2(os.path.join(src_base, 'index.html'), dst_base)
    shutil.copy2(os.path.join(src_base, '王健希个人照片.jpg'), dst_base)
    
    # 创建 works 目录
    works_src = os.path.join(src_base, 'works')
    works_dst = os.path.join(dst_base, 'works')
    os.makedirs(works_dst)
    
    # 路径映射
    path_map = {}  # 旧路径 -> 新路径
    
    # 遍历所有子文件夹
    for category in os.listdir(works_src):
        cat_src = os.path.join(works_src, category)
        if not os.path.isdir(cat_src):
            continue
        
        cat_dst = os.path.join(works_dst, category)
        os.makedirs(cat_dst, exist_ok=True)
        
        # 遍历该分类下的所有文件（包括子文件夹）
        for root, dirs, files in os.walk(cat_src):
            # 计算相对路径
            rel_root = os.path.relpath(root, cat_src)
            
            # 创建目标目录
            if rel_root != '.':
                dst_root = os.path.join(cat_dst, clean_filename(rel_root))
            else:
                dst_root = cat_dst
            os.makedirs(dst_root, exist_ok=True)
            
            # 复制并重命名文件
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(dst_root, clean_filename(file))
                    
                    # 确保目标文件名唯一
                    counter = 1
                    base_dst = dst_file
                    while os.path.exists(dst_file):
                        name, ext = os.path.splitext(base_dst)
                        dst_file = f"{name}_{counter}{ext}"
                        counter += 1
                    
                    shutil.copy2(src_file, dst_file)
                    
                    # 记录路径映射
                    old_rel = os.path.join('works', category, 
                        os.path.relpath(src_file, works_src)).replace('\\', '/')
                    new_rel = os.path.relpath(dst_file, dst_base).replace('\\', '/')
                    path_map[old_rel] = new_rel
                    
    return dst_base, path_map

def fix_html_references(path_map):
    """修复HTML中的引用"""
    
    html_path = 'deploy-clean/index.html'
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换所有路径
    for old_path, new_path in sorted(path_map.items(), key=lambda x: -len(x[0])):
        # 处理URL编码问题
        content = content.replace(old_path, new_path)
        # 同时处理可能的HTML实体编码
        old_encoded = old_path.replace('&', '&amp;')
        content = content.replace(old_encoded, new_path)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已修复HTML引用: {len(path_map)} 处")

def create_upload_package():
    """创建上传包（zip格式便于上传）"""
    
    src = 'deploy-clean'
    dst = 'portfolio-final'
    
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    
    # 创建zip
    shutil.make_archive('portfolio-final', 'zip', dst)
    
    print(f"\n上传包已创建: portfolio-final.zip")
    print(f"文件夹位置: {dst}/")
    
    # 统计
    total = 0
    for dirpath, dirnames, filenames in os.walk(dst):
        for f in filenames:
            total += os.path.getsize(os.path.join(dirpath, f))
    print(f"总大小: {total/(1024*1024):.2f} MB")

if __name__ == '__main__':
    print("=" * 60)
    print("GitHub Pages 完整路径修复工具")
    print("=" * 60)
    
    print("\n1. 创建清理后的文件结构...")
    dst_base, path_map = create_clean_structure()
    print(f"   整理了 {len(path_map)} 个文件")
    
    print("\n2. 修复HTML引用...")
    fix_html_references(path_map)
    
    print("\n3. 创建上传包...")
    create_upload_package()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    print("\n请上传 'portfolio-final' 文件夹到GitHub")
    print("或上传 'portfolio-final.zip' 并解压")
    print("\n新网址: https://wongginhei.github.io/portfolio/")
