#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理MOC文件的Python脚本
"""

import os
import shutil

def clean_moc_files():
    """清理现有的MOC文件"""
    obj_dir = os.path.join(os.getcwd(), 'obj')
    
    print(f"清理MOC文件，目录: {obj_dir}")
    
    if not os.path.exists(obj_dir):
        print("obj目录不存在")
        return
    
    # 查找所有.moc文件
    moc_files = []
    for file in os.listdir(obj_dir):
        if file.endswith('.moc'):
            moc_path = os.path.join(obj_dir, file)
            moc_files.append(moc_path)
    
    print(f"找到 {len(moc_files)} 个MOC文件:")
    for moc_file in moc_files:
        print(f"  - {moc_file}")
    
    # 删除所有MOC文件
    for moc_file in moc_files:
        try:
            os.remove(moc_file)
            print(f"已删除: {moc_file}")
        except Exception as e:
            print(f"删除失败 {moc_file}: {e}")
    
    print("MOC文件清理完成")

if __name__ == "__main__":
    clean_moc_files()