#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接编译脚本 - 解决VS2022环境问题
"""

import os
import subprocess
import sys
import time

def setup_environment_and_compile():
    """设置环境并编译"""
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 开始直接编译WebEngine")
    
    # 清理构建目录
    for directory in ['obj', 'bin']:
        if os.path.exists(directory):
            import shutil
            shutil.rmtree(directory)
        os.makedirs(directory, exist_ok=True)
    
    # 创建简单的编译脚本
    compile_script = '''@echo off
cd /d "E:\\GitHub3\\cpp\\qt_conan_test"
"D:\\Code\\VS2022\\Community\\VC\\Auxiliary\\Build\\vcvars64.bat" -vcvars_ver=14.29
echo VS2022 activated
echo Starting compilation...
set INCLUDE=-I"C:\\Users\\happyli\\.conan2\\p\\qt4048dd8d846aa\\s\\src\\qtwebengine\\src\\webenginewidgets\\api" -I"C:\\Users\\happyli\\.conan2\\p\\qt4048dd8d846aa\\s\\src\\qtwebengine\\src\\webenginewidgets"
cl /nologo /c /std:c++20 /utf-8 /W3 /EHsc %INCLUDE% src\\main.cpp /Foobj\\main.obj
if %errorlevel% neq 0 goto :error
cl /nologo /c /std:c++20 /utf-8 /W3 /EHsc %INCLUDE% src\\mainwindow.cpp /Foobj\\mainwindow.obj
if %errorlevel% neq 0 goto :error
cl /nologo /c /std:c++20 /utf-8 /W3 /EHsc %INCLUDE% src\\webviewwidget.cpp /Foobj\\webviewwidget.obj
if %errorlevel% neq 0 goto :error
link /nologo /subsystem:windows /entry:mainCRTStartup obj\\main.obj obj\\mainwindow.obj obj\\webviewwidget.obj /OUT:bin\\Qt6WebViewApp.exe
if %errorlevel% neq 0 goto :error
echo Compilation successful!
goto :end
:error
echo Compilation failed!
exit /b 1
:end
pause
'''
    
    # 写入脚本文件
    script_path = "compile_now.bat"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(compile_script)
    
    print(f"Created compile script: {script_path}")
    print("To compile manually, run:")
    print(f"  {script_path}")
    
    # 尝试自动执行（如果失败，手动执行）
    try:
        print("Attempting auto-compilation...")
        result = subprocess.run([script_path], 
                              capture_output=True, 
                              text=True, 
                              timeout=60)
        
        print("Compilation result:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        # 检查输出文件
        exe_path = "bin\\Qt6WebViewApp.exe"
        if os.path.exists(exe_path):
            size = os.path.getsize(exe_path)
            print(f"SUCCESS: Generated {exe_path} ({size} bytes)")
            return True
        else:
            print("No executable found. Please run the script manually.")
            return False
            
    except Exception as e:
        print(f"Auto-compilation failed: {e}")
        print("Please run the compile script manually.")
        return False
    finally:
        # 清理脚本文件
        try:
            os.remove(script_path)
        except:
            pass

if __name__ == "__main__":
    success = setup_environment_and_compile()
    sys.exit(0 if success else 1)