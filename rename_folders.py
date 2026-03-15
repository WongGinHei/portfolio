#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重命名work文件夹中的中文子文件夹为英文
"""

import os
import shutil

# 文件夹名映射（中文 -> 英文）
FOLDER_MAPPING = {
    '作品草稿': 'sketches',
    '其他作品': 'others',
    '摄影作品': 'photography',
    '水墨作品': 'ink-painting',
    '海报设计': 'posters',
    '重彩、色粉作品': 'heavy-color',
}

def rename_work_folders():
    """重命名work文件夹中的子文件夹"""
    work_dir = 'work'
    
    if not os.path.exists(work_dir):
        print(f'错误: 找不到 {work_dir} 文件夹')
        return False
    
    print(f'处理文件夹: {work_dir}/')
    print('-' * 50)
    
    renamed = []
    for cn_name, en_name in FOLDER_MAPPING.items():
        cn_path = os.path.join(work_dir, cn_name)
        en_path = os.path.join(work_dir, en_name)
        
        if os.path.exists(cn_path):
            if os.path.exists(en_path):
                shutil.rmtree(en_path)
            os.rename(cn_path, en_path)
            print(f'重命名: {cn_name} -> {en_name}')
            renamed.append((cn_name, en_name))
        else:
            print(f'跳过: {cn_name} (不存在)')
    
    print('-' * 50)
    print(f'共重命名 {len(renamed)} 个文件夹')
    return renamed

def update_html_paths(renamed_folders):
    """更新index.html中的路径引用"""
    html_file = 'index.html'
    
    if not os.path.exists(html_file):
        print(f'错误: 找不到 {html_file}')
        return False
    
    print(f'\n更新 {html_file} 中的路径...')
    print('-' * 50)
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 记录替换次数
    total_replacements = 0
    
    # 替换每个文件夹名
    for cn_name, en_name in renamed_folders:
        # 替换 work/中文名/ 为 work/英文名/
        old_path = f'work/{cn_name}/'
        new_path = f'work/{en_name}/'
        
        count = content.count(old_path)
        if count > 0:
            content = content.replace(old_path, new_path)
            print(f'替换 {count} 处: work/{cn_name}/ -> work/{en_name}/')
            total_replacements += count
    
    # 保存文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('-' * 50)
    print(f'共替换 {total_replacements} 处路径')
    return True

def main():
    print('=' * 60)
    print('重命名work文件夹中的中文子文件夹')
    print('=' * 60)
    
    # 步骤1: 重命名文件夹
    renamed = rename_work_folders()
    if not renamed:
        print('没有需要重命名的文件夹')
        return
    
    # 步骤2: 更新HTML路径
    update_html_paths(renamed)
    
    print('\n' + '=' * 60)
    print('完成!')
    print('=' * 60)
    print('\n新的文件结构:')
    work_dir = 'work'
    for item in sorted(os.listdir(work_dir)):
        full_path = os.path.join(work_dir, item)
        if os.path.isdir(full_path):
            print(f'  work/{item}/')

if __name__ == '__main__':
    main()
