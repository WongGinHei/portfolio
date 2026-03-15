#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重命名heavy-color中的子文件夹为英文
"""

import os
import shutil

# heavy-color子文件夹映射
SUBFOLDER_MAPPING = {
    '《午夜诗》系列作品': 'midnight-poems',
    '任朝暮系列作品': 'renzhao-series',
    '作品小稿': 'drafts',
    '其他作品': 'other-works',
    '写生作品': 'sketches',
    '抽象色彩作品': 'abstract-color',
    '系列组画《A One And A Two（一一）》': 'series-a-one-and-a-two',
}

def rename_heavy_color_subfolders():
    """重命名heavy-color中的子文件夹"""
    heavy_color_dir = 'work/heavy-color'
    
    if not os.path.exists(heavy_color_dir):
        print(f'错误: 找不到 {heavy_color_dir} 文件夹')
        return False
    
    print(f'处理文件夹: {heavy_color_dir}/')
    print('-' * 60)
    
    renamed = []
    for cn_name, en_name in SUBFOLDER_MAPPING.items():
        cn_path = os.path.join(heavy_color_dir, cn_name)
        en_path = os.path.join(heavy_color_dir, en_name)
        
        if os.path.exists(cn_path):
            if os.path.exists(en_path):
                shutil.rmtree(en_path)
            os.rename(cn_path, en_path)
            print(f'重命名: {cn_name} -> {en_name}')
            renamed.append((cn_name, en_name))
        else:
            print(f'跳过: {cn_name} (不存在)')
    
    print('-' * 60)
    print(f'共重命名 {len(renamed)} 个文件夹')
    return renamed

def update_html_paths(renamed_folders):
    """更新index.html中的路径引用"""
    html_file = 'index.html'
    
    if not os.path.exists(html_file):
        print(f'错误: 找不到 {html_file}')
        return False
    
    print(f'\n更新 {html_file} 中的路径...')
    print('-' * 60)
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 记录替换次数
    total_replacements = 0
    
    # 替换每个子文件夹名
    for cn_name, en_name in renamed_folders:
        # 替换 work/heavy-color/中文名/ 为 work/heavy-color/英文名/
        old_path = f'work/heavy-color/{cn_name}/'
        new_path = f'work/heavy-color/{en_name}/'
        
        count = content.count(old_path)
        if count > 0:
            content = content.replace(old_path, new_path)
            print(f'替换 {count} 处: heavy-color/{cn_name}/ -> heavy-color/{en_name}/')
            total_replacements += count
    
    # 保存文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('-' * 60)
    print(f'共替换 {total_replacements} 处路径')
    return True

def main():
    print('=' * 60)
    print('重命名heavy-color中的子文件夹')
    print('=' * 60)
    
    # 步骤1: 重命名文件夹
    renamed = rename_heavy_color_subfolders()
    if not renamed:
        print('没有需要重命名的文件夹')
        return
    
    # 步骤2: 更新HTML路径
    update_html_paths(renamed)
    
    print('\n' + '=' * 60)
    print('完成!')
    print('=' * 60)
    print('\nwork/heavy-color/ 的新结构:')
    heavy_color_dir = 'work/heavy-color'
    for item in sorted(os.listdir(heavy_color_dir)):
        full_path = os.path.join(heavy_color_dir, item)
        if os.path.isdir(full_path):
            print(f'  work/heavy-color/{item}/')

if __name__ == '__main__':
    main()
