#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复SConstruct文件中的编码问题
"""

import re

def main():
    file_path = "E:/GitHub3/cpp/qt_conan_test/SConstruct"
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换emoji符号为普通文本
    replacements = {
        '✅': '[OK]',
        '⚠️': '[WARNING]',
        '🔧': '[INFO]',
        '🔍': '[INFO]',
        '📁': '[DIR]',
        '🎉': '[SUCCESS]',
        '❌': '[ERROR]'
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ SConstruct编码问题已修复")

if __name__ == "__main__":
    main()