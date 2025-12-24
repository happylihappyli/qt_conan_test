#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qt6 WebView项目验证和编译脚本
验证项目结构，检查依赖，并提供编译指导
"""

import os
import sys
import time
from pathlib import Path

def print_header(title):
    """打印标题"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

def print_info(message):
    """打印信息"""
    print(f"[INFO] {message}")

def print_warning(message):
    """打印警告"""
    print(f"[WARNING] {message}")

def print_error(message):
    """打印错误"""
    print(f"[ERROR] {message}")

def check_project_structure():
    """检查项目结构"""
    print_header("检查项目结构")
    
    required_files = [
        "conanfile.txt",
        "SConstruct", 
        "src/main.cpp",
        "src/mainwindow.h",
        "src/mainwindow.cpp", 
        "src/webviewwidget.h",
        "src/webviewwidget.cpp"
    ]
    
    required_dirs = ["src", "test", "bin", "obj"]
    
    missing_files = []
    missing_dirs = []
    
    # 检查目录
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print_info(f"目录存在: {dir_name}")
        else:
            missing_dirs.append(dir_name)
            print_error(f"目录缺失: {dir_name}")
    
    # 检查文件
    for file_name in required_files:
        if os.path.exists(file_name):
            print_info(f"文件存在: {file_name}")
        else:
            missing_files.append(file_name)
            print_error(f"文件缺失: {file_name}")
    
    if missing_files or missing_dirs:
        print_error("项目结构不完整!")
        return False
    else:
        print_info("项目结构完整!")
        return True

def check_file_encodings():
    """检查文件编码"""
    print_header("检查文件编码")
    
    cpp_h_files = [
        "src/main.cpp",
        "src/mainwindow.h", 
        "src/mainwindow.cpp",
        "src/webviewwidget.h",
        "src/webviewwidget.cpp"
    ]
    
    for file_path in cpp_h_files:
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
                print_info(f"文件编码正确: {file_path}")
        except UnicodeDecodeError:
            print_error(f"文件编码错误: {file_path}")
        except FileNotFoundError:
            print_error(f"文件不存在: {file_path}")

def analyze_source_code():
    """分析源代码"""
    print_header("源代码分析")
    
    cpp_files = [
        "src/main.cpp",
        "src/mainwindow.cpp", 
        "src/webviewwidget.cpp"
    ]
    
    for file_path in cpp_files:
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
                lines = content.split('\n')
                
                print_info(f"文件: {file_path}")
                print_info(f"  行数: {len(lines)}")
                print_info(f"  字符数: {len(content)}")
                
                # 检查关键功能
                if "Qt6" in content:
                    print_info("  ✓ 使用Qt6")
                if "WebEngine" in content:
                    print_info("  ✓ 包含WebEngine")
                if "工具栏" in content or "toolbar" in content.lower():
                    print_info("  ✓ 包含工具栏功能")
                if "UTF-8" in content or "utf-8" in content.lower():
                    print_info("  ✓ 支持UTF-8编码")
                    
        except Exception as e:
            print_error(f"无法读取文件 {file_path}: {e}")

def check_sconstruct_config():
    """检查SConstruct配置"""
    print_header("检查SConstruct配置")
    
    try:
        with open("SConstruct", 'r', encoding='utf-8-sig') as f:
            content = f.read()
            
        # 检查关键配置
        checks = [
            ("Qt6Core", "Qt6Core模块"),
            ("Qt6WebEngineWidgets", "WebEngine模块"),
            ("utf-8", "UTF-8编码支持"),
            ("bin", "bin目录配置"),
            ("obj", "obj目录配置"),
            ("time.strftime", "时间显示")
        ]
        
        for check_text, description in checks:
            if check_text in content:
                print_info(f"✓ {description}已配置")
            else:
                print_warning(f"✗ {description}可能未配置")
                
    except Exception as e:
        print_error(f"无法读取SConstruct: {e}")

def check_conan_config():
    """检查Conan配置"""
    print_header("检查Conan配置")
    
    try:
        with open("conanfile.txt", 'r', encoding='utf-8-sig') as f:
            content = f.read()
            
        # 检查关键配置
        checks = [
            ("qt/6.5.0", "Qt6版本"),
            ("qtwebengine", "WebEngine组件"),
            ("shared", "共享库配置"),
            ("Scons", "Scons生成器")
        ]
        
        for check_text, description in checks:
            if check_text in content:
                print_info(f"✓ {description}已配置")
            else:
                print_warning(f"✗ {description}可能未配置")
                
    except Exception as e:
        print_error(f"无法读取conanfile.txt: {e}")

def generate_build_guide():
    """生成编译指导"""
    print_header("编译指导")
    
    guide = """
Qt6 WebView项目编译步骤：

1. 安装Qt6和WebEngine
   - 从 https://www.qt.io/download 下载Qt6
   - 安装时选择Qt WebEngine组件
   - 建议版本：Qt 6.5.0 或更新

2. 安装构建工具
   - 安装Visual Studio 2019/2022 (Windows)
   - 安装Python 3.8+
   - 安装Conan: pip install conan
   - 安装Scons: pip install scons

3. 配置Qt环境
   - 设置QTDIR环境变量
   - 将Qt的bin目录添加到PATH

4. 安装Conan依赖
   conan install . --build=missing

5. 编译项目
   scons

6. 运行程序
   ./bin/QtWebViewApp.exe

注意事项：
- 确保Visual Studio工具链可用
- 检查Qt6 WebEngine是否正确安装
- 如果编译失败，检查依赖库路径
"""
    print(guide)

def create_test_script():
    """创建测试脚本"""
    print_header("创建测试脚本")
    
    test_script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qt6 WebView项目功能测试脚本
"""

import subprocess
import sys
import os
import time

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\\n=== {description} ===")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"命令: {cmd}")
        print(f"返回码: {result.returncode}")
        if result.stdout:
            print(f"输出:\\n{result.stdout}")
        if result.stderr:
            print(f"错误:\\n{result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"执行命令失败: {e}")
        return False

def main():
    """主测试函数"""
    print("Qt6 WebView项目测试")
    
    # 测试SConstruct语法
    if not run_command("python SConstruct --help", "测试SConstruct语法"):
        print("SConstruct语法检查失败")
        return False
    
    # 如果存在编译好的程序，测试运行
    exe_path = "bin/QtWebViewApp.exe"
    if os.path.exists(exe_path):
        print(f"\\n找到可执行文件: {exe_path}")
        # 这里可以添加程序运行测试
    else:
        print(f"\\n未找到可执行文件: {exe_path}")
        print("请先完成编译过程")
    
    return True

if __name__ == "__main__":
    main()
'''
    
    try:
        with open("test/test_qt_project.py", "w", encoding="utf-8-sig") as f:
            f.write(test_script)
        print_info("测试脚本已创建: test/test_qt_project.py")
    except Exception as e:
        print_error(f"创建测试脚本失败: {e}")

def main():
    """主函数"""
    start_time = time.time()
    
    print(f"Qt6 WebView项目验证工具")
    print(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查项目结构
    if not check_project_structure():
        print_error("项目结构检查失败!")
        return 1
    
    # 检查文件编码
    check_file_encodings()
    
    # 分析源代码
    analyze_source_code()
    
    # 检查配置文件
    check_sconstruct_config()
    check_conan_config()
    
    # 生成编译指导
    generate_build_guide()
    
    # 创建测试脚本
    create_test_script()
    
    end_time = time.time()
    print_header("验证完成")
    print(f"验证时间: {end_time - start_time:.2f}秒")
    print(f"完成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())