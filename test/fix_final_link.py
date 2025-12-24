#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复最终链接问题
手动整理编译文件并生成可执行文件
"""

import os
import shutil
import subprocess
import time

def main():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 开始修复最终链接...")
    
    # 设置路径
    project_root = "E:/GitHub3/cpp/qt_conan_test"
    src_dir = os.path.join(project_root, "src")
    obj_dir = os.path.join(project_root, "obj")
    bin_dir = os.path.join(project_root, "bin")
    
    # 确保目录存在
    os.makedirs(bin_dir, exist_ok=True)
    os.makedirs(obj_dir, exist_ok=True)
    
    # 移动obj文件到obj目录
    print("📁 移动obj文件到obj目录...")
    src_files = ['main.obj', 'mainwindow.obj', 'webviewwidget.obj']
    for obj_file in src_files:
        src_path = os.path.join(src_dir, obj_file)
        dest_path = os.path.join(obj_dir, obj_file)
        if os.path.exists(src_path):
            shutil.move(src_path, dest_path)
            print(f"✅ 移动 {obj_file}")
        else:
            print(f"⚠️ 找不到 {obj_file}")
    
    # 检查MOC文件
    print("🔍 检查MOC文件...")
    moc_files = []
    for moc_file in ['mainwindow.moc', 'webviewwidget.moc']:
        moc_path = os.path.join(obj_dir, moc_file)
        if os.path.exists(moc_path):
            moc_files.append(moc_path)
            print(f"✅ 找到 {moc_file}")
        else:
            print(f"❌ 找不到 {moc_file}")
    
    # 检查Conan配置
    conandeps_path = os.path.join(project_root, "SConscript_conandeps")
    if os.path.exists(conandeps_path):
        print("✅ 找到Conan配置")
        
        # 执行scons最终链接
        print("🔧 执行最终链接...")
        os.chdir(project_root)
        result = subprocess.run(['scons'], capture_output=True, text=True)
        
        print("=== SCons输出 ===")
        print(result.stdout)
        if result.stderr:
            print("=== 错误信息 ===")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ 编译成功！")
            
            # 检查生成的可执行文件
            exe_path = os.path.join(bin_dir, "QtWebViewApp.exe")
            if os.path.exists(exe_path):
                file_size = os.path.getsize(exe_path)
                print(f"✅ 可执行文件生成成功: {exe_path} (大小: {file_size:,} 字节)")
                return True
            else:
                print("❌ 可执行文件未生成")
                return False
        else:
            print("❌ 编译失败")
            return False
    else:
        print("❌ 找不到Conan配置")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("🎉 Qt6工具栏+WebView项目编译完成！")
    else:
        print("❌ 编译失败，需要进一步调试")