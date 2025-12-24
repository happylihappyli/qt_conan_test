# -*- coding: utf-8 -*-
"""
编译脚本 - 使用SCons编译Qt5 WebEngine项目
"""

import subprocess
import time
import sys
import os

def speak(text):
    """使用TTS播放语音提示"""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[TTS] 语音提示失败: {e}")

def run_command(cmd):
    """运行命令并返回结果"""
    print(f"[CMD] 执行命令: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
    if result.returncode != 0:
        print(f"[ERROR] 命令执行失败: {result.stderr}")
        return False
    print(result.stdout)
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("Qt5 WebEngine项目编译脚本")
    print("=" * 60)
    
    start_time = time.time()
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 开始编译")
    
    # 设置VS2022环境
    print("\n[INFO] 配置VS2022编译环境...")
    vs_path = r"D:\Code\VS2022\Community\VC\Auxiliary\Build\vcvars64.bat"
    if not os.path.exists(vs_path):
        print(f"[ERROR] VS2022路径不存在: {vs_path}")
        return False
    
    # 清理旧的编译文件
    print("\n[INFO] 清理旧的编译文件...")
    if os.path.exists("obj"):
        import shutil
        shutil.rmtree("obj")
        print("[OK] 已清理obj目录")
    
    # 使用SCons编译
    print("\n[INFO] 使用SCons编译项目...")
    
    # 先调用vcvars64.bat设置环境，然后运行scons
    cmd = f'"{vs_path}" && scons -j4'
    print(f"[CMD] {cmd}")
    
    result = subprocess.run(cmd, shell=True, capture_output=False)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 编译完成")
    print(f"[INFO] 耗时: {elapsed_time:.2f}秒")
    
    if result.returncode == 0:
        print("[OK] 编译成功!")
        speak("任务运行完毕，过来看看！")
        return True
    else:
        print("[ERROR] 编译失败!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
