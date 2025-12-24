#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试VS2022编译环境是否可用
"""

import os
import subprocess
import sys

def test_vs2022_environment():
    """测试VS2022环境"""
    print("测试VS2022编译环境...")
    
    # 检查VS2022路径
    vs2022_path = r"D:\Code\VS2022\Community"
    vcvars_path = os.path.join(vs2022_path, r"VC\Auxiliary\Build\vcvars64.bat")
    
    print(f"VS2022路径: {vs2022_path}")
    print(f"VCVARS路径: {vcvars_path}")
    
    if not os.path.exists(vcvars_path):
        print("❌ 未找到VCVARS脚本")
        return False
    
    # 创建测试批处理文件
    test_bat = "test_vs_env.bat"
    with open(test_bat, 'w', encoding='utf-8') as f:
        f.write(f'''@echo off
call "{vcvars_path}" -vcvars_ver=14.29
echo 测试VS2022环境...
cl /version
echo 测试完成
''')
    
    try:
        # 运行测试
        result = subprocess.run([test_bat], capture_output=True, text=True, timeout=30)
        
        print("返回码:", result.returncode)
        print("标准输出:")
        print(result.stdout)
        
        if result.stderr:
            print("错误输出:")
            print(result.stderr)
        
        # 清理测试文件
        try:
            os.remove(test_bat)
        except:
            pass
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ 测试超时")
        return False
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        return False

def main():
    """主函数"""
    if test_vs2022_environment():
        print("✅ VS2022环境测试成功")
        return True
    else:
        print("❌ VS2022环境测试失败")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)