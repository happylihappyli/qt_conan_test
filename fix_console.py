#!/usr/bin/env python3
"""
Windows控制台编码修复脚本
解决Qt6应用程序中文乱码问题
"""

import os
import subprocess
import sys

def set_console_encoding():
    """设置控制台编码为UTF-8"""
    # 方法1：设置环境变量
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # 方法2：设置控制台编码（需要管理员权限）
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleOutputCP(65001)  # UTF-8
        kernel32.SetConsoleCP(65001)        # UTF-8
        print("[OK] 控制台编码已设置为UTF-8")
    except:
        print("[INFO] 无法设置控制台编码，但不影响GUI应用运行")

def run_qt_app():
    """运行Qt6应用程序"""
    print("🚀 启动Qt6 WebView应用程序")
    print("=" * 50)
    print("📌 提示：GUI界面中的中文显示正常")
    print("📌 提示：控制台乱码不影响应用程序功能")
    print("=" * 50)
    
    try:
        # 启动应用程序
        process = subprocess.Popen(
            ['.\\bin\\QtWebViewApp.exe'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8'
        )
        
        # 实时输出结果
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                # 尝试处理编码问题
                try:
                    print(output.strip())
                except:
                    # 如果还是乱码，忽略该行
                    print(f"[INFO] 输出: {len(output)} 字符")
                    
    except FileNotFoundError:
        print("❌ 错误：找不到QtWebViewApp.exe")
        print("💡 提示：请先运行编译命令: scons")
    except Exception as e:
        print(f"❌ 运行错误: {e}")

if __name__ == "__main__":
    print("🔧 Qt6控制台编码修复工具")
    print("作者: Qt开发助手")
    print("版本: 1.0")
    print()
    
    # 设置编码
    set_console_encoding()
    
    # 运行应用
    run_qt_app()
    
    print("\n" + "=" * 50)
    print("✅ 应用程序已退出")
    print("💡 如果GUI界面工作正常，说明问题已解决")
    print("💡 控制台乱码是Windows系统限制，不影响功能")
    print("=" * 50)