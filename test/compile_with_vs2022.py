#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用VS2022编译器正确编译Qt6项目的脚本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def setup_vs2022_environment():
    """设置VS2022编译环境"""
    print("🌟 设置VS2022编译环境...")
    
    # VS2022安装路径
    vs_install_paths = [
        r"D:\Code\VS2022\Community",
        r"C:\Program Files\Microsoft Visual Studio\2022\Community",
        r"C:\Program Files\Microsoft Visual Studio\2022\Professional",
        r"C:\Program Files\Microsoft Visual Studio\2022\Enterprise"
    ]
    
    # 查找VS2022安装目录
    vs_install_dir = None
    for path in vs_install_paths:
        if Path(path).exists():
            vs_install_dir = path
            print(f"✅ 找到VS2022: {vs_install_dir}")
            break
    
    if not vs_install_dir:
        print("❌ 未找到VS2022安装目录!")
        return False
    
    # MSVC版本（使用较新的版本）
    msvc_version = "14.44.35207"  # 使用更新的版本
    vc_tools_path = Path(vs_install_dir) / "VC" / "Tools" / "MSVC" / msvc_version
    
    if not vc_tools_path.exists():
        # 如果新版本不存在，使用旧版本
        msvc_version = "14.29.30133"
        vc_tools_path = Path(vs_install_dir) / "VC" / "Tools" / "MSVC" / msvc_version
        
        if not vc_tools_path.exists():
            print(f"❌ 未找到MSVC {msvc_version}!")
            return False
    
    print(f"✅ 使用MSVC版本: {msvc_version}")
    
    # 设置环境变量
    os.environ["VCINSTALLDIR"] = str(Path(vs_install_dir) / "VC")
    os.environ["VCToolsInstallDir"] = str(vc_tools_path) + "\\"
    os.environ["VCToolsVersion"] = msvc_version
    
    # 添加编译器路径到PATH
    compiler_path = vc_tools_path / "bin" / "Hostx64" / "x64"
    if compiler_path.exists():
        if "PATH" in os.environ:
            os.environ["PATH"] = str(compiler_path) + ";" + os.environ["PATH"]
        else:
            os.environ["PATH"] = str(compiler_path)
        print(f"✅ 添加编译器路径: {compiler_path}")
    
    # Windows SDK路径
    windows_sdk_paths = [
        Path(vs_install_dir) / "SDK" / "10",
        Path("C:/Program Files (x86)/Windows Kits/10")
    ]
    
    windows_sdk_dir = None
    for sdk_path in windows_sdk_paths:
        if sdk_path.exists():
            windows_sdk_dir = sdk_path
            print(f"✅ 找到Windows SDK: {windows_sdk_dir}")
            break
    
    if windows_sdk_dir:
        # 查找最新版本的SDK
        include_dirs = [d for d in windows_sdk_dir.glob("Include/*") if d.is_dir()]
        if include_dirs:
            latest_sdk = sorted(include_dirs)[-1]
            os.environ["WindowsSdkDir"] = str(latest_sdk.parent)
            os.environ["WindowsSdkVersion"] = latest_sdk.name
            
            # 添加SDK Include路径
            include_path = latest_sdk / "um"
            if include_path.exists():
                if "INCLUDE" in os.environ:
                    os.environ["INCLUDE"] = str(include_path) + ";" + os.environ["INCLUDE"]
                else:
                    os.environ["INCLUDE"] = str(include_path)
                print(f"✅ 添加SDK Include路径: {include_path}")
            
            # 添加SDK Lib路径
            lib_path = latest_sdk.parent / "Lib" / latest_sdk.name / "um" / "x64"
            if lib_path.exists():
                if "LIB" in os.environ:
                    os.environ["LIB"] = str(lib_path) + ";" + os.environ["LIB"]
                else:
                    os.environ["LIB"] = str(lib_path)
                print(f"✅ 添加SDK Lib路径: {lib_path}")
    
    # 设置平台工具集
    platform_toolset = "v143"
    os.environ["PlatformToolset"] = platform_toolset
    
    # 基本编译环境
    os.environ["_CL_"] = "/permissive- /Zc:__cplusplus"
    os.environ["_CXX_"] = "/permissive- /Zc:__cplusplus"
    
    print("✅ VS2022环境设置完成")
    return True

