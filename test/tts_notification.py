# -*- coding: utf-8 -*-
"""
播放任务完成语音提示
"""

import win32com.client

def play_completion_message():
    """播放任务完成语音提示"""
    try:
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak("任务运行完毕，过来看看！")
        print("[OK] 语音提示播放成功")
    except Exception as e:
        print(f"[ERROR] 语音提示播放失败: {e}")

if __name__ == '__main__':
    play_completion_message()
