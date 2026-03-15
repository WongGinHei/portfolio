#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建简化版网站 - 使用英文路径确保GitHub Pages兼容
"""

import os
import shutil

def create_simple_version():
    """创建简化版，每个分类只保留代表性作品"""
    
    dst = 'portfolio-simple'
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)
    
    # 复制主文件和照片
    if os.path.exists('deploy-github/index.html'):
        src_base = 'deploy-github'
    else:
        src_base = '.'
    
    # 读取原始HTML
    with open(os.path.join(src_base, 'index.html'), 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 创建简化版works结构
    works_dst = os.path.join(dst, 'works')
    os.makedirs(works_dst)
    
    # 定义要保留的代表性作品（源路径 -> 简化英文名）
    selected_works = [
        # 重彩作品
        ('视觉作品/重彩、色粉作品/系列组画《A One And A Two（一一）》/系列组画《A One And A Two（一一）》之（Ⅰ）《 The Ray Of Tomorrow（未来之念）》 2026 160x50x2 纸本重彩.jpg',
         'heavy-color/series-1.jpg'),
        ('视觉作品/重彩、色粉作品/《午夜诗》系列作品/《匆匆》2025 40x40 卡纸色粉.jpg',
         'heavy-color/midnight-poem-1.jpg'),
        ('视觉作品/重彩、色粉作品/任朝暮系列作品/《任朝暮》组画之（一）2025 85x40 纸本重彩.jpg',
         'heavy-color/renzhao-1.jpg'),
        
        # 水墨作品
        ('视觉作品/水墨作品/水墨人物创作-城市青年.jpg',
         'ink-painting/urban-youth.jpg'),
        ('视觉作品/水墨作品/水墨小品.jpg',
         'ink-painting/sketch.jpg'),
        ('视觉作品/水墨作品/水墨人像写生1.jpg',
         'ink-painting/portrait-1.jpg'),
        
        # 作品草稿
        ('视觉作品/作品草稿/工笔《汉韵》草稿.jpg',
         'sketches/hanyun-draft.jpg'),
        ('视觉作品/作品草稿/系列组画《春风》之Ⅰ草稿.jpg',
         'sketches/spring-1.jpg'),
        
        # 摄影作品
        ('视觉作品/摄影作品/骤雨黄昏.jpg',
         'photography/dusk.jpg'),
        ('视觉作品/摄影作品/和合.jpg',
         'photography/harmony.jpg'),
        
        # 海报设计
        ('视觉作品/海报设计/形色解析课程作业展海报.png',
         'posters/course-exhibition.png'),
        ('视觉作品/海报设计/拼贴海报-消费主义.jpg',
         'posters/collage.jpg'),
        
        # 其他作品
        ('视觉作品/其他作品/骤雨黄昏.jpg',
         'others/dusk.jpg'),
    ]
    
    # 复制选中的作品
    copied = []
    for src_rel, dst_rel in selected_works:
        src = os.path.join(src_base, src_rel)
        if os.path.exists(src):
            dst_file = os.path.join(dst, 'works', dst_rel)
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(src, dst_file)
            copied.append((src_rel, dst_rel))
    
    print(f"复制了 {len(copied)} 个代表性作品")
    
    # 修复HTML中的路径
    for src_rel, dst_rel in copied:
        old_path = src_rel.replace('视觉作品/', 'works/')
        new_path = 'works/' + dst_rel
        html = html.replace(old_path, new_path)
    
    # 复制照片
    photo_src = os.path.join(src_base, '王健希个人照片.jpg')
    if os.path.exists(photo_src):
        shutil.copy2(photo_src, dst)
    
    # 保存修复后的HTML
    with open(os.path.join(dst, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    
    # 创建zip
    shutil.make_archive('portfolio-simple', 'zip', dst)
    
    # 统计
    total = 0
    for dirpath, dirnames, filenames in os.walk(dst):
        for f in filenames:
            total += os.path.getsize(os.path.join(dirpath, f))
    
    print(f"\n简化版已创建: {dst}/")
    print(f"压缩包: portfolio-simple.zip")
    print(f"总大小: {total/(1024*1024):.2f} MB")
    print(f"\n文件结构:")
    for root, dirs, files in os.walk(os.path.join(dst, 'works')):
        level = root.replace(os.path.join(dst, 'works'), '').count(os.sep)
        indent = '  ' * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = '  ' * (level + 1)
        for file in files:
            print(f'{subindent}{file}')

if __name__ == '__main__':
    print("=" * 50)
    print("创建简化版网站")
    print("=" * 50)
    create_simple_version()
    print("\n" + "=" * 50)
    print("完成！")
    print("=" * 50)
