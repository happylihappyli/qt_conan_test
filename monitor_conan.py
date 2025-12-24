#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conan构建进度监控脚本
监控Qt WebEngine依赖的下载和编译进度
"""

import os
import time
import subprocess
import json
from datetime import datetime

def monitor_conan_progress():
    """监控Conan构建进度"""
    print("🔄 开始监控Conan构建进度...")
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查Conan缓存目录大小变化
    cache_dir = "C:/Users/happyli/.conan2"
    
    if os.path.exists(cache_dir):
        print(f"📁 Conan缓存目录: {cache_dir}")
        
        # 记录初始状态
        initial_size = get_directory_size(cache_dir)
        print(f"📊 初始缓存大小: {format_size(initial_size)}")
        
        # 监控循环
        for i in range(10):  # 监控10次，每次间隔30秒
            time.sleep(30)
            
            current_size = get_directory_size(cache_dir)
            size_diff = current_size - initial_size
            
            print(f"⏱️  {datetime.now().strftime('%H:%M:%S')} - 缓存大小: {format_size(current_size)} (增长: {format_size(size_diff)})")
            
            if size_diff > 1024 * 1024 * 100:  # 如果增长超过100MB，说明在下载
                print("📥 正在下载依赖...")
            elif i > 2:  # 3分钟后检查构建状态
                print("🔨 可能正在进行编译...")
                
    else:
        print("❌ Conan缓存目录不存在")

def get_directory_size(path):
    """获取目录大小"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, IOError):
                    continue
    except (OSError, IOError):
        pass
    return total_size

def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"

if __name__ == "__main__":
    monitor_conan_progress()