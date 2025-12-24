#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qt6编译错误诊断和修复工具
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header(title):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def check_qt_installation():
    """检查Qt6安装情况"""
    print_header("Qt6安装检查")
    
    # 常见Qt6安装路径
    qt_paths = [
        r"D:\Qt\6.5.0\msvc2019_64",
        r"D:\Qt\6.4.0\msvc2019_64", 
        r"C:\Qt\6.5.0\msvc2019_64",
        r"C:\Qt\6.4.0\msvc2019_64",
        r"D:\Qt\6.5.1\msvc2019_64",
        r"C:\Qt\6.5.1\msvc2019_64",
    ]
    
    found_qt = False
    for path in qt_paths:
        qt_path = Path(path)
        include_dir = qt_path / "include"
        lib_dir = qt_path / "lib"
        bin_dir = qt_path / "bin"
        
        if include_dir.exists() and lib_dir.exists() and bin_dir.exists():
            print(f"✓ 找到Qt6安装: {qt_path}")
            
            # 检查关键组件
            components = {
                "Qt6": include_dir / "Qt6",
                "Qt6Core": include_dir / "Qt6Core", 
                "Qt6Widgets": include_dir / "Qt6Widgets",
                "Qt6Gui": include_dir / "Qt6Gui",
                "Qt6WebEngineWidgets": include_dir / "Qt6WebEngineWidgets"
            }
            
            for comp_name, comp_path in components.items():
                if comp_path.exists():
                    print(f"  ✓ {comp_name}")
                else:
                    print(f"  ✗ {comp_name} 缺失")
            
            found_qt = True
            break
    
    if not found_qt:
        print("✗ 未找到Qt6安装")
        return False
    
    return True

def get_qt_installation_guide():
    """获取Qt6安装指导"""
    print_header("Qt6安装指导")
    
    guide = """
Qt6下载和安装步骤：

1. 下载Qt6
   - 访问: https://www.qt.io/download
   - 选择 "Qt Online Installer for Windows"
   - 或者直接下载: https://download.qt.io/online_installers/

2. 安装选项
   在Qt安装向导中选择：
   ✓ Qt 6.5.x (或更新版本)
   ✓ Qt WebEngine (必须选择！)
   ✓ MSVC 2019 64-bit (Windows)
   ✓ CMake Tools (推荐)
   ✓ Ninja (推荐)

3. 重要提示
   - Qt WebEngine是必需的，位置在"Qt > Additional Libraries"
   - 确保选择"WebEngine"相关组件
   - 建议安装路径: D:\\Qt\\6.5.x\\msvc2019_64

4. 环境变量设置 (可选)
   设置以下环境变量:
   QTDIR = D:\\Qt\\6.5.x\\msvc2019_64
   PATH = %QTDIR%\\bin;%PATH%
"""
    print(guide)

def fix_sconstruct_config():
    """修复SConstruct配置"""
    print_header("修复SConstruct配置")
    
    # 读取现有SConstruct
    try:
        with open("SConstruct", 'r', encoding='utf-8-sig') as f:
            content = f.read()
    except Exception as e:
        print(f"读取SConstruct失败: {e}")
        return False
    
    # 查找Qt6路径并替换
    qt_paths = [
        r"D:\Qt\6.5.0\msvc2019_64\include",
        r"D:\Qt\6.4.0\msvc2019_64\include", 
        r"C:\Qt\6.5.0\msvc2019_64\include",
        r"C:\Qt\6.4.0\msvc2019_64\include",
        r"D:\Qt\6.5.1\msvc2019_64\include",
        r"C:\Qt\6.5.1\msvc2019_64\include",
    ]
    
    # 更新include路径
    for path in qt_paths:
        if os.path.exists(path):
            include_path = path.replace('\\include', '')
            print(f"找到Qt6: {include_path}")
            
            # 更新SConstruct中的路径
            new_include_paths = [
                os.path.join(include_path, 'include'),
                os.path.join(include_path, 'include', 'Qt6'),
                os.path.join(include_path, 'include', 'Qt6Core'),
                os.path.join(include_path, 'include', 'Qt6Widgets'),
                os.path.join(include_path, 'include', 'Qt6Gui'),
                os.path.join(include_path, 'include', 'Qt6WebEngineWidgets'),
            ]
            
            new_lib_paths = [
                os.path.join(include_path, 'lib'),
            ]
            
            # 替换路径配置
            lines = content.split('\n')
            updated_lines = []
            
            for line in lines:
                if 'qt_include_paths = [' in line:
                    updated_lines.append(f"qt_include_paths = {new_include_paths}")
                    # 跳过后面的行
                    while updated_lines and not updated_lines[-1].strip().endswith(']'):
                        updated_lines.pop()
                    updated_lines.append('')
                elif 'qt_library_paths = [' in line:
                    updated_lines.append(f"qt_library_paths = {new_lib_paths}")
                    # 跳过后面的行  
                    while updated_lines and not updated_lines[-1].strip().endswith(']'):
                        updated_lines.pop()
                    updated_lines.append('')
                else:
                    updated_lines.append(line)
            
            # 写入修复后的文件
            try:
                with open("SConstruct", 'w', encoding='utf-8-sig') as f:
                    f.write('\n'.join(updated_lines))
                print("✓ SConstruct配置已修复")
                return True
            except Exception as e:
                print(f"写入SConstruct失败: {e}")
                return False
    
    print("✗ 未找到可用的Qt6路径")
    return False

