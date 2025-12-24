#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编译WebEngine版本的脚本
设置VS2022环境并尝试编译
"""

import os
import subprocess
import sys
import time

def setup_vs2022_environment():
    """设置VS2022编译环境"""
    print("设置VS2022编译环境...")
    
    vs2022_path = r"D:\Code\VS2022\Community"
    vcvars_path = os.path.join(vs2022_path, r"VC\Auxiliary\Build\vcvars64.bat")
    
    if not os.path.exists(vcvars_path):
        print(f"错误：未找到VC环境脚本: {vcvars_path}")
        return False
    
    # 创建批处理文件来设置环境
    bat_content = f"""@echo off
call "{vcvars_path}" -vcvars_ver=14.29
echo VS2022环境已设置
echo INCLUDE=%INCLUDE%
echo LIB=%LIB%
echo PATH=%PATH%
"""
    
    bat_file = "temp_vs_env.bat"
    with open(bat_file, 'w', encoding='gbk') as f:
        f.write(bat_content)
    
    print("正在执行VS2022环境设置...")
    result = subprocess.run(bat_file, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"VS2022环境设置失败: {result.stderr}")
        return False
    
    print("VS2022环境设置成功")
    print(result.stdout)
    
    # 清理临时文件
    try:
        os.remove(bat_file)
    except:
        pass
    
    return True

def compile_with_cl():
    """使用cl编译器编译项目"""
    print("\n开始编译项目...")
    
    # 清理之前的编译结果
    if os.path.exists("obj"):
        import shutil
        shutil.rmtree("obj")
    if os.path.exists("bin"):
        shutil.rmtree("bin")
    
    os.makedirs("obj", exist_ok=True)
    os.makedirs("bin", exist_ok=True)
    
    # 设置基本编译参数
    include_paths = [
        r"C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\webenginewidgets\api",
        r"C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\webenginewidgets",
        r"C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\core\api",
        r"C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\core",
        r"C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\webengine",
        r"C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\tools\mkspecs",
    ]
    
    include_args = " ".join([f'/I"{path}"' for path in include_paths if os.path.exists(path)])
    
    # 编译命令
    compile_cmd = f'cl /nologo /c /std:c++17 /utf-8 /W3 /EHsc {include_args} src\\main.cpp /Foobj\\main.obj'
    
    print(f"执行命令: {compile_cmd}")
    
    try:
        result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("编译成功！")
            print(result.stdout)
            return True
        else:
            print("编译失败！")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"编译过程中出错: {e}")
        return False

def main():
    """主函数"""
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 开始WebEngine编译任务")
    
    # 检查源文件
    if not os.path.exists("src/main.cpp"):
        print("错误：未找到源文件 src/main.cpp")
        return False
    
    # 设置VS2022环境
    if not setup_vs2022_environment():
        print("VS2022环境设置失败，尝试直接编译...")
    
    # 尝试编译
    success = compile_with_cl()
    
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 编译任务结束")
    
    if success:
        print("✅ 编译成功完成")
    else:
        print("❌ 编译失败")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)