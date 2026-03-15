#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
压缩 work 文件夹中超过 25MB 的图片文件
"""

import os
from PIL import Image
import shutil

# 25MB 阈值（字节）
SIZE_THRESHOLD = 25 * 1024 * 1024  # 25MB

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
    """
    压缩图片到目标大小以下
    策略：先降低尺寸，再降低质量
    """
    try:
        original_size = get_file_size_mb(input_path)
        print(f"  原大小: {original_size:.2f} MB")
        
        with Image.open(input_path) as img:
            # 转换为 RGB
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            width, height = img.size
            print(f"  原尺寸: {width}x{height}")
            
            # 计算需要的压缩比例
            # 假设文件大小与像素数成正比，与质量成正比
            current_pixels = width * height
            target_ratio = (target_size_mb / original_size) ** 0.5
            
            # 如果文件很大，先降低尺寸
            if original_size > 50:  # 超过50MB，大幅降尺寸
                max_dimension = 2000
            elif original_size > 35:  # 超过35MB，中等降尺寸
                max_dimension = 2500
            else:  # 25-35MB，小幅降尺寸
                max_dimension = 3000
            
            # 调整尺寸
            if width > max_dimension or height > max_dimension:
                if width > height:
                    new_width = max_dimension
                    new_height = int(height * max_dimension / width)
                else:
                    new_height = max_dimension
                    new_width = int(width * max_dimension / height)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                print(f"  调整后尺寸: {new_width}x{new_height}")
            
            # 保存，逐步降低质量直到满足大小要求
            quality = 90
            ext = os.path.splitext(input_path)[1].lower()
            
            # 创建临时文件
            temp_path = input_path + '.temp'
            
            while quality >= 60:  # 最低质量60%
                if ext == '.png':
                    img.save(temp_path, 'PNG', optimize=True)
                else:
                    img.save(temp_path, 'JPEG', quality=quality, optimize=True)
                
                new_size = get_file_size_mb(temp_path)
                print(f"  尝试质量 {quality}%: {new_size:.2f} MB", end='')
                
                if new_size <= target_size_mb:
                    print(" ✓")
                    # 替换原文件
                    shutil.move(temp_path, input_path)
                    return True
                else:
                    print(" ✗")
                    quality -= 10
            
            # 如果质量降到60%还是太大，继续降低尺寸
            if quality < 60:
                print("  质量已降到最低，继续降低尺寸...")
                # 再次降低尺寸到1500
                if width > 1500 or height > 1500:
                    if width > height:
                        new_width = 1500
                        new_height = int(height * 1500 / width)
                    else:
                        new_height = 1500
                        new_width = int(width * 1500 / height)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    print(f"  最终尺寸: {new_width}x{new_height}")
                
                # 用质量60保存
                if ext == '.png':
                    img.save(temp_path, 'PNG', optimize=True)
                else:
                    img.save(temp_path, 'JPEG', quality=60, optimize=True)
                
                new_size = get_file_size_mb(temp_path)
                print(f"  最终大小: {new_size:.2f} MB")
                
                if new_size <= target_size_mb:
                    shutil.move(temp_path, input_path)
                    return True
                else:
                    # 最后手段：降到1200
                    if width > 1200 or height > 1200:
                        if width > height:
                            new_width = 1200
                            new_height = int(height * 1200 / width)
                        else:
                            new_height = 1200
                            new_width = int(width * 1200 / height)
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        
                        if ext == '.png':
                            img.save(temp_path, 'PNG', optimize=True)
                        else:
                            img.save(temp_path, 'JPEG', quality=60, optimize=True)
                        
                        new_size = get_file_size_mb(temp_path)
                        print(f"  最终大小: {new_size:.2f} MB")
                        shutil.move(temp_path, input_path)
                        return True
            
            # 清理临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return False
            
    except Exception as e:
        print(f"  错误: {e}")
        # 清理临时文件
        if os.path.exists(input_path + '.temp'):
            os.remove(input_path + '.temp')
        return False

def main():
    work_dir = 'work'
    
    if not os.path.exists(work_dir):
        print(f"错误: 找不到 {work_dir} 文件夹")
        return
    
    print("=" * 60)
    print("查找超过 25MB 的图片文件...")
    print("=" * 60)
    
    large_files = find_large_files(work_dir)
    
    if not large_files:
        print("\n没有找到超过 25MB 的文件")
        return
    
    print(f"\n找到 {len(large_files)} 个大文件:")
    print("-" * 60)
    for i, file_info in enumerate(large_files, 1):
        print(f"{i}. {file_info['path']}")
        print(f"   大小: {file_info['size_mb']:.2f} MB")
    print("-" * 60)
    
    print("\n开始压缩...")
    print("=" * 60)
    
    success_count = 0
    for file_info in large_files:
        print(f"\n处理: {file_info['path']}")
        if compress_image(file_info['path']):
            new_size = get_file_size_mb(file_info['path'])
            print(f"  成功! 新大小: {new_size:.2f} MB")
            success_count += 1
        else:
            print(f"  失败!")
    
    print("\n" + "=" * 60)
    print(f"完成! 成功压缩 {success_count}/{len(large_files)} 个文件")
    print("=" * 60)

if __name__ == '__main__':
    main()
