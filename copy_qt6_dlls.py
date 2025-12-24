#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
复制Qt6 DLL文件到bin目录
解决运行时找不到Qt6Core.dll等问题
"""

import os
import shutil
import glob

def copy_qt6_dlls():
    """复制Qt6核心DLL文件到bin目录"""
    # Qt6 DLL源目录
    qt6_bin_dir = r'C:\Users\happyli\.conan2\p\b\qtb73b254637aeb\p\bin'
    
    # 目标目录
    project_root = os.path.abspath('.')
    bin_dir = os.path.join(project_root, 'bin')
    
    # 确保bin目录存在
    os.makedirs(bin_dir, exist_ok=True)
    
    # 需要复制的Qt6核心DLL文件
    qt6_dlls = [
        'Qt6Core.dll',
        'Qt6Gui.dll', 
        'Qt6Widgets.dll',
        'Qt6Network.dll',
        'Qt6Sql.dll',
        'Qt6Xml.dll'
    ]
    
    print("🔧 开始复制Qt6 DLL文件到bin目录...")
    copied_count = 0
    
    for dll_name in qt6_dlls:
        source_path = os.path.join(qt6_bin_dir, dll_name)
        target_path = os.path.join(bin_dir, dll_name)
        
        if os.path.exists(source_path):
            try:
                shutil.copy2(source_path, target_path)
                print(f"✅ 复制成功: {dll_name}")
                copied_count += 1
            except Exception as e:
                print(f"❌ 复制失败 {dll_name}: {e}")
        else:
            print(f"⚠️  源文件不存在: {source_path}")
    
    # 复制所有Qt6相关的DLL文件（包含Qt6前缀的）
    print("\n📦 复制所有Qt6相关DLL文件...")
    qt6_pattern = os.path.join(qt6_bin_dir, 'Qt6*.dll')
    qt6_dll_files = glob.glob(qt6_pattern)
    
    for dll_path in qt6_dll_files:
        dll_name = os.path.basename(dll_path)
        target_path = os.path.join(bin_dir, dll_name)
        
        try:
            if not os.path.exists(target_path):
                shutil.copy2(dll_path, target_path)
                print(f"✅ 复制: {dll_name}")
                copied_count += 1
            else:
                print(f"ℹ️  已存在: {dll_name}")
        except Exception as e:
            print(f"❌ 复制失败 {dll_name}: {e}")
    
    print(f"\n🎉 完成！共复制了 {copied_count} 个Qt6 DLL文件")
    
    # 列出bin目录中的DLL文件
    print("\n📁 bin目录中的DLL文件:")
    bin_dlls = glob.glob(os.path.join(bin_dir, '*.dll'))
    for dll_path in bin_dlls:
        dll_name = os.path.basename(dll_path)
        print(f"  - {dll_name}")
    
    return True

if __name__ == "__main__":
    copy_qt6_dlls()