def create_qt_env_setup():
    """创建Qt环境设置脚本"""
    print_header("创建Qt环境设置脚本")
    
    # 查找Qt6路径
    qt_base_paths = [
        r"D:\Qt\6.5.0\msvc2019_64",
        r"D:\Qt\6.4.0\msvc2019_64", 
        r"C:\Qt\6.5.0\msvc2019_64",
        r"C:\Qt\6.4.0\msvc2019_64",
        r"D:\Qt\6.5.1\msvc2019_64",
        r"C:\Qt\6.5.1\msvc2019_64",
    ]
    
    for base_path in qt_base_paths:
        if os.path.exists(base_path):
            qt_path = base_path
            break
    else:
        qt_path = "D:\\Qt\\6.5.0\\msvc2019_64"  # 默认路径
    
    # 创建批处理文件
    bat_content = f'''@echo off
REM Qt6环境设置脚本
echo 设置Qt6环境变量...

set QTDIR={qt_path}
set PATH=%QTDIR%\\bin;%PATH%
set QT_PLUGIN_PATH=%QTDIR%\\plugins

echo QTDIR=%QTDIR%
echo PATH=%PATH%
echo QT_PLUGIN_PATH=%QT_PLUGIN_PATH%

echo.
echo Qt6环境设置完成！
echo 现在可以尝试编译项目了。
echo.
pause
'''
    
    try:
        with open("setup_qt_env.bat", "w", encoding="utf-8-sig") as f:
            f.write(bat_content)
        print(f"✓ 创建了环境设置脚本: setup_qt_env.bat")
        print(f"  使用方法: 运行此脚本后再执行 scons")
        return True
    except Exception as e:
        print(f"✗ 创建环境脚本失败: {e}")
        return False

def create_alternative_build():
    """创建备选编译方案"""
    print_header("创建备选编译方案")
    
    # 创建简化的CMakeLists.txt
    cmake_content = f'''cmake_minimum_required(VERSION 3.16)
project(QtWebViewApp)

# 设置C++标准
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 启用UTF-8编码
add_compile_options(/utf-8)

# 查找Qt6 (自动检测)
find_package(Qt6 6.0 COMPONENTS Core Widgets Gui WebEngineWidgets QUIET)

if(NOT Qt6_FOUND)
    message(FATAL_ERROR "Qt6未找到! 请安装Qt6和WebEngine组件")
endif()

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
add_executable(QtWebViewApp {{SOURCES}} {{HEADERS}})

# 链接Qt6库
target_link_libraries(QtWebViewApp 
    Qt6::Core 
    Qt6::Widgets 
    Qt6::Gui 
    Qt6::WebEngineWidgets
)

# Windows特定设置
if(WIN32)
    target_compile_definitions(QtWebViewApp PRIVATE WIN32 _UNICODE UNICODE)
endif()

# 输出目录
set_target_properties(QtWebViewApp PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "bin"
)
'''
    
    try:
        with open("CMakeLists.txt", "w", encoding="utf-8-sig") as f:
            f.write(cmake_content)
        print("✓ 创建了CMakeLists.txt")
        
        # 创建编译指导
        guide = '''
使用CMake编译步骤：

1. 创建构建目录
   mkdir build
   cd build

2. 配置项目
   cmake .. -G "Visual Studio 16 2019" -A x64
   (或者使用Visual Studio 2019/2022的 CMake支持)

3. 编译项目
   cmake --build . --config Release

4. 运行程序
   ..\\bin\\QtWebViewApp.exe

注意: 如果Qt6未找到，请检查Qt6安装和CMake路径配置
'''
        print(guide)
        return True
    except Exception as e:
        print(f"✗ 创建CMake方案失败: {e}")
        return False

def main():
    """主函数"""
    print("Qt6编译错误诊断和修复工具")
    
    # 检查Qt6安装
    qt_found = check_qt_installation()
    
    if not qt_found:
        get_qt_installation_guide()
        return 1
    
    # 修复SConstruct配置
    sconstruct_fixed = fix_sconstruct_config()
    
    # 创建环境设置脚本
    env_script_created = create_qt_env_setup()
    
    # 创建备选编译方案
    cmake_created = create_alternative_build()
    
    print_header("修复完成")
    print("修复措施:")
    if sconstruct_fixed:
        print("✓ SConstruct配置已修复")
    if env_script_created:
        print("✓ 环境设置脚本已创建 (setup_qt_env.bat)")
    if cmake_created:
        print("✓ CMake编译方案已创建")
    
    print("\n推荐编译步骤:")
    print("1. 运行: setup_qt_env.bat")
    print("2. 运行: scons")
    print("或者使用CMake:")
    print("1. mkdir build && cd build")
    print("2. cmake .. -G \"Visual Studio 16 2019\" -A x64")
    print("3. cmake --build . --config Release")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())