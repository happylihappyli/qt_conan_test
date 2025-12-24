#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qt6 WebView项目编译脚本
提供简化编译方案和依赖检查
"""

import os
import sys
import subprocess
import time
import platform

def print_header(title):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def run_command(cmd, description, check=True):
    """运行命令并显示结果"""
    print(f"\n=== {description} ===")
    print(f"执行命令: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"返回码: {result.returncode}")
        if result.stdout:
            print(f"输出:\n{result.stdout}")
        if result.stderr:
            print(f"错误:\n{result.stderr}")
        if check and result.returncode != 0:
            print(f"命令执行失败，返回码: {result.returncode}")
        return result.returncode == 0
    except Exception as e:
        print(f"执行命令失败: {e}")
        return False

def check_qt_installation():
    """检查Qt6安装"""
    print_header("检查Qt6安装")
    
    # 检查常见Qt安装路径
    qt_paths = [
        r"D:\Qt\6.5.0\msvc2019_64\bin",
        r"C:\Qt\6.5.0\msvc2019_64\bin",
        r"D:\Qt\6.4.0\msvc2019_64\bin",
        r"C:\Qt\6.4.0\msvc2019_64\bin",
    ]
    
    qt_found = False
    for path in qt_paths:
        if os.path.exists(path):
            print(f"✓ 找到Qt安装: {path}")
            qt_found = True
            break
    
    if not qt_found:
        print("✗ 未找到Qt6安装")
        print("请从 https://www.qt.io/download 下载并安装Qt6")
        print("确保安装Qt WebEngine组件")
        return False
    
    return True

def check_build_tools():
    """检查构建工具"""
    print_header("检查构建工具")
    
    tools = {
        "python": "Python",
        "cl": "Visual Studio编译器",
        "qmake": "Qt qmake",
    }
    
    for cmd, name in tools.items():
        if run_command(f"where {cmd} || echo '{cmd} not found'", f"检查{name}", check_error=False):
            print(f"✓ {name}可用")
        else:
            print(f"✗ {name}不可用")

def try_scons_compile():
    """尝试使用scons编译"""
    print_header("尝试scons编译")
    
    # 首先检查SConstruct语法
    if not run_command("python -c \"import SConstruct\"", "检查SConstruct语法", check_error=False):
        print("SConstruct语法检查失败")
        return False
    
    print("开始scons编译...")
    return run_command("scons", "scons编译")

def create_simple_makefile():
    """创建简化的makefile用于测试编译"""
    print_header("创建简化编译脚本")
    
    # 创建一个简单的批处理文件
    bat_content = '''@echo off
REM Qt6 WebView项目编译批处理文件
echo 开始编译Qt6 WebView项目...
echo 时间: %date% %time%

REM 设置Qt环境变量 (需要根据实际Qt安装路径调整)
REM set QTDIR=D:\\Qt\\6.5.0\\msvc2019_64
REM set PATH=%QTDIR%\\bin;%PATH%

echo 检查Qt6...
qmake --version

echo 检查Visual Studio...
cl /?

echo 编译项目...
REM 这里需要根据实际的源文件和库路径调整
REM cl /EHsc /MD /Zi src\\main.cpp src\\mainwindow.cpp src\\webviewwidget.cpp ^
REM     /I"%QTDIR%\\include\\Qt6" /I"%QTDIR%\\include\\Qt6\\Core" ^
REM     /I"%QTDIR%\\include\\Qt6\\Widgets" /I"%QTDIR%\\include\\Qt6\\Gui" ^
REM     /I"%QTDIR%\\include\\Qt6\\WebEngineWidgets" ^
REM     /link /LIBPATH:"%QTDIR%\\lib" ^
REM     Qt6Core.lib Qt6Gui.lib Qt6Widgets.lib Qt6WebEngineWidgets.lib ^
REM     kernel32.lib user32.lib gdi32.lib ^
REM     /out:bin\\QtWebViewApp.exe

echo 编译完成
echo 时间: %date% %time%
pause
'''
    
    try:
        with open("build.bat", "w", encoding="utf-8-sig") as f:
            f.write(bat_content)
        print("✓ 创建了编译批处理文件: build.bat")
        return True
    except Exception as e:
        print(f"✗ 创建批处理文件失败: {e}")
        return False

def create_cmake_version():
    """创建CMakeLists.txt作为替代方案"""
    print_header("创建CMakeLists.txt")
    
    cmake_content = '''cmake_minimum_required(VERSION 3.16)
project(QtWebViewApp)

# 设置C++标准
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 启用UTF-8编码
if(CMAKE_CXX_COMPILER_ID MATCHES "MSVC")
    add_compile_options(/utf-8)
else()
    add_compile_options(-finput-charset=UTF-8 -fexec-charset=UTF-8)
endif()

# 查找Qt6
find_package(Qt6 6.0 REQUIRED COMPONENTS Core Widgets Gui WebEngineWidgets)

# 启用Qt自动MOC
set(CMAKE_AUTOMOC ON)

# 源文件
set(SOURCES
    src/main.cpp
    src/mainwindow.cpp
    src/webviewwidget.cpp
)

# 头文件
set(HEADERS
    src/mainwindow.h
    src/webviewwidget.h
)

# 创建可执行文件
add_executable(QtWebViewApp ${SOURCES} ${HEADERS})

# 链接Qt6库
target_link_libraries(QtWebViewApp 
    Qt6::Core 
    Qt6::Widgets 
    Qt6::Gui 
    Qt6::WebEngineWidgets
)

# 设置输出目录
set_target_properties(QtWebViewApp PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)

# Windows特定设置
if(WIN32)
    target_compile_definitions(QtWebViewApp PRIVATE WIN32 _UNICODE UNICODE)
endif()
'''
    
    try:
        with open("CMakeLists.txt", "w", encoding="utf-8-sig") as f:
            f.write(cmake_content)
        print("✓ 创建了CMakeLists.txt")
        print("可以使用以下命令编译:")
        print("  mkdir build && cd build")
        print("  cmake ..")
        print("  cmake --build .")
        return True
    except Exception as e:
        print(f"✗ 创建CMakeLists.txt失败: {e}")
        return False

def main():
    """主函数"""
    start_time = time.time()
    
    print(f"Qt6 WebView项目编译工具")
    print(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"操作系统: {platform.system()}")
    print(f"Python版本: {sys.version}")
    
    # 检查项目文件
    if not os.path.exists("SConstruct"):
        print("错误: 未找到SConstruct文件")
        return 1
    
    # 检查Qt6安装
    if not check_qt_installation():
        print("警告: Qt6安装检查失败，编译可能失败")
    
    # 检查构建工具
    check_build_tools()
    
    # 尝试scons编译
    scons_success = try_scons_compile()
    
    # 如果scons失败，创建替代方案
    if not scons_success:
        print("\nScons编译失败，创建替代编译方案...")
        create_simple_makefile()
        create_cmake_version()
    
    end_time = time.time()
    print_header("编译过程完成")
    print(f"总耗时: {end_time - start_time:.2f}秒")
    print(f"完成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if scons_success:
        print("✓ 编译成功!")
        print("可执行文件位置: bin/QtWebViewApp.exe")
    else:
        print("✗ 编译未成功完成")
        print("请检查:")
        print("1. Qt6是否正确安装")
        print("2. Visual Studio工具链是否可用")
        print("3. 环境变量是否配置正确")
    
    return 0 if scons_success else 1

if __name__ == "__main__":
    sys.exit(main())