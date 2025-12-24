#!/usr/bin/env python3
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
    print(f"\n=== {description} ===")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"命令: {cmd}")
        print(f"返回码: {result.returncode}")
        if result.stdout:
            print(f"输出:\n{result.stdout}")
        if result.stderr:
            print(f"错误:\n{result.stderr}")
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
        print(f"\n找到可执行文件: {exe_path}")
        # 这里可以添加程序运行测试
    else:
        print(f"\n未找到可执行文件: {exe_path}")
        print("请先完成编译过程")
    
    return True

if __name__ == "__main__":
    main()