def compile_with_vs2022():
    """使用VS2022编译项目"""
    print("\n🔨 开始编译Qt6项目...")
    
    # 设置项目路径
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"
    obj_dir = project_root / "obj"
    bin_dir = project_root / "bin"
    
    # 确保目录存在
    obj_dir.mkdir(exist_ok=True)
    bin_dir.mkdir(exist_ok=True)
    
    # 清理旧的编译文件
    print("🧹 清理旧的编译文件...")
    for obj_file in obj_dir.glob("*.obj"):
        obj_file.unlink()
    for exe_file in bin_dir.glob("*.exe"):
        exe_file.unlink()
    
    # 加载Conan环境
    print("🌟 加载Conan环境...")
    conan_env_script = project_root / "conanbuildenv-release-x86_64.bat"
    if conan_env_script.exists():
        # 使用PowerShell设置环境
        cmd = f"powershell -Command \"& '{conan_env_script}'; Write-Host 'Conan环境已加载'\""
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Conan环境加载成功")
        else:
            print(f"⚠️ Conan环境加载警告: {result.stderr}")
    
    # 查找编译器
    cl_exe = None
    msvc_versions = ["14.44.35207", "14.29.30133"]
    
    for version in msvc_versions:
        compiler_paths = [
            Path(f"D:/Code/VS2022/Community/VC/Tools/MSVC/{version}/bin/Hostx64/x64/cl.exe"),
            Path(f"C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/{version}/bin/Hostx64/x64/cl.exe")
        ]
        
        for compiler_path in compiler_paths:
            if compiler_path.exists():
                cl_exe = str(compiler_path)
                print(f"✅ 找到编译器: {cl_exe}")
                break
        if cl_exe:
            break
    
    if not cl_exe:
        print("❌ 未找到Visual Studio编译器!")
        return False
    
    # 源文件列表
    source_files = [
        "src/main.cpp",
        "src/mainwindow.cpp", 
        "src/webviewwidget.cpp"
    ]
    
    # MOC文件处理
    moc_files = []
    moc_cpp_files = []
    moc_obj_files = []
    
    # 检查MOC文件
    moc_headers = [
        (src_dir / "mainwindow.h", "mainwindow.moc"),
        (src_dir / "webviewwidget.h", "webviewwidget.moc")
    ]
    
    for header_file, moc_name in moc_headers:
        if header_file.exists():
            moc_file = obj_dir / moc_name
            if not moc_file.exists():
                print(f"❌ MOC文件不存在: {moc_file}")
                return False
            moc_files.append(moc_file)
            
            # 创建对应的.cpp文件
            cpp_name = moc_name.replace('.moc', '.cpp')
            cpp_file = obj_dir / cpp_name
            
            if not cpp_file.exists():
                shutil.copy2(moc_file, cpp_file)
                print(f"📄 创建MOC .cpp文件: {cpp_name}")
            
            moc_cpp_files.append(cpp_file)
            
            # 编译MOC文件
            obj_name = moc_name.replace('.moc', '.obj')
            obj_file = obj_dir / obj_name
            moc_obj_files.append(obj_file)
            
            print(f"🔧 编译MOC: {cpp_name} -> {obj_name}")
    
    # 编译所有源文件
    obj_files = []
    
    # 编译MOC文件
    for cpp_file, obj_file in zip(moc_cpp_files, moc_obj_files):
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
            '/std:c++17',
            '/permissive-'
        ]
        
        print(f"🔧 {' '.join(compile_cmd)}")
        result = subprocess.run(compile_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ 编译失败: {cpp_file.name}")
            print(f"错误: {result.stderr}")
            return False
        else:
            print(f"✅ 编译成功: {cpp_file.name}")
            obj_files.append(obj_file)
    
    # 编译普通源文件
    for source_file in source_files:
        source_path = project_root / source_file
        if not source_path.exists():
            print(f"❌ 源文件不存在: {source_file}")
            continue
            
        # 生成对象文件名
        rel_path = source_path.relative_to(project_root)
        obj_name = str(rel_path).replace('.cpp', '.obj').replace('/', '_')
        obj_file = obj_dir / obj_name
        obj_files.append(obj_file)
        
        compile_cmd = [
            cl_exe,
            '/c', str(source_path),
            '/Fo' + str(obj_file),
            '/I' + str(src_dir),
            '/W3',
            '/EHsc',
            '/MD',
            '/Zi',
            '/Zc:__cplusplus',
            '/std:c++17',
            '/permissive-'
        ]
        
        print(f"🔧 {' '.join(compile_cmd)}")
        result = subprocess.run(compile_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ 编译失败: {source_file}")
            print(f"错误: {result.stderr}")
            return False
        else:
            print(f"✅ 编译成功: {source_file}")
    
    # 链接所有对象文件
    print(f"\n🔗 链接对象文件...")
    
    # 获取Qt6库路径
    qt_libs = []
    if os.path.exists("SConscript_conandeps"):
        try:
            # 尝试从Conan配置获取库
            exec("conandeps = {}")
            with open("SConscript_conandeps", 'r') as f:
                content = f.read()
                if '"LIBS"' in content:
                    # 简化处理，直接使用已知库
                    qt_libs = [
                        'Qt6Core', 'Qt6Gui', 'Qt6Widgets', 'Qt6Network', 'Qt6Sql',
                        'kernel32', 'user32', 'gdi32', 'comdlg32', 'ole32', 'oleaut32',
                        'uuid', 'winmm', 'imm32', 'wininet', 'wsock32', 'ws2_32'
                    ]
        except:
            qt_libs = [
                'Qt6Core', 'Qt6Gui', 'Qt6Widgets', 'Qt6Network', 'Qt6Sql',
                'kernel32', 'user32', 'gdi32', 'comdlg32', 'ole32', 'oleaut32',
                'uuid', 'winmm', 'imm32', 'wininet', 'wsock32', 'ws2_32'
            ]
    else:
        qt_libs = [
            'Qt6Core', 'Qt6Gui', 'Qt6Widgets', 'Qt6Network', 'Qt6Sql',
            'kernel32', 'user32', 'gdi32', 'comdlg32', 'ole32', 'oleaut32',
            'uuid', 'winmm', 'imm32', 'wininet', 'wsock32', 'ws2_32'
        ]
    
    exe_file = bin_dir / "QtWebViewApp.exe"
    
    link_cmd = [
        cl_exe,
        '/Fe' + str(exe_file),
        '/Fo' + str(obj_dir) + '\\',
        '/SUBSYSTEM:WINDOWS',
        '/MACHINE:X64',
        '/DEBUG'
    ]
    
    # 添加所有对象文件
    link_cmd.extend([str(obj) for obj in obj_files])
    
    # 添加库文件
    for lib in qt_libs:
        link_cmd.append(lib + '.lib')
    
    print(f"🔧 {' '.join(link_cmd)}")
    result = subprocess.run(link_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ 链接失败!")
        print(f"错误: {result.stderr}")
        return False
    else:
        print(f"✅ 链接成功!")
        print(f"🎉 生成可执行文件: {exe_file}")
        if exe_file.exists():
            size = exe_file.stat().st_size
            print(f"文件大小: {size:,} 字节 ({size/1024/1024:.2f} MB)")
        return True

def main():
    """主函数"""
    print("=" * 60)
    print("Qt6项目编译工具 - 使用VS2022编译器")
    print("=" * 60)
    
    # 设置VS2022环境
    if not setup_vs2022_environment():
        print("❌ 环境设置失败!")
        return False
    
    # 编译项目
    if not compile_with_vs2022():
        print("❌ 编译失败!")
        return False
    
    print("\n🎉 编译完成!")
    print("您可以运行 bin\\QtWebViewApp.exe 来启动应用程序")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)