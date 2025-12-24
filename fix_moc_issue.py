#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复Qt6 MOC文件问题
清理损坏的MOC文件并重新生成
"""

import os
import shutil
import subprocess
import time

def fix_moc_files():
    """修复MOC文件问题"""
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 开始修复Qt6 MOC文件问题")
    
    # 项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(project_root, 'src')
    obj_dir = os.path.join(project_root, 'obj')
    
    print(f"[INFO] 项目根目录: {project_root}")
    print(f"[INFO] 源代码目录: {src_dir}")
    print(f"[INFO] 目标文件目录: {obj_dir}")
    
    # 清理损坏的MOC文件
    moc_files = ['mainwindow.moc', 'webviewwidget.moc']
    for moc_file in moc_files:
        moc_path = os.path.join(obj_dir, moc_file)
        if os.path.exists(moc_path):
            try:
                os.remove(moc_path)
                print(f"[OK] 已删除损坏的MOC文件: {moc_path}")
            except Exception as e:
                print(f"[ERROR] 删除MOC文件失败 {moc_path}: {e}")
    
    # 查找MOC可执行文件
    moc_paths = [
        r'C:\Users\happyli\.conan2\p\b\qtb73b254637aeb\p\bin\moc.exe',
        r'D:\Qt\6.5.0\msvc2019_64\bin\moc.exe',
        r'D:\Qt\6.7.3\msvc2019_64\bin\moc.exe',
        r'C:\Qt\6.5.0\msvc2019_64\bin\moc.exe',
        r'C:\Qt\6.7.3\msvc2019_64\bin\moc.exe'
    ]
    
    moc_path = None
    for path in moc_paths:
        if os.path.exists(path):
            moc_path = path
            print(f"[OK] 找到MOC可执行文件: {moc_path}")
            break
    
    if not moc_path:
        print("[ERROR] 未找到MOC可执行文件")
        return False
    
    # 重新生成MOC文件
    headers = [
        ('src/mainwindow.h', 'mainwindow.moc'),
        ('src/webviewwidget.h', 'webviewwidget.moc')
    ]
    
    new_moc_files = []
    for header_file, moc_file in headers:
        header_path = os.path.join(project_root, header_file)
        moc_path_target = os.path.join(obj_dir, moc_file)
        
        if os.path.exists(header_path):
            try:
                # 使用Conan环境的MOC
                cmd = [moc_path, '-o', moc_path_target, header_path]
                print(f"[INFO] 生成MOC: {cmd}")
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0 and os.path.exists(moc_path_target):
                    new_moc_files.append(moc_path_target)
                    print(f"[OK] 成功生成 {moc_file}")
                else:
                    print(f"[ERROR] 生成 {moc_file} 失败")
                    print(f"错误输出: {result.stderr}")
            except Exception as e:
                print(f"[ERROR] 生成 {moc_file} 时出错: {e}")
        else:
            print(f"[ERROR] 头文件不存在: {header_path}")
    
    # 验证生成的MOC文件
    print(f"\n[INFO] 验证生成的MOC文件:")
    for moc_file in new_moc_files:
        if os.path.exists(moc_file):
            file_size = os.path.getsize(moc_file)
            print(f"[OK] {moc_file} 存在，大小: {file_size} 字节")
        else:
            print(f"[ERROR] {moc_file} 不存在")
    
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] MOC文件修复完成")
    return len(new_moc_files) > 0

if __name__ == "__main__":
    success = fix_moc_files()
    if success:
        print("\n✅ MOC文件修复成功！现在可以重新编译了")
    else:
        print("\n❌ MOC文件修复失败")