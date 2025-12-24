# -*- coding: utf-8 -*-
"""
检查EXE文件的依赖关系
使用dumpbin工具检查DLL依赖
"""

import subprocess
import os
import sys

def check_dependencies(exe_path):
    """检查EXE文件的DLL依赖"""
    
    print("=" * 60)
    print("检查EXE文件依赖关系")
    print("=" * 60)
    
    # 查找dumpbin工具
    dumpbin_path = r'D:\Code\VS2022\Community\VC\Tools\MSVC\14.29.30133\bin\HostX64\x64\dumpbin.exe'
    
    if not os.path.exists(dumpbin_path):
        print(f"[ERROR] dumpbin工具不存在: {dumpbin_path}")
        return
    
    print(f"[INFO] 使用dumpbin工具: {dumpbin_path}")
    
    # 运行dumpbin命令
    cmd = f'"{dumpbin_path}" /DEPENDENTS "{exe_path}"'
    print(f"\n[INFO] 执行命令: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("\n" + "=" * 60)
            print("依赖的DLL文件:")
            print("=" * 60)
            
            lines = result.stdout.split('\n')
            in_summary = False
            
            for line in lines:
                line = line.strip()
                if 'Summary' in line or '依赖项' in line or 'DLL Name' in line:
                    in_summary = True
                    continue
                
                if in_summary and line:
                    if '.dll' in line.lower():
                        print(f"  {line}")
        else:
            print(f"[ERROR] dumpbin执行失败: {result.stderr}")
    except Exception as e:
        print(f"[ERROR] 检查依赖失败: {e}")

if __name__ == '__main__':
    exe_path = r'E:\GitHub3\cpp\qt_conan_test\bin\QtWebViewApp.exe'
    check_dependencies(exe_path)
