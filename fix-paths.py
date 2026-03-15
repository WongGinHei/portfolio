#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复图片路径脚本 - 将中文路径改为英文，避免GitHub Pages兼容问题
"""

import os
import re
import shutil

def rename_folders_to_english():
    """将中文文件夹名改为英文"""
    
    # 检查是否在deploy-github目录
    if os.path.exists('deploy-github'):
        base_dir = 'deploy-github'
    else:
        base_dir = '.'
    
    # 映射关系
    folder_mapping = {
        '视觉作品': 'works',
        '作品草稿': 'sketches',
        '摄影作品': 'photography',
        '水墨作品': 'ink-painting',
        '海报设计': 'posters',
        '重彩、色粉作品': 'heavy-color',
        '其他作品': 'others',
    }
    
    works_path = os.path.join(base_dir, '视觉作品')
    if not os.path.exists(works_path):
        print("错误: 找不到 '视觉作品' 文件夹")
        return False
    
    # 重命名一级文件夹
    for cn, en in folder_mapping.items():
        src = os.path.join(base_dir, cn)
        dst = os.path.join(base_dir, en)
        if os.path.exists(src) and not os.path.exists(dst):
            os.rename(src, dst)
            print(f"重命名: {cn} -> {en}")
    
    return True

def fix_html_paths():
    """修复HTML中的路径"""
    
    if os.path.exists('deploy-github/index.html'):
        html_path = 'deploy-github/index.html'
    else:
        html_path = 'index.html'
    
    # 读取文件
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 路径映射
    path_mapping = {
        '视觉作品': 'works',
        '作品草稿': 'sketches',
        '摄影作品': 'photography',
        '水墨作品': 'ink-painting',
        '海报设计': 'posters',
        '重彩、色粉作品': 'heavy-color',
        '其他作品': 'others',
    }
    
    # 替换路径
    for cn, en in path_mapping.items():
        content = content.replace(cn + '/', en + '/')
    
    # 保存
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已修复HTML路径: {html_path}")
    return True

def create_simple_test():
    """创建一个简化版测试文件"""
    
    test_html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>王健希 | 测试页面</title>
    <style>
        body { font-family: sans-serif; padding: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; }
        h1 { color: #333; }
        .image-test { margin: 20px 0; }
        .image-test img { max-width: 100%; height: auto; border: 2px solid #ddd; }
        .success { color: green; }
        .error { color: red; }
    </style>
</head>
<body>
    <div class="container">
        <h1>图片路径测试</h1>
        <p>如果以下图片能显示，说明路径正确。</p>
        
        <div class="image-test">
            <h3>测试1: 个人照片</h3>
            <img src="王健希个人照片.jpg" alt="个人照片" onerror="this.parentElement.innerHTML+='<p class=\\'error\\'>✗ 加载失败</p>'" onload="this.parentElement.innerHTML+='<p class=\\'success\\'>✓ 加载成功</p>'">
        </div>
        
        <div class="image-test">
            <h3>测试2: 水墨作品</h3>
            <img src="works/ink-painting/水墨小品.jpg" alt="水墨小品" onerror="this.parentElement.innerHTML+='<p class=\\'error\\'>✗ 加载失败</p>'" onload="this.parentElement.innerHTML+='<p class=\\'success\\'>✓ 加载成功</p>'">
        </div>
        
        <div class="image-test">
            <h3>测试3: 重彩作品</h3>
            <img src="works/heavy-color/《午夜诗》系列作品/《匆匆》2025 40x40 卡纸色粉.jpg" alt="匆匆" onerror="this.parentElement.innerHTML+='<p class=\\'error\\'>✗ 加载失败</p>'" onload="this.parentElement.innerHTML+='<p class=\\'success\\'>✓ 加载成功</p>'">
        </div>
        
        <hr>
        <p><a href="index.html">返回主页面</a></p>
    </div>
</body>
</html>'''
    
    # 根据位置保存
    if os.path.exists('deploy-github'):
        test_path = 'deploy-github/test.html'
    else:
        test_path = 'test.html'
    
    with open(test_path, 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print(f"已创建测试页面: {test_path}")

if __name__ == '__main__':
    print("=" * 50)
    print("GitHub Pages 图片路径修复工具")
    print("=" * 50)
    
    # 方案1: 重命名文件夹
    print("\n【方案1】将中文文件夹名改为英文...")
    if rename_folders_to_english():
        fix_html_paths()
    
    # 创建测试页面
    print("\n【方案2】创建测试页面...")
    create_simple_test()
    
    print("\n" + "=" * 50)
    print("修复完成！")
    print("=" * 50)
    print("\n请重新上传 'deploy-github' 文件夹到GitHub")
    print("然后访问: https://你的用户名.github.io/portfolio/test.html")
    print("\n如果测试页面图片能显示，说明路径已修复。")
