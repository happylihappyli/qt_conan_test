#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终WebEngine编译脚本
"""

import os
import subprocess
import sys
import time
import shutil

def main():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 开始WebEngine编译")
    
    # 清理构建目录
    for dir_name in ['obj', 'bin']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.makedirs(dir_name, exist_ok=True)
    
    # VS2022环境设置
    vs2022_path = r"D:\Code\VS2022\Community"
    vcvars_path = os.path.join(vs2022_path, r"VC\Auxiliary\Build\vcvars64.bat")
    
    if not os.path.exists(vcvars_path):
        print(f"错误：未找到VCVARS脚本: {vcvars_path}")
        return False
    
    # 创建批处理文件设置环境
    bat_content = f'''@echo off
call "{vcvars_path}" -vcvars_ver=14.29
echo VS2022环境已设置
echo 编译开始...

set WEBENGINE_INCLUDE=-I"C:\\Users\\happyli\\.conan2\\p\\qt4048dd8d846aa\\s\\src\\qtwebengine\\src\\webenginewidgets\\api" -I"C:\\Users\\happyli\\.conan2\\p\\qt4048dd8d846aa\\s\\src\\qtwebengine\\src\\webenginewidgets"

echo 编译main.cpp...
cl /nologo /c /std:c++20 /utf-8 /W3 /EHsc %WEBENGINE_INCLUDE% src\\main.cpp /Foobj\\main.obj

echo 编译mainwindow.cpp...
cl /nologo /c /std:c++20 /utf-8 /W3 /EHsc %WEBENGINE_INCLUDE% src\\mainwindow.cpp /Foobj\\mainwindow.obj

echo 编译webviewwidget.cpp...
cl /nologo /c /std:c++20 /utf-8 /W3 /EHsc %WEBENGINE_INCLUDE% src\\webviewwidget.cpp /Foobj\\webviewwidget.obj

echo 链接程序...
link /nologo /subsystem:windows /entry:mainCRTStartup obj\\main.obj obj\\mainwindow.obj obj\\webviewwidget.obj /OUT:bin\\Qt6WebViewApp.exe

echo 编译完成！
echo 可执行文件: bin\\Qt6WebViewApp.exe
'''
    
    bat_file = "compile_webengine.bat"
    with open(bat_file, 'w', encoding='gbk') as f:
        f.write(bat_content)
    
    try:
        # 运行批处理文件
        result = subprocess.run(bat_file, shell=True, capture_output=True, text=True, timeout=120)
        
        print("编译输出:")
        print(result.stdout)
        
        if result.stderr:
            print("错误信息:")
            print(result.stderr)
        
        # 检查是否生成了可执行文件
        exe_path = "bin\\Qt6WebViewApp.exe"
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path)
            print(f"✅ 编译成功！")
            print(f"可执行文件: {exe_path} (大小: {file_size} 字节)")
            return True
        else:
            print("❌ 编译失败：未生成可执行文件")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 编译超时")
        return False
    except Exception as e:
        print(f"❌ 编译异常: {e}")
        return False
    finally:
        # 清理临时文件
        try:
            os.remove(bat_file)
        except:
            pass

if __name__ == "__main__":
    success = main()
    if success:
        print("🎉 WebEngine编译任务完成！")
    else:
        print("💥 WebEngine编译任务失败！")
    sys.exit(0 if success else 1)