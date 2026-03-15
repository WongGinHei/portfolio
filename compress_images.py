#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片压缩脚本 - 用于GitHub Pages部署
将图片压缩到适合网页展示的大小
"""

import os
import sys
from PIL import Image
from pathlib import Path
import shutil

def compress_image(input_path, output_path, max_size=1200, quality=85):
    """
    压缩单个图片
    :param input_path: 输入路径
    :param output_path: 输出路径
    :param max_size: 最大边长（像素）
    :param quality: JPEG质量（1-100）
    """
    try:
        with Image.open(input_path) as img:
            # 转换为RGB（处理RGBA等模式）
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # 计算新尺寸
            width, height = img.size
            if width > max_size or height > max_size:
                if width > height:
                    new_width = max_size
                    new_height = int(height * max_size / width)
                else:
                    new_height = max_size
                    new_width = int(width * max_size / height)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 保存
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 根据原格式选择保存格式
            ext = os.path.splitext(input_path)[1].lower()
            if ext in ['.png']:
                img.save(output_path, 'PNG', optimize=True)
            else:
                img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
            return True
    except Exception as e:
        print(f"  错误: {e}")
        return False

def main():
    input_folder = "视觉作品"
    output_folder = "视觉作品_compressed"
    
    if not os.path.exists(input_folder):
        print(f"错误: 找不到文件夹 '{input_folder}'")
        return
    
    # 创建输出文件夹
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    
    # 统计
    total_files = 0
    success_files = 0
    original_size = 0
    compressed_size = 0
    
    # 遍历所有图片
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, input_folder)
                output_path = os.path.join(output_folder, relative_path)
                
                # 确保输出目录存在
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                total_files += 1
                original_size += os.path.getsize(input_path)
                
                print(f"[{total_files}] 压缩: {relative_path}")
                
                if compress_image(input_path, output_path):
                    success_files += 1
                    compressed_size += os.path.getsize(output_path)
    
    # 输出统计
    print("\n" + "="*50)
    print("压缩完成!")
    print(f"总文件数: {total_files}")
    print(f"成功: {success_files}")
    print(f"原大小: {original_size/(1024*1024):.2f} MB")
    print(f"压缩后: {compressed_size/(1024*1024):.2f} MB")
    print(f"压缩率: {(1-compressed_size/original_size)*100:.1f}%")
    print("="*50)
    print(f"\n压缩后的文件夹: '{output_folder}'")
    print("请将 '视觉作品_compressed' 重命名为 '视觉作品' 后上传至GitHub")

if __name__ == "__main__":
    main()
