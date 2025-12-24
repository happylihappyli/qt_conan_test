#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的MOC文件重新生成和编译脚本
"""

import os
import shutil
import subprocess
import time

def main():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 开始完整的MOC生成和编译...")
    
    # 设置路径
    project_root = "E:/GitHub3/cpp/qt_conan_test"
    src_dir = os.path.join(project_root, "src")
    obj_dir = os.path.join(project_root, "obj")
    bin_dir = os.path.join(project_root, "bin")
    moc_path = "C:/Users/happyli/.conan2/p/b/qtb73b254637aeb/p/bin/moc.exe"
    
    # 确保目录存在
    os.makedirs(bin_dir, exist_ok=True)
    os.makedirs(obj_dir, exist_ok=True)
    
    # 删除现有的MOC文件
    print("🗑️ 删除现有MOC文件...")
    for moc_file in ['mainwindow.moc', 'webviewwidget.moc']:
        moc_path_full = os.path.join(obj_dir, moc_file)
        if os.path.exists(moc_path_full):
            try:
                os.remove(moc_path_full)
                print(f"✅ 删除 {moc_file}")
            except Exception as e:
                print(f"❌ 无法删除 {moc_file}: {e}")
    
    # 检查MOC工具
    if not os.path.exists(moc_path):
        print(f"❌ MOC工具不存在: {moc_path}")
        return False
    
    print(f"✅ 使用MOC工具: {moc_path}")
    
    # 生成新的MOC文件
    headers = [
        ('src/mainwindow.h', 'mainwindow.moc'),
        ('src/webviewwidget.h', 'webviewwidget.moc')
    ]
    
    moc_files = []
    for header_file, moc_file in headers:
        header_path = os.path.join(project_root, header_file)
        moc_path_target = os.path.join(obj_dir, moc_file)
        
        if os.path.exists(header_path):
            try:
                cmd = [moc_path, '-o', moc_path_target, header_path]
                print(f"🔧 生成MOC: {cmd}")
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0 and os.path.exists(moc_path_target):
                    moc_files.append(moc_path_target)
                    print(f"✅ 成功生成 {moc_file}")
                else:
                    print(f"❌ 生成 {moc_file} 失败")
                    print(f"错误输出: {result.stderr}")
            except Exception as e:
                print(f"❌ 生成 {moc_file} 时出错: {e}")
        else:
            print(f"❌ 头文件不存在: {header_path}")
    
    print(f"✅ 生成了 {len(moc_files)} 个MOC文件")
    
    # 运行scons编译
    print("🔧 运行SCons编译...")
    os.chdir(project_root)
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONUTF8'] = '1'
    
    try:
        # 使用UTF-8编码处理subprocess输出
        result = subprocess.run(['scons'], 
                               capture_output=True, 
                               text=True, 
                               encoding='utf-8', 
                               errors='replace',
                               env=env)
    except UnicodeDecodeError as e:
        print(f"编码错误，尝试使用默认编码: {e}")
        result = subprocess.run(['scons'], 
                               capture_output=True, 
                               text=True,
                               env=env)
    
    print("=== SCons输出 ===")
    print(result.stdout)
    if result.stderr:
        print("=== 错误信息 ===")
        print(result.stderr)
    
    if result.returncode == 0:
        exe_path = os.path.join(bin_dir, "QtWebViewApp.exe")
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path)
            print(f"🎉 编译成功！可执行文件: {exe_path} (大小: {file_size:,} 字节)")
            return True
        else:
            print("❌ 可执行文件未生成")
            return False
    else:
        print("❌ 编译失败")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("🎉 Qt6工具栏+WebView项目编译完成！")
    else:
        print("❌ 编译失败")