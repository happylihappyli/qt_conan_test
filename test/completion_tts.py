#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS语音提示 - Qt6项目编译完成
"""

import pyttsx3
import time

def play_completion_tts():
    """播放编译完成的语音提示"""
    try:
        # 初始化TTS引擎
        engine = pyttsx3.init()
        
        # 设置语音参数
        voices = engine.getProperty('voices')
        if voices:
            # 选择中文语音（如果可用）
            for voice in voices:
                if 'chinese' in voice.name.lower() or 'chinese' in voice.id.lower():
                    engine.setProperty('voice', voice.id)
                    break
        
        # 设置语速和音量
        engine.setProperty('rate', 150)  # 语速
        engine.setProperty('volume', 0.8)  # 音量
        
        # 播放编译完成提示
        messages = [
            "任务运行完毕，过来看看！",
            "Qt6工具栏和WebView项目编译成功！",
            "生成的可执行文件已保存在bin目录",
            "现在可以运行应用进行测试"
        ]
        
        for message in messages:
            print(f"🎤 TTS提示: {message}")
            engine.say(message)
            engine.runAndWait()
            time.sleep(1)
            
    except Exception as e:
        print(f"TTS播放失败: {e}")
        # 备用提示
        print("=" * 50)
        print("🎉 Qt6项目编译完成！")
        print("📁 可执行文件: bin/QtWebViewApp.exe")
        print("📦 使用Conan管理的Qt6.7.3依赖")
        print("🔧 使用SCons编译系统")
        print("=" * 50)

if __name__ == "__main__":
    play_completion_tts()