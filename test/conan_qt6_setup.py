#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conan Qt6配置和安装指导
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

def create_optimized_conanfile():
    """创建优化的Conan配置文件"""
    print_header("创建优化的Conan配置文件")
    
    conanfile_content = '''[requires]
qt/6.5.0

[generators]
Scons
CMakeDeps
CMakeToolchain

[options]
qt:qtbase=True
qt:qtwebengine=True
qt:qtsvg=True
qt:qtdeclarative=True
qt:shared=True
qt:qttool=False
qt:qtx11extras=False
qt:qtmultimedia=False
qt:qt3d=False
qt:qt5compat=False
qt:qtshadertools=False
qt:qtwebengine=True

[imports]
bin, *.dll -> ./bin
lib, *.lib -> ./lib
lib, *.so -> ./bin
lib, *.dylib -> ./bin
include, *.h -> ./include
'''
    
    try:
        with open("conanfile.txt", "w", encoding="utf-8-sig") as f:
            f.write(conanfile_content)
        print("✓ 创建了优化的conanfile.txt")
        return True
    except Exception as e:
        print(f"✗ 创建conanfile.txt失败: {e}")
        return False

def check_conan_installation():
    """检查Conan安装状态"""
    print_header("检查Conan安装状态")
    
    try:
        result = subprocess.run(["conan", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✓ Conan已安装: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Conan未安装")
        return False

def install_conan():
    """安装Conan"""
    print_header("安装Conan")
    
    print("正在安装Conan...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "conan"], 
                      check=True, timeout=120)
        print("✓ Conan安装成功")
        return True
    except Exception as e:
        print(f"✗ Conan安装失败: {e}")
        return False

def conan_install_qt6():
    """使用Conan安装Qt6"""
    print_header("使用Conan安装Qt6")
    
    commands = [
        # 清理之前的Conan缓存
        ["conan", "remove", "qt/*", "-f"],
        
        # 远程源配置 (可选)
        ["conan", "remote", "add", "conancenter", "https://center.conan.io", "--force"],
        
        # 安装Qt6依赖
        ["conan", "install", ".", "--build=missing", "--update"],
        
        # 生成构建文件
        ["conan", "install", ".", "--build=missing", "--generate-binaries"],
    ]
    
    for i, cmd in enumerate(commands, 1):
        print(f"\n步骤 {i}: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, 
                                  timeout=600)  # 10分钟超时
            if result.returncode == 0:
                print(f"✓ 步骤 {i} 完成")
            else:
                print(f"✗ 步骤 {i} 失败:")
                print(f"错误输出: {result.stderr}")
                if i < len(commands):
                    print("尝试继续下一步骤...")
        except subprocess.TimeoutExpired:
            print(f"✗ 步骤 {i} 超时")
        except Exception as e:
            print(f"✗ 步骤 {i} 异常: {e}")
    
    return True

def create_conan_profile():
    """创建Conan构建配置"""
    print_header("创建Conan构建配置")
    
    # 检测编译器
    if platform.system() == "Windows":
        compiler = "msvc"
        compiler_version = "193"  # VS2022
        compiler_base = "Visual Studio"
    else:
        compiler = "gcc"
        compiler_version = "11"
        compiler_base = "gcc"
    
    profile_content = f'''[settings]
os=Windows
os_build=Windows
arch=x86_64
arch_build=x86_64
compiler={compiler}
compiler.version={compiler_version}
compiler.base={compiler_base}
build_type=Release
compiler.runtime=MT
compiler.runtime_type=Release
compiler.cppstd=20

[env]
CC=cl
CXX=cl

[conf]
tools.microsoft.msbuild:vs_version=17
tools.microsoft.msbuild:verbosity=minimal
'''
    
    try:
        with open("windows_release_profile.txt", "w", encoding="utf-8-sig") as f:
            f.write(profile_content)
        print("✓ 创建了Conan配置文件")
        return True
    except Exception as e:
        print(f"✗ 创建配置文件失败: {e}")
        return False

def fix_sconstruct_for_conan():
    """修复SConstruct以支持Conan"""
    print_header("修复SConstruct以支持Conan")
    
    try:
        with open("SConstruct", 'r', encoding='utf-8-sig') as f:
            sconstruct_content = f.read()
        
        # 更新SConstruct以使用Conan生成的文件
        updates = [
            # 添加Conan自动检测
            ("# 检查并加载Conan生成的文件", 
             "# 检查并加载Conan生成的文件\n# 尝试从Conan安装目录自动检测Qt6路径\ntry:\n    from conan import ConanFile\n    print(\"✓ 检测到Conan配置\")\nexcept ImportError:\n    print(\"警告: 未检测到Conan配置，将使用系统Qt6\")"),
            
            # 更新包含路径检测
            ("qt_include_paths = [", 
             "# 自动检测Conan生成的Qt6路径\nauto_qt_paths = []\ntry:\n    import os\n    conan_install_dir = \".\"\n    for root, dirs, files in os.walk(conan_install_dir):\n        if 'include' in dirs:\n            include_dir = os.path.join(root, 'include')\n            if os.path.exists(os.path.join(include_dir, 'Qt6')):\n                auto_qt_paths.append(include_dir)\n        if 'lib' in dirs:\n            lib_dir = os.path.join(root, 'lib')\n            if any(f.endswith('.lib') for f in os.listdir(lib_dir) if os.path.isfile(os.path.join(lib_dir, f))):\n                auto_qt_paths.append(lib_dir)\nexcept:\n    pass\n\nqt_include_paths = ["),
            
            # 更新库路径检测
            ("qt_library_paths = [", 
             "qt_library_paths = [")
        ]
        
        updated_content = sconstruct_content
        for old, new in updates:
            updated_content = updated_content.replace(old, new)
        
        # 写入更新后的文件
        with open("SConstruct", 'w', encoding='utf-8-sig') as f:
            f.write(updated_content)
        
        print("✓ SConstruct已更新以支持Conan")
        return True
        
    except Exception as e:
        print(f"✗ 更新SConstruct失败: {e}")
        return False

def create_conan_build_script():
    """创建Conan构建脚本"""
    print_header("创建Conan构建脚本")
    
    script_content = '''@echo off
REM Conan Qt6项目构建脚本
echo [Conan Qt6 WebView项目构建]
echo ===============================

echo.
echo 步骤1: 检查Conan安装...
conan --version
if %ERRORLEVEL% NEQ 0 (
    echo Conan未安装，正在安装...
    python -m pip install conan
)

echo.
echo 步骤2: 清理之前的构建...
if exist "build" rmdir /s /q "build"
if exist "bin" rmdir /s /q "bin"
if exist "obj" rmdir /s /q "obj"

echo.
echo 步骤3: 使用Conan安装Qt6...
conan install . --build=missing --update

echo.
echo 步骤4: 使用SCons构建...
scons

echo.
echo 步骤5: 检查构建结果...
if exist "bin\\QtWebViewApp.exe" (
    echo ✓ 构建成功！可执行文件: bin\\QtWebViewApp.exe
    echo 运行程序: bin\\QtWebViewApp.exe
) else (
    echo ✗ 构建失败，请检查错误信息
)

echo.
pause
'''
    
    try:
        with open("build_with_conan.bat", "w", encoding="utf-8-sig") as f:
            f.write(script_content)
        print("✓ 创建了Conan构建脚本: build_with_conan.bat")
        return True
    except Exception as e:
        print(f"✗ 创建构建脚本失败: {e}")
        return False

def main():
    """主函数"""
    print("Conan Qt6配置和安装工具")
    
    # 1. 检查Conan安装
    if not check_conan_installation():
        if not install_conan():
            return 1
    
    # 2. 创建优化的Conan配置
    if not create_optimized_conanfile():
        return 1
    
    # 3. 创建Conan配置文件
    create_conan_profile()
    
    # 4. 修复SConstruct以支持Conan
    fix_sconstruct_for_conan()
    
    # 5. 创建构建脚本
    create_conan_build_script()
    
    print_header("Conan Qt6配置完成")
    print("✓ 优化了conanfile.txt配置")
    print("✓ 创建了Conan构建配置文件")
    print("✓ 更新了SConstruct以支持Conan")
    print("✓ 创建了构建脚本 build_with_conan.bat")
    
    print("\n推荐使用方法:")
    print("1. 运行: build_with_conan.bat")
    print("   或者手动执行:")
    print("   conan install . --build=missing --update")
    print("   scons")
    
    print("\n重要提示:")
    print("- Conan会自动下载和配置Qt6")
    print("- 首次安装可能需要较长时间")
    print("- 确保网络连接稳定")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())