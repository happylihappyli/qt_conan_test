#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复MOC链接问题的脚本
重新生成MOC文件并确保正确编译
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_cmd(cmd, cwd=None, shell=True):
    """运行命令并返回结果"""
    print(f"🔧 执行命令: {cmd}")
    try:
        result = subprocess.run(cmd, shell=shell, cwd=cwd, capture_output=True, text=True)
        print(f"返回码: {result.returncode}")
        if result.stdout:
            print(f"标准输出: {result.stdout}")
        if result.stderr:
            print(f"错误输出: {result.stderr}")
        return result
    except Exception as e:
        print(f"❌ 命令执行失败: {e}")
        return None

def main():
    # 设置项目路径
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"
    obj_dir = project_root / "obj"
    bin_dir = project_root / "bin"
    
    print(f"项目根目录: {project_root}")
    print(f"源码目录: {src_dir}")
    print(f"对象目录: {obj_dir}")
    print(f"输出目录: {bin_dir}")
    
    # 确保目录存在
    obj_dir.mkdir(exist_ok=True)
    bin_dir.mkdir(exist_ok=True)
    
    # 清理旧的MOC文件
    print("\n🧹 清理旧的MOC文件...")
    for moc_file in obj_dir.glob("*.moc"):
        print(f"删除: {moc_file}")
        moc_file.unlink()
    
    for cpp_file in obj_dir.glob("*.cpp"):
        if cpp_file.name.endswith(".moc.cpp"):
            print(f"删除: {cpp_file}")
            cpp_file.unlink()
    
    # 加载Conan环境
    print("\n🌟 加载Conan环境...")
    if (project_root / "conanbuildenv-release-x86_64.bat").exists():
        # 在PowerShell中运行批处理文件
        cmd = f"powershell -Command \"& '{project_root}/conanbuildenv-release-x86_64.bat'\""
        result = run_cmd(cmd)
    
    # 查找moc.exe
    print("\n🔍 查找MOC可执行文件...")
    moc_exe = None
    
    # 1. 从Conan配置中查找
    try:
        from SCons.Script import SConscript
        conandeps_path = project_root / "SConscript_conandeps"
        if conandeps_path.exists():
            print("加载Conan依赖配置...")
            exec(f"conandeps = SConscript('{conandeps_path}')", globals())
            if 'conandeps' in globals() and 'conandeps' in globals()['conandeps']:
                qt_config = globals()['conandeps']['conandeps']
                if 'BINPATH' in qt_config:
                    for bin_path in qt_config['BINPATH']:
                        moc_path = Path(bin_path) / "moc.exe"
                        if moc_path.exists():
                            moc_exe = moc_path
                            print(f"✅ 从Conan配置找到MOC: {moc_exe}")
                            break
    except Exception as e:
        print(f"❌ 加载Conan配置失败: {e}")
    
    # 2. 从常见路径查找
    if not moc_exe:
        common_moc_paths = [
            r"C:\Users\happyli\.conan2\p\b\qtb73b254637aeb\p\bin\moc.exe",
            r"D:\Qt\6.7.3\msvc2019_64\bin\moc.exe",
            r"C:\Qt\6.7.3\msvc2019_64\bin\moc.exe",
        ]
        
        for moc_path in common_moc_paths:
            if Path(moc_path).exists():
                moc_exe = Path(moc_path)
                print(f"✅ 从常见路径找到MOC: {moc_exe}")
                break
    
    if not moc_exe:
        print("❌ 未找到MOC可执行文件!")
        return False
    
    # 生成MOC文件
    print(f"\n📄 生成MOC文件...")
    headers = [
        (src_dir / "mainwindow.h", obj_dir / "mainwindow.moc"),
        (src_dir / "webviewwidget.h", obj_dir / "webviewwidget.moc")
    ]
    
    moc_files = []
    for header_file, moc_file in headers:
        if header_file.exists():
            cmd = [str(moc_exe), '-o', str(moc_file), str(header_file)]
            print(f"🔧 生成MOC: {cmd}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                moc_files.append(moc_file)
                print(f"✅ 成功生成 {moc_file.name}")
            else:
                print(f"❌ 生成 {moc_file.name} 失败")
                print(f"错误: {result.stderr}")
                return False
        else:
            print(f"❌ 头文件不存在: {header_file}")
            return False
    
    # 编译MOC文件
    print(f"\n🔨 编译MOC文件...")
    moc_obj_files = []
    
    for moc_file in moc_files:
        # 将.moc文件重命名为.cpp文件
        cpp_file = obj_dir / f"{moc_file.stem}.cpp"
        
        # 复制MOC文件为.cpp文件
        if not cpp_file.exists():
            shutil.copy2(moc_file, cpp_file)
            print(f"📄 复制MOC文件: {moc_file.name} -> {cpp_file.name}")
        
        # 编译.cpp文件为.obj文件
        obj_file = obj_dir / f"{moc_file.stem}.obj"
        moc_obj_files.append(obj_file)
        
        # 查找编译器
        cl_exe = None
        common_cl_paths = [
            r"D:\Code\VS2022\Community\VC\Tools\MSVC\14.40.33807\bin\Hostx64\x64\cl.exe",
            r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.40.33807\bin\Hostx64\x64\cl.exe",
        ]
        
        for cl_path in common_cl_paths:
            if Path(cl_path).exists():
                cl_exe = cl_path
                break
        
        if not cl_exe:
            # 尝试使用系统PATH中的cl
            result = run_cmd("where cl")
            if result and result.returncode == 0:
                cl_exe = result.stdout.strip().split('\n')[0]
        
        if not cl_exe:
            print("❌ 未找到C++编译器!")
            return False
        
        print(f"✅ 使用编译器: {cl_exe}")
        
        # 编译命令
        compile_cmd = [
            cl_exe,
            '/c', str(cpp_file),
            '/Fo' + str(obj_file),
            '/I' + str(src_dir),
            '/W3',
            '/EHsc',
            '/MD',
            '/Zi',
            '/Zc:__cplusplus',
            '/std:c++17'
        ]
        
        print(f"🔧 编译命令: {' '.join(compile_cmd)}")
        result = subprocess.run(compile_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ 成功编译 {cpp_file.name} -> {obj_file.name}")
        else:
            print(f"❌ 编译失败 {cpp_file.name}")
            print(f"错误: {result.stderr}")
            return False
    
    print(f"\n✅ MOC处理完成!")
    print(f"生成的MOC .obj文件:")
    for obj_file in moc_obj_files:
        print(f"  - {obj_file}")
    
    # 运行SCons编译
    print(f"\n🔨 运行SCons编译...")
    result = run_cmd("scons", cwd=project_root)
    
    if result and result.returncode == 0:
        print(f"\n🎉 编译成功!")
        exe_file = bin_dir / "QtWebViewApp.exe"
        if exe_file.exists():
            print(f"✅ 生成可执行文件: {exe_file}")
            print(f"文件大小: {exe_file.stat().st_size} 字节")
        return True
    else:
        print(f"\n❌ 编译失败!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)