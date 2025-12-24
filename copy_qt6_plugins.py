#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
复制Qt6插件目录到bin目录
解决Qt平台插件找不到的问题
"""

import os
import shutil
import glob

def copy_qt6_plugins():
    """复制Qt6插件目录到bin目录"""
    # Qt6插件源目录
    qt6_plugins_dir = r'C:\Users\happyli\.conan2\p\b\qtb73b254637aeb\p\plugins'
    
    # 目标目录
    project_root = os.path.abspath('.')
    bin_dir = os.path.join(project_root, 'bin')
    
    # 确保bin目录存在
    os.makedirs(bin_dir, exist_ok=True)
    
    print("🔧 开始复制Qt6插件目录到bin目录...")
    
    # 检查源目录是否存在
    if not os.path.exists(qt6_plugins_dir):
        print(f"❌ Qt6插件目录不存在: {qt6_plugins_dir}")
        return False
    
    # 复制整个plugins目录
    target_plugins_dir = os.path.join(bin_dir, 'plugins')
    
    try:
        if os.path.exists(target_plugins_dir):
            shutil.rmtree(target_plugins_dir)
            print(f"🗑️  删除旧插件目录: {target_plugins_dir}")
        
        shutil.copytree(qt6_plugins_dir, target_plugins_dir)
        print(f"✅ 复制插件目录成功: {target_plugins_dir}")
        
        # 列出复制的插件目录
        print("\n📦 复制的插件目录:")
        for root, dirs, files in os.walk(target_plugins_dir):
            level = root.replace(target_plugins_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files[:5]:  # 只显示前5个文件
                print(f"{subindent}{file}")
            if len(files) > 5:
                print(f"{subindent}... 和其他 {len(files) - 5} 个文件")
        
        print(f"\n🎉 完成！Qt6插件已复制到 {target_plugins_dir}")
        return True
        
    except Exception as e:
        print(f"❌ 复制插件目录失败: {e}")
        return False

if __name__ == "__main__":
    copy_qt6_plugins()