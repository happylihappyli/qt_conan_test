# -*- coding: utf-8 -*-
"""
使用windeployqt工具部署Qt应用程序
"""

import subprocess
import os
import time

def deploy_qt_app():
    """使用windeployqt部署Qt应用"""
    
    print("=" * 60)
    print("使用windeployqt部署Qt应用程序")
    print("=" * 60)
    
    # windeployqt路径
    windeployqt_path = r'D:\Code\Qt\Qt5.14.2\5.14.2\msvc2017_64\bin\windeployqt.exe'
    
    # 目标EXE路径
    exe_path = r'E:\GitHub3\cpp\qt_conan_test\bin\QtWebViewApp.exe'
    
    if not os.path.exists(windeployqt_path):
        print(f"[ERROR] windeployqt不存在: {windeployqt_path}")
        return
    
    if not os.path.exists(exe_path):
        print(f"[ERROR] EXE文件不存在: {exe_path}")
        return
    
    # 构建命令
    cmd = [
        windeployqt_path,
        '--release',
        '--no-translations',
        '--no-system-d3d-compiler',
        '--no-opengl-sw',
        exe_path
    ]
    
    print(f"[INFO] 执行命令: {' '.join(cmd)}")
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 开始部署")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        print("\n" + "=" * 60)
        print("部署输出:")
        print("=" * 60)
        print(result.stdout)
        
        if result.stderr:
            print("\n" + "=" * 60)
            print("错误输出:")
            print("=" * 60)
            print(result.stderr)
        
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 部署完成")
        
        if result.returncode == 0:
            print("[OK] 部署成功！")
        else:
            print(f"[ERROR] 部署失败，返回码: {result.returncode}")
    except Exception as e:
        print(f"[ERROR] 部署失败: {e}")

if __name__ == '__main__':
    deploy_qt_app()
