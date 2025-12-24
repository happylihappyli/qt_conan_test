# -*- coding: utf-8 -*-
"""
TTS通知脚本 - 播放完成提示音
"""
import sys
import os

def speak(text):
    """
    使用Windows TTS播放语音提示
    """
    try:
        import win32com.client
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(text)
        print(f"[TTS] 语音提示: {text}")
    except ImportError:
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            print(f"[TTS] 语音提示: {text}")
        except ImportError:
            print(f"[TTS] 语音库未安装，文本: {text}")
            # 如果没有TTS库，使用系统提示音
            import winsound
            winsound.Beep(1000, 500)  # 频率1000Hz，持续500ms

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = "任务运行完毕，过来看看！"
    
    speak(text)