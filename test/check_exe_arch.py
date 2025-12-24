# -*- coding: utf-8 -*-
"""
检查exe文件的位数
"""
import struct

def check_exe_architecture(exe_path):
    """
    检查exe文件的位数
    """
    try:
        with open(exe_path, 'rb') as f:
            # 读取DOS头
            dos_header = f.read(64)
            if dos_header[:2] != b'MZ':
                return "无效的EXE文件"
            
            # 读取PE头偏移
            pe_offset = struct.unpack('<I', dos_header[60:64])[0]
            
            # 跳转到PE头
            f.seek(pe_offset)
            
            # 读取PE签名
            pe_signature = f.read(4)
            if pe_signature != b'PE\x00\x00':
                return "无效的PE文件"
            
            # 读取文件头
            file_header = f.read(20)
            
            # 读取机器类型
            machine = struct.unpack('<H', file_header[0:2])[0]
            
            if machine == 0x014c:
                return "32位 (x86)"
            elif machine == 0x8664:
                return "64位 (x64)"
            else:
                return f"未知架构: 0x{machine:04x}"
    except Exception as e:
        return f"错误: {e}"

if __name__ == "__main__":
    import os
    
    # 检查exe文件
    exe_path = r"E:\GitHub3\cpp\qt_conan_test\bin\QtWebViewApp.exe"
    if os.path.exists(exe_path):
        print(f"EXE文件: {exe_path}")
        print(f"位数: {check_exe_architecture(exe_path)}")
    else:
        print(f"EXE文件不存在: {exe_path}")
    
    # 检查Qt DLL
    dll_path = r"E:\GitHub3\cpp\qt_conan_test\bin\Qt5Core.dll"
    if os.path.exists(dll_path):
        print(f"\nQt DLL: {dll_path}")
        print(f"位数: {check_exe_architecture(dll_path)}")
    else:
        print(f"\nQt DLL不存在: {dll_path}")
