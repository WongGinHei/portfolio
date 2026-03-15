#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
压缩 work 文件夹中超过 25MB 的图片文件
"""

import os
from PIL import Image
import shutil

# 25MB 阈值（字节）
SIZE_THRESHOLD = 25 * 1024 * 1024

def get_file_size_mb(filepath):
    """获取文件大小（MB）"""
    return os.path.getsize(filepath) / (1024 * 1024)

def find_large_files(folder):
    """查找超过阈值的文件"""
    large_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                filepath = os.path.join(root, file)
                size = os.path.getsize(filepath)
                if size > SIZE_THRESHOLD:
                    large_files.append({
                        'path': filepath,
                        'size_mb': size / (1024 * 1024)
                    })
    return large_files

def compress_image(input_path, target_size_mb=20):
    """压缩图片"""
    try:
        original_size = get_file_size_mb(input_path)
        print(f"  Original: {original_size:.2f} MB")
        
        with Image.open(input_path) as img:
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            width, height = img.size
            print(f"  Original size: {width}x{height}")
            
            # 根据原文件大小决定目标尺寸
            if original_size > 50:
                max_dimension = 1333
            elif original_size > 35:
                max_dimension = 2000
            else:
                max_dimension = 2500
            
            # 调整尺寸
            if width > max_dimension or height > max_dimension:
                if width > height:
                    new_width = max_dimension
                    new_height = int(height * max_dimension / width)
                else:
                    new_height = max_dimension
                    new_width = int(width * max_dimension / height)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                print(f"  New size: {new_width}x{new_height}")
            
            # 保存为JPEG（通常比PNG小很多）
            temp_path = input_path + '.temp.jpg'
            
            # 尝试不同质量
            for quality in [90, 80, 70, 60]:
                img.save(temp_path, 'JPEG', quality=quality, optimize=True)
                new_size = get_file_size_mb(temp_path)
                print(f"  Quality {quality}%: {new_size:.2f} MB")
                
                if new_size <= target_size_mb:
                    # 替换原文件
                    if input_path.endswith('.png'):
                        # 如果是PNG，保留原文件名但改为.jpg
                        new_path = input_path.replace('.png', '.jpg')
                        shutil.move(temp_path, new_path)
                        print(f"  Saved as: {new_path}")
                    else:
                        shutil.move(temp_path, input_path)
                    return True
            
            # 如果还是太大，进一步降低尺寸
            print("  Reducing size further...")
            img_small = img.resize((1000, 1500), Image.Resampling.LANCZOS)
            img_small.save(temp_path, 'JPEG', quality=70, optimize=True)
            new_size = get_file_size_mb(temp_path)
            print(f"  Final: {new_size:.2f} MB")
            
            if new_size <= target_size_mb:
                if input_path.endswith('.png'):
                    new_path = input_path.replace('.png', '.jpg')
                    shutil.move(temp_path, new_path)
                else:
                    shutil.move(temp_path, input_path)
                return True
            
            # 清理
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return False
            
    except Exception as e:
        print(f"  Error: {e}")
        if os.path.exists(input_path + '.temp.jpg'):
            os.remove(input_path + '.temp.jpg')
        return False

def main():
    work_dir = 'work'
    
    if not os.path.exists(work_dir):
        print(f"Error: Cannot find {work_dir} folder")
        return
    
    print("=" * 60)
    print("Finding images over 25MB...")
    print("=" * 60)
    
    large_files = find_large_files(work_dir)
    
    if not large_files:
        print("\nNo files over 25MB found")
        return
    
    print(f"\nFound {len(large_files)} large files:")
    print("-" * 60)
    for i, file_info in enumerate(large_files, 1):
        print(f"{i}. {file_info['path']}")
        print(f"   Size: {file_info['size_mb']:.2f} MB")
    print("-" * 60)
    
    print("\nStarting compression...")
    print("=" * 60)
    
    success_count = 0
    for file_info in large_files:
        print(f"\nProcessing: {file_info['path']}")
        if compress_image(file_info['path']):
            success_count += 1
            print("  [SUCCESS]")
        else:
            print("  [FAILED]")
    
    print("\n" + "=" * 60)
    print(f"Done! Compressed {success_count}/{len(large_files)} files")
    print("=" * 60)

if __name__ == '__main__':
    main()
