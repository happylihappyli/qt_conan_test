#!/usr/bin/env python3
import os
import glob

def delete_moc_files():
    """删除所有MOC文件"""
    print("🗑️ 删除现有MOC文件...")
    
    # 查找obj目录中的所有MOC文件
    moc_pattern = "obj/*.moc"
    moc_files = glob.glob(moc_pattern)
    
    deleted_count = 0
    for moc_file in moc_files:
        try:
            if os.path.exists(moc_file):
                os.remove(moc_file)
                print(f"✅ 删除 {moc_file}")
                deleted_count += 1
        except Exception as e:
            print(f"❌ 删除 {moc_file} 失败: {e}")
    
    print(f"📊 总共删除了 {deleted_count} 个MOC文件")
    return deleted_count

if __name__ == "__main__":
    delete_moc_files()