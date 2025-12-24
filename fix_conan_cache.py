#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conan缓存清理和重新配置脚本
解决Qt6下载时的磁盘空间不足问题
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def check_disk_space():
    """检查各盘符空间"""
    print("=== 磁盘空间检查 ===")
    drives = ['C:', 'D:', 'E:', 'F:']
    for drive in drives:
        try:
            result = subprocess.run(['wmic', 'logicaldisk', 'get', 'freespace,size', f'where={drive}'],
                                  capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                values = lines[1].split()
                if len(values) >= 2:
                    free_gb = int(values[0]) / (1024**3) if values[0].isdigit() else 0
                    total_gb = int(values[1]) / (1024**3) if values[1].isdigit() else 0
                    print(f"{drive}: {free_gb:.1f}GB 可用 / {total_gb:.1f}GB 总空间")
        except:
            print(f"{drive}: 无法获取空间信息")

def clean_conan_cache():
    """清理Conan缓存"""
    conan_home = Path.home() / '.conan2'
    if conan_home.exists():
        print(f"=== 清理Conan缓存 {conan_home} ===")
        try:
            cache_size = sum(f.stat().st_size for f in conan_home.rglob('*') if f.is_file())
            cache_gb = cache_size / (1024**3)
            print(f"当前缓存大小: {cache_gb:.1f}GB")
            
            if cache_gb > 0.1:  # 如果缓存大于100MB
                response = input("是否清理Conan缓存? (y/N): ").lower().strip()
                if response == 'y':
                    shutil.rmtree(conan_home)
                    print("✅ Conan缓存已清理")
                    return True
            else:
                print("缓存很小，无需清理")
                return True
        except Exception as e:
            print(f"❌ 清理缓存失败: {e}")
    return False

def setup_conan_cache_on_f_drive():
    """在F盘设置Conan缓存"""
    f_drive = Path('F:/conan_cache')
    
    print("=== 在F盘设置Conan缓存 ===")
    print(f"目标目录: {f_drive}")
    
    try:
        f_drive.mkdir(parents=True, exist_ok=True)
        
        # 设置环境变量
        env_script = """
# 设置Conan使用F盘缓存
$env:CONAN_USER_HOME = "F:/conan_cache"
Write-Host "Conan缓存已设置为: $env:CONAN_USER_HOME" -ForegroundColor Green
"""
        
        with open('set_conan_cache.bat', 'w', encoding='utf-8') as f:
            f.write("@echo off\n")
            f.write("set CONAN_USER_HOME=F:/conan_cache\n")
            f.write("echo Conan缓存已设置为: F:/conan_cache\n")
            f.write("echo 请重新运行Conan命令\n")
            f.write("pause\n")
        
        with open('set_conan_cache.ps1', 'w', encoding='utf-8') as f:
            f.write(env_script)
        
        print("✅ 已创建缓存设置脚本")
        print("   - set_conan_cache.bat (批处理版本)")
        print("   - set_conan_cache.ps1 (PowerShell版本)")
        return True
        
    except Exception as e:
        print(f"❌ 设置F盘缓存失败: {e}")
        return False

def test_conan_cache():
    """测试Conan配置"""
    print("=== 测试Conan配置 ===")
    try:
        result = subprocess.run(['conan', 'config', 'home'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Conan配置正常: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Conan配置测试失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Conan测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🔧 Conan Qt6 缓存修复工具")
    print("=" * 50)
    
    # 1. 检查磁盘空间
    check_disk_space()
    print()
    
    # 2. 清理Conan缓存
    clean_conan_cache()
    print()
    
    # 3. 设置F盘缓存
    setup_conan_cache_on_f_drive()
    print()
    
    # 4. 测试Conan
    test_conan_cache()
    print()
    
    print("📋 使用说明:")
    print("1. 运行 set_conan_cache.bat 或 set_conan_cache.ps1 设置环境变量")
    print("2. 然后重新运行: conan install . --build=missing --update --profile:host=qt6_profile --profile:build=qt6_profile")
    print("3. 如果还有问题，考虑使用本地Qt6安装 + Conan混合方案")

if __name__ == "__main__":
    main()