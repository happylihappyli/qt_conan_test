#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qt安装检测和配置工具
用于自动检测系统中的Qt安装并配置项目
"""

import os
import sys
import platform
from pathlib import Path

def detect_qt_installation():
    """检测系统中的Qt安装"""
    print("=" * 60)
    print("Qt安装检测工具")
    print("=" * 60)
    
    system = platform.system()
    if system != "Windows":
        print(f"当前仅支持Windows系统，检测到: {system}")
        return None
    
    # 可能的Qt安装路径
    possible_paths = [
        r"D:\Qt",
        r"C:\Qt",
        r"D:\Qt\6.5.0",
        r"C:\Qt\6.5.0",
        r"D:\Qt\6.2.0", 
        r"C:\Qt\6.2.0",
        r"D:\Qt\5.15.2",
        r"C:\Qt\5.15.2",
    ]
    
    found_qt = []
    
    for qt_path in possible_paths:
        if os.path.exists(qt_path):
            print(f"✓ 发现Qt目录: {qt_path}")
            
            # 查找版本目录
            versions = []
            for item in os.listdir(qt_path):
                if os.path.isdir(os.path.join(qt_path, item)):
                    # 检查是否是版本目录
                    if any(char.isdigit() for char in item) and 'msvc' in item:
                        versions.append(item)
                    elif item.replace('.', '').isdigit():  # 纯数字版本号
                        versions.append(item)
            
            if versions:
                print(f"  包含版本: {', '.join(versions)}")
                for version in versions:
                    version_path = os.path.join(qt_path, version)
                    include_dir = os.path.join(version_path, 'include')
                    lib_dir = os.path.join(version_path, 'lib')
                    bin_dir = os.path.join(version_path, 'bin')
                    
                    qt_config = {
                        'base_path': version_path,
                        'include_path': include_dir,
                        'lib_path': lib_dir,
                        'bin_path': bin_dir,
                        'version': version
                    }
                    
                    # 检查关键目录
                    checks = [
                        ('Qt6Core', include_dir, 'Qt6'),
                        ('QtWidgets', include_dir, 'QtWidgets'),
                        ('QtWebEngineWidgets', include_dir, 'QtWebEngineWidgets'),
                        ('Qt5Core', include_dir, 'Qt5Core')
                    ]
                    
                    available_modules = []
                    for module, inc_dir, prefix in checks:
                        module_path = os.path.join(inc_dir, prefix)
                        if os.path.exists(module_path):
                            available_modules.append(module)
                    
                    if available_modules:
                        qt_config['available_modules'] = available_modules
                        qt_config['type'] = 'Qt6' if 'Qt6Core' in available_modules else 'Qt5'
                        found_qt.append(qt_config)
                        print(f"    版本 {version}: {qt_config['type']}")
                        print(f"    可用模块: {', '.join(available_modules)}")
                        print(f"    头文件路径: {include_dir}")
                        print(f"    库文件路径: {lib_dir}")
                        print()
    
    if not found_qt:
        print("✗ 未找到Qt安装")
        print("\n请确保:")
        print("1. 已安装Qt6或Qt5")
        print("2. Qt安装路径在D:\\Qt或C:\\Qt目录下")
        print("3. 安装了Qt WebEngine模块（用于WebView功能）")
        return None
    
    # 选择最佳的Qt安装
    best_qt = None
    for qt in found_qt:
        if 'QtWebEngineWidgets' in qt.get('available_modules', []):
            best_qt = qt
            break
    
    if not best_qt and found_qt:
        best_qt = found_qt[0]  # 使用第一个找到的Qt安装
    
    return best_qt

def generate_qt_config(qt_config):
    """生成Qt配置信息"""
    if not qt_config:
        return
    
    print("=" * 60)
    print("最佳Qt配置:")
    print("=" * 60)
    print(f"Qt版本: {qt_config['version']}")
    print(f"Qt类型: {qt_config['type']}")
    print(f"基础路径: {qt_config['base_path']}")
    print(f"头文件目录: {qt_config['include_path']}")
    print(f"库文件目录: {qt_config['lib_path']}")
    print(f"可执行文件目录: {qt_config['bin_path']}")
    print(f"可用模块: {', '.join(qt_config['available_modules'])}")
    
    # 生成SConstruct配置代码
    config_code = f"""
# 自动检测到的Qt配置
qt_config = {{
    'include_path': r'{qt_config['include_path']}',
    'lib_path': r'{qt_config['lib_path']}',
    'bin_path': r'{qt_config['bin_path']}',
    'version': r'{qt_config['version']}',
    'type': r'{qt_config['type']}',
    'modules': {qt_config['available_modules']}
}}

# 添加Qt路径到环境
if os.path.exists(qt_config['include_path']):
    env.Append(CPPPATH=[qt_config['include_path']])

if os.path.exists(qt_config['lib_path']):
    env.Append(LIBPATH=[qt_config['lib_path']])

# 根据Qt版本选择库文件
if qt_config['type'] == 'Qt6':
    qt_libs = [
        'Qt6Core', 'Qt6Gui', 'Qt6Widgets', 'Qt6WebEngineWidgets',
        'Qt6WebEngineCore', 'Qt6Network', 'Qt6Sql',
        'kernel32', 'user32', 'gdi32', 'comdlg32', 'ole32', 'oleaut32', 
        'uuid', 'winmm', 'imm32', 'wininet', 'wsock32', 'ws2_32'
    ]
else:  # Qt5
    qt_libs = [
        'Qt5Core', 'Qt5Gui', 'Qt5Widgets', 'Qt5WebEngineWidgets',
        'Qt5WebEngineCore', 'Qt5Network', 'Qt5Sql',
        'kernel32', 'user32', 'gdi32', 'comdlg32', 'ole32', 'oleaut32', 
        'uuid', 'winmm', 'imm32', 'wininet', 'wsock32', 'ws2_32'
    ]
"""
    
    print("\nSConstruct配置代码:")
    print("-" * 40)
    print(config_code)
    
    # 保存配置到文件
    config_file = 'qt_config.py'
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_code)
    print(f"\n配置已保存到: {config_file}")
    
    return config_code

def main():
    """主函数"""
    print("开始检测Qt安装...")
    
    # 检测Qt安装
    qt_config = detect_qt_installation()
    
    if qt_config:
        # 生成配置
        generate_qt_config(qt_config)
        print("\n" + "=" * 60)
        print("✓ Qt配置完成！现在可以运行 scons 进行编译")
        print("=" * 60)
        return True
    else:
        print("\n" + "=" * 60)
        print("✗ 未找到合适的Qt安装")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)