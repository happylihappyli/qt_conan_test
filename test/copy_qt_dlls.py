# -*- coding: utf-8 -*-
"""
复制Qt DLL到bin目录
"""
import os
import shutil
import sys

def copy_qt_dlls():
    """
    复制Qt所需的DLL到bin目录
    """
    # Qt5.14.2的bin目录
    qt_bin_path = r"D:\Code\Qt\Qt5.14.2\5.14.2\msvc2017_64\bin"
    
    # Qt5.14.2的资源目录
    qt_resources_path = r"D:\Code\Qt\Qt5.14.2\5.14.2\msvc2017_64\resources"
    
    # Qt5.14.2的翻译目录
    qt_translations_path = r"D:\Code\Qt\Qt5.14.2\5.14.2\msvc2017_64\translations"
    
    # Qt5.14.2的插件目录
    qt_plugins_path = r"D:\Code\Qt\Qt5.14.2\5.14.2\msvc2017_64\plugins"
    
    # 目标bin目录
    target_bin_path = r"E:\GitHub3\cpp\qt_conan_test\bin"
    
    # 需要复制的DLL列表
    required_dlls = [
        "Qt5Core.dll",
        "Qt5Widgets.dll",
        "Qt5Gui.dll",
        "Qt5WebEngineWidgets.dll",
        "Qt5WebEngineCore.dll",
        "Qt5WebEngine.dll",
        "Qt5WebChannel.dll",
        "Qt5Network.dll",
        "Qt5Quick.dll",
        "Qt5Qml.dll",
        "Qt5Positioning.dll",
        "Qt5PrintSupport.dll",
        "Qt5Svg.dll",
        "libEGL.dll",
        "libGLESv2.dll",
        "opengl32sw.dll",
        "d3dcompiler_47.dll"
    ]
    
    # 需要复制的WebEngine进程文件
    required_exe = [
        "QtWebEngineProcess.exe"
    ]
    
    # 需要复制的资源目录
    required_resources = [
        "qtwebengine_resources.pak",
        "qtwebengine_resources_100p.pak",
        "qtwebengine_resources_200p.pak",
        "icudtl.dat"
    ]
    
    print("=" * 60)
    print("复制Qt DLL到bin目录")
    print("=" * 60)
    
    if not os.path.exists(qt_bin_path):
        print(f"[ERROR] Qt bin目录不存在: {qt_bin_path}")
        return False
    
    if not os.path.exists(target_bin_path):
        print(f"[ERROR] 目标bin目录不存在: {target_bin_path}")
        return False
    
    copied_count = 0
    for dll_name in required_dlls:
        src_path = os.path.join(qt_bin_path, dll_name)
        dst_path = os.path.join(target_bin_path, dll_name)
        
        if os.path.exists(src_path):
            # 如果目标文件已存在，先删除
            if os.path.exists(dst_path):
                os.remove(dst_path)
            
            # 复制文件
            shutil.copy2(src_path, dst_path)
            print(f"[OK] 复制: {dll_name}")
            copied_count += 1
        else:
            print(f"[WARN] 未找到: {dll_name}")
    
    # 复制WebEngine进程文件
    print("\n" + "=" * 60)
    print("复制WebEngine进程文件")
    print("=" * 60)
    for exe_name in required_exe:
        src_path = os.path.join(qt_bin_path, exe_name)
        dst_path = os.path.join(target_bin_path, exe_name)
        
        if os.path.exists(src_path):
            if os.path.exists(dst_path):
                os.remove(dst_path)
            shutil.copy2(src_path, dst_path)
            print(f"[OK] 复制: {exe_name}")
            copied_count += 1
        else:
            print(f"[WARN] 未找到: {exe_name}")
    
    # 复制资源文件
    print("\n" + "=" * 60)
    print("复制WebEngine资源文件")
    print("=" * 60)
    for resource_name in required_resources:
        src_path = os.path.join(qt_resources_path, resource_name)
        dst_path = os.path.join(target_bin_path, resource_name)
        
        if os.path.exists(src_path):
            if os.path.exists(dst_path):
                os.remove(dst_path)
            shutil.copy2(src_path, dst_path)
            print(f"[OK] 复制: {resource_name}")
            copied_count += 1
        else:
            print(f"[WARN] 未找到: {resource_name}")
    
    # 创建QtWebEngine进程目录
    print("\n" + "=" * 60)
    print("创建WebEngine进程目录")
    print("=" * 60)
    webengine_process_dir = os.path.join(target_bin_path, "QtWebEngineProcess.exe")
    if os.path.exists(webengine_process_dir):
        print(f"[OK] WebEngine进程文件已存在")
    else:
        print(f"[WARN] WebEngine进程文件不存在")
    
    # 复制平台插件
    print("\n" + "=" * 60)
    print("复制平台插件")
    print("=" * 60)
    
    # 创建platforms目录
    platforms_dir = os.path.join(target_bin_path, "platforms")
    os.makedirs(platforms_dir, exist_ok=True)
    
    # 复制qwindows.dll
    qwindows_src = os.path.join(qt_plugins_path, "platforms", "qwindows.dll")
    qwindows_dst = os.path.join(platforms_dir, "qwindows.dll")
    
    if os.path.exists(qwindows_src):
        if os.path.exists(qwindows_dst):
            os.remove(qwindows_dst)
        shutil.copy2(qwindows_src, qwindows_dst)
        print(f"[OK] 复制: qwindows.dll")
        copied_count += 1
    else:
        print(f"[WARN] 未找到: qwindows.dll")
    
    # 复制WebEngine相关插件
    print("\n" + "=" * 60)
    print("复制WebEngine相关插件")
    print("=" * 60)
    
    # 创建qtwebengine目录
    qtwebengine_dir = os.path.join(target_bin_path, "qtwebengine")
    os.makedirs(qtwebengine_dir, exist_ok=True)
    
    # 复制qtwebengine_resources_100p.pak（已经在资源文件中复制）
    # 创建qt.conf配置文件
    qt_conf_path = os.path.join(target_bin_path, "qt.conf")
    qt_conf_content = "[Paths]\nPlugins=plugins\n"
    with open(qt_conf_path, 'w', encoding='utf-8') as f:
        f.write(qt_conf_content)
    print(f"[OK] 创建: qt.conf")
    
    # 复制imageformats插件
    print("\n" + "=" * 60)
    print("复制图片格式插件")
    print("=" * 60)
    
    imageformats_dir = os.path.join(target_bin_path, "imageformats")
    os.makedirs(imageformats_dir, exist_ok=True)
    
    image_plugins = [
        "qjpeg.dll",
        "qsvg.dll",
        "qico.dll",
        "qgif.dll"
    ]
    
    for plugin in image_plugins:
        src_path = os.path.join(qt_plugins_path, "imageformats", plugin)
        dst_path = os.path.join(imageformats_dir, plugin)
        
        if os.path.exists(src_path):
            if os.path.exists(dst_path):
                os.remove(dst_path)
            shutil.copy2(src_path, dst_path)
            print(f"[OK] 复制: {plugin}")
            copied_count += 1
        else:
            print(f"[WARN] 未找到: {plugin}")
    
    # 复制printsupport插件
    print("\n" + "=" * 60)
    print("复制打印支持插件")
    print("=" * 60)
    
    printsupport_dir = os.path.join(target_bin_path, "printsupport")
    os.makedirs(printsupport_dir, exist_ok=True)
    
    windowsprint_src = os.path.join(qt_plugins_path, "printsupport", "windowsprintersupport.dll")
    windowsprint_dst = os.path.join(printsupport_dir, "windowsprintersupport.dll")
    
    if os.path.exists(windowsprint_src):
        if os.path.exists(windowsprint_dst):
            os.remove(windowsprint_dst)
        shutil.copy2(windowsprint_src, windowsprint_dst)
        print(f"[OK] 复制: windowsprintersupport.dll")
        copied_count += 1
    else:
        print(f"[WARN] 未找到: windowsprintersupport.dll")
    
    print("=" * 60)
    print(f"共复制 {copied_count} 个文件")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = copy_qt_dlls()
    if success:
        print("[OK] DLL复制完成！")
        sys.exit(0)
    else:
        print("[ERROR] DLL复制失败！")
        sys.exit(1)