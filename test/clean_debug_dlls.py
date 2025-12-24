# -*- coding: utf-8 -*-
"""
清理bin目录中的debug DLLs
只保留release版本的DLL
"""

import os
import glob

def clean_debug_dlls():
    """清理bin目录中的debug DLLs"""
    
    bin_path = r'E:\GitHub3\cpp\qt_conan_test\bin'
    
    print("=" * 60)
    print("清理bin目录中的debug DLLs")
    print("=" * 60)
    
    # 查找所有debug DLL（以d.dll结尾）
    debug_dlls = []
    for root, dirs, files in os.walk(bin_path):
        for file in files:
            if file.endswith('d.dll'):
                debug_dlls.append(os.path.join(root, file))
    
    print(f"\n找到 {len(debug_dlls)} 个debug DLL文件")
    
    # 删除debug DLLs
    deleted_count = 0
    for dll_path in debug_dlls:
        try:
            os.remove(dll_path)
            print(f"[OK] 删除: {os.path.basename(dll_path)}")
            deleted_count += 1
        except Exception as e:
            print(f"[ERROR] 删除失败 {os.path.basename(dll_path)}: {e}")
    
    # 检查并删除debug版本的exe
    debug_exes = glob.glob(os.path.join(bin_path, '*d.exe'))
    for exe_path in debug_exes:
        try:
            os.remove(exe_path)
            print(f"[OK] 删除: {os.path.basename(exe_path)}")
            deleted_count += 1
        except Exception as e:
            print(f"[ERROR] 删除失败 {os.path.basename(exe_path)}: {e}")
    
    print(f"\n总共删除了 {deleted_count} 个debug文件")
    print("=" * 60)

if __name__ == '__main__':
    clean_debug_dlls()
