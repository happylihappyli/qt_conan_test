#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qt6编译错误修复完成提示
"""

import os
import sys
import subprocess
import platform
import time

def text_to_speech(message):
    """将文本转换为语音"""
    try:
        # Windows TTS
        if platform.system() == "Windows":
            # 使用PowerShell调用Windows语音合成
            ps_command = f'Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak("{message}")'
            subprocess.run(["powershell", "-Command", ps_command], check=False, timeout=10)
        else:
            # Linux/Mac TTS (需要安装espeak或say)
            try:
                subprocess.run(["espeak", message], check=False, timeout=10)
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    subprocess.run(["say", message], check=False, timeout=10)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print("无法播放语音提示")
    except Exception as e:
        print(f"语音合成失败: {e}")

def main():
    """主函数"""
    print("Qt6编译错误修复完成!")
    
    # 生成最终报告
    report = f"""
Qt6 WebView项目编译错误修复完成
修复时间: {time.strftime('%Y-%m-%d %H:%M:%S')}

问题原因: 系统中未安装Qt6或路径配置不正确
解决方案: 已创建详细的修复指导文档

修复文件:
✅ COMPILATION_FIX.md - 详细修复指导
✅ setup_qt_env.bat - Qt环境设置脚本  
✅ CMakeLists.txt - 备选编译方案
✅ test/fix_compilation_error.py - 错误诊断工具

关键步骤:
1. 从 https://www.qt.io/download 下载Qt6
2. 安装时选择Qt WebEngine组件 (重要!)
3. 运行 setup_qt_env.bat 设置环境
4. 执行 scons 重新编译

推荐安装路径: D:\\Qt\\6.5.0\\msvc2019_64
"""
    
    print(report)
    
    # 保存报告
    try:
        with open("FIX_REPORT.txt", "w", encoding="utf-8-sig") as f:
            f.write(report)
        print("修复报告已保存到: FIX_REPORT.txt")
    except Exception as e:
        print(f"保存报告失败: {e}")
    
    # 播放语音提示
    tts_message = "Qt6编译错误修复工具已完成! 请查看修复文档并安装Qt6后重新编译!"
    print(f"\n语音提示: {tts_message}")
    
    try:
        text_to_speech(tts_message)
    except Exception as e:
        print(f"播放语音失败: {e}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())