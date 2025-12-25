# -*- coding: utf-8 -*-
"""
SConstruct 文件 - 配置Qt6项目的scons编译环境
支持Conan依赖管理，Qt6工具栏和WebView应用
"""

import os
import time
import shutil
from pathlib import Path

# 导入SCons必要组件
import SCons
from SCons.Script import Environment, SConscript, Default, Exit

# 显示编译开始时间
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 开始编译Qt6工具栏+WebView项目")

# 设置项目根目录
project_root = os.path.abspath('.')
src_dir = os.path.join(project_root, 'src')
bin_dir = os.path.join(project_root, 'bin')
obj_dir = os.path.join(project_root, 'obj')

# 确保输出目录存在
os.makedirs(bin_dir, exist_ok=True)
os.makedirs(obj_dir, exist_ok=True)

# 配置Qt5依赖（使用预安装的Qt5.14.2）
print("[INFO] 使用预安装的Qt5.14.2配置")

# 设置Qt5.14.2路径
qt_base_path = r'D:\Code\Qt\Qt5.14.2\5.14.2\msvc2017_64'
qt_include_path = os.path.join(qt_base_path, 'include')
qt_lib_path = os.path.join(qt_base_path, 'lib')
qt_bin_path = os.path.join(qt_base_path, 'bin')

# 编译器环境配置
env = Environment()

# 设置UTF-8编码和中文支持
env.Append(CPPFLAGS=['-DUNICODE', '-D_UNICODE'])
env.Append(CPPFLAGS=['-utf-8'])  # GCC/Clang编译器
env.Append(CPPFLAGS=['/utf-8'])  # MSVC编译器

# 手动配置Qt MOC工具
moc_path = os.path.join(qt_bin_path, 'moc.exe')
if os.path.exists(moc_path):
    env['MOC'] = moc_path
    print(f"[OK] MOC工具路径: {moc_path}")
    
    # 创建MOC构建器，使用完整的路径命令
    def moc_builder_action(target, source, env):
        import subprocess
        import os
        tgt = str(target[0])
        src = str(source[0])
        cmd = f'"{moc_path}" -o "{tgt}" "{src}"'
        print(f"Running MOC: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"MOC Error: {result.stderr}")
            return result.returncode
        return 0
    
    # 创建MOC构建器
    moc_builder = env.Builder(
        action=moc_builder_action,
        suffix='.cpp',
        src_suffix='.h'
    )
    env.Append(BUILDERS={'MOC': moc_builder})
else:
    print(f"[ERROR] MOC工具不存在: {moc_path}")

# 添加Qt5路径到环境
if os.path.exists(qt_include_path):
    # 添加Qt5主include目录和各个模块目录
    env.Append(CPPPATH=[qt_include_path])
    print(f"[OK] 添加Qt5主头文件路径: {qt_include_path}")
    
    # 添加各个模块的include路径
    qt_modules = ['QtCore', 'QtWidgets', 'QtGui', 'QtNetwork', 'QtWebChannel', 
                  'QtWebEngine', 'QtWebEngineCore', 'QtWebEngineWidgets']
    for module in qt_modules:
        module_path = os.path.join(qt_include_path, module)
        if os.path.exists(module_path):
            env.Append(CPPPATH=[module_path])
            print(f"[OK] 添加Qt5模块头文件路径: {module_path}")

if os.path.exists(qt_lib_path):
    env.Append(LIBPATH=[qt_lib_path])
    print(f"[OK] 添加Qt5库文件路径: {qt_lib_path}")

if os.path.exists(qt_bin_path):
    env.Append(BINPATH=[qt_bin_path])
    print(f"[OK] 添加Qt5可执行文件路径: {qt_bin_path}")
    # 打印MOC路径用于调试
    moc_path = os.path.join(qt_bin_path, 'moc.exe')
    print(f"  - MOC路径: {moc_path}")

# 设置基本Qt5库
qt_libs = [
    'Qt5Core', 'Qt5Widgets', 'Qt5Gui', 'Qt5WebEngineWidgets', 
    'Qt5WebEngineCore', 'Qt5WebChannel', 'Qt5Network'
]

qt_defines = ['QT_CORE_LIB', 'QT_WIDGETS_LIB', 'QT_GUI_LIB', 
              'QT_WEBENGINEWIDGETS_LIB', 'QT_WEBENGINECORE_LIB', 
              'QT_WEBCHANNEL_LIB', 'QT_NETWORK_LIB', 'UNICODE', '_UNICODE']

# 应用Qt5配置
env.Append(LIBS=qt_libs)
env.Append(CPPDEFINES=qt_defines)

# 设置C++标准和编译选项 (VS2022使用C++17标准，这里的qt版本，导致不能用新版本的c++23)
# 强制使用MSVC编译选项（Windows平台）
env.Append(CXXFLAGS=['/std:c++17', '/Zc:__cplusplus'])

# 设置Release构建配置
env.Append(CXXFLAGS=['/O2', '/MD', '/DNDEBUG'])
env.Append(CPPDEFINES=['QT_NO_DEBUG'])
print("[INFO] 使用MSVC编译器选项，C++17标准")
print("[INFO] 使用Release构建配置")

# 设置输出目录
env['OBJDIR'] = obj_dir
env['BINDIR'] = bin_dir

# 查找源代码文件
source_files = []
for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(('.cpp', '.cxx', '.cc')):
            source_files.append(os.path.join(root, file))

print(f"[INFO] 找到 {len(source_files)} 个源文件")

# 查找头文件用于MOC处理
header_files = []
for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(('.h', '.hpp')):
            header_files.append(os.path.join(root, file))

print(f"[INFO] 找到 {len(header_files)} 个头文件")

# 生成MOC文件并添加到源文件列表
moc_files = []

for header_file in header_files:
    # 检查是否包含Q_OBJECT宏（需要MOC处理）
    with open(header_file, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'Q_OBJECT' in content:
            # 生成MOC文件名
            base_name = os.path.splitext(os.path.basename(header_file))[0]
            moc_file = os.path.join(obj_dir, f'moc_{base_name}.cpp')
            moc_files.append(moc_file)
            
            # 添加MOC构建规则
            env.MOC(moc_file, header_file)
            print(f"[OK] 为 {os.path.basename(header_file)} 生成MOC: {moc_file}")

# 添加MOC文件到源文件列表
all_sources = source_files + moc_files

# 添加MOC文件到源文件列表
all_sources = source_files + moc_files

# 设置输出程序名
program_name = 'test'
program_target = os.path.join(bin_dir, program_name + env['PROGSUFFIX'])

# 构建程序
program = env.Program(target=program_target, source=all_sources)

# 设置默认目标
Default(program)

# 打印编译信息
print(f"[INFO] 程序将输出到: {program_target}")
print(f"[INFO] 目标程序名: {program_name}")

# 显示编译结束时间
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 编译配置完成")