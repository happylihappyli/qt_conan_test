"""
SCons 配置 - 使用本地 Qt6 安装
支持 WebEngine 集成
"""

import os
import platform
import shutil
from pathlib import Path

# 本地 Qt6 安装路径配置
LOCAL_QT_PATHS = [
    r"D:\Code\VS2022\Community\Qt6.5.3\6.5.3\msvc2019_64",
    r"D:\Code\VS2022\Community\Qt6.6.2\6.6.2\msvc2019_64",
    r"D:\Code\VS2022\Community\Qt6.7.0\6.7.0\msvc2019_64",
    r"C:\Qt\6.5.3\msvc2019_64",
    r"C:\Qt\6.6.2\msvc2019_64",
    r"C:\Qt\6.7.0\msvc2019_64"
]

def find_local_qt_installation():
    """查找本地 Qt6 安装"""
    for qt_path in LOCAL_QT_PATHS:
        if os.path.exists(qt_path):
            # 检查是否包含 WebEngine
            webengine_path = os.path.join(qt_path, "include", "QtWebEngineWidgets")
            if os.path.exists(webengine_path):
                print(f"[OK] 找到本地 Qt6 安装: {qt_path}")
                return qt_path
    
    print("[WARNING] 未找到本地 Qt6 WebEngine 安装")
    return None

# 查找本地 Qt6
local_qt_path = find_local_qt_installation()

if local_qt_path:
    print(f"[INFO] 使用本地 Qt6: {local_qt_path}")
    
    # 配置本地 Qt6 路径
    qt_include_path = os.path.join(local_qt_path, "include")
    qt_lib_path = os.path.join(local_qt_path, "lib")
    qt_bin_path = os.path.join(local_qt_path, "bin")
    qt_plugins_path = os.path.join(local_qt_path, "plugins")
    
    # WebEngine 特定路径
    webengine_include_path = os.path.join(qt_include_path, "QtWebEngineWidgets")
    webengine_lib_path = qt_lib_path
    webengine_bin_path = qt_bin_path
    
    print(f"[OK] Qt6 头文件路径: {qt_include_path}")
    print(f"[OK] Qt6 库文件路径: {qt_lib_path}")
    print(f"[OK] Qt6 可执行文件路径: {qt_bin_path}")
    print(f"[OK] WebEngine 头文件路径: {webengine_include_path}")
    
else:
    print("[ERROR] 无法找到本地 Qt6 WebEngine 安装")
    print("[INFO] 请安装 Qt6.5.3 或更高版本，确保包含 WebEngine 模块")
    
    # 回退到当前 Conan 配置
    print("[INFO] 回退到当前 Conan 配置...")
    if os.path.exists("SConscript_conandeps"):
        exec(open("SConscript_conandeps").read())
        exit(0)
    else:
        print("[ERROR] 无法找到 SConscript_conandeps 文件")
        exit(1)

# 配置项目结构
project_root = os.path.abspath(".")
src_dir = os.path.join(project_root, "src")
bin_dir = os.path.join(project_root, "bin")
obj_dir = os.path.join(project_root, "obj")

# 创建必要的目录
os.makedirs(bin_dir, exist_ok=True)
os.makedirs(obj_dir, exist_ok=True)

# 查找源代码文件
sources = []
headers = []

for file in os.listdir(src_dir):
    if file.endswith('.cpp'):
        sources.append(os.path.join(src_dir, file))
    elif file.endswith('.h'):
        headers.append(os.path.join(src_dir, file))

print(f"[INFO] 找到 {len(sources)} 个源文件: {sources}")
print(f"[INFO] 找到 {len(headers)} 个头文件: {headers}")

# 创建构建环境
env = Environment()

# 设置编译器选项
env.Append(CXXFLAGS=[
    '/permissive-',     # 启用严格标准一致性
    '-Zc:__cplusplus',  # Qt6要求：确保__cplusplus宏正确设置
    '/std:c++17',       # 使用C++17标准
    '/utf-8',           # UTF-8编码
    '/W3',              # 警告级别3
    '/EHsc',            # 异常处理
    '/MD',              # 多线程DLL运行时
    '/Zi'               # 生成调试信息
])

# 添加包含路径
include_paths = [
    qt_include_path,
    webengine_include_path,
    src_dir
]

# 添加 Qt6 子模块路径
qt_submodules = [
    'QtCore', 'QtGui', 'QtWidgets', 'QtNetwork', 'QtWebEngineCore',
    'QtWebEngineWidgets', 'QtWebChannel', 'QtQml', 'QtQuick'
]

for module in qt_submodules:
    module_path = os.path.join(qt_include_path, module)
    if os.path.exists(module_path):
        include_paths.append(module_path)

env.Append(CPPPATH=include_paths)

# 添加库路径
lib_paths = [qt_lib_path, webengine_lib_path]
env.Append(LIBPATH=lib_paths)

# 配置库文件
qt_libs = [
    'Qt6WebEngineCore', 'Qt6WebEngineWidgets', 'Qt6WebChannel',
    'Qt6Core', 'Qt6Gui', 'Qt6Widgets', 'Qt6Network', 'Qt6Qml', 'Qt6Quick',
    'dwmapi', 'shell32', 'uxtheme', 'advapi32', 'gdi32', 'imm32',
    'ole32', 'oleaut32', 'setupapi', 'shlwapi', 'user32', 'winmm',
    'winspool', 'wtsapi32', 'shcore', 'comdlg32'
]

env.Append(LIBS=qt_libs)

# 添加预处理器定义
env.Append(CPPDEFINES=[
    'UNICODE', '_UNICODE', 'WIN32', '_WINDOWS',
    'QT_WEBCHANNEL_LIB', 'QT_QML_LIB', 'QT_GUI_LIB', 'QT_NETWORK_LIB',
    'QT_WIDGETS_LIB', 'QT_CORE_LIB', 'QT_NO_DEBUG'
])

# 配置MOC（Qt元对象编译器）
print("[INFO] 配置Qt MOC支持...")

# 查找moc可执行文件
moc_exe = os.path.join(qt_bin_path, 'moc.exe')
if os.path.exists(moc_exe):
    print(f"[OK] 找到MOC: {moc_exe}")
    env['MOC'] = moc_exe
    
    # 创建MOC构建器
    def run_moc(target, source, env):
        """运行MOC编译器"""
        cmd = [env['MOC'], '-o', str(target[0]), str(source[0])]
        return env.Execute(env.Action(cmd, '生成MOC文件: $TARGET'))
    
    # 注册MOC构建器
    moc_builder = Builder(action=run_moc, suffix='.moc', src_suffix='.h')
    env['BUILDERS']['MOC'] = moc_builder
    
    # 查找需要MOC的头文件
    moc_headers = []
    for header in headers:
        with open(header, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'Q_OBJECT' in content:
                moc_headers.append(header)
    
    print(f"[OK] 找到 {len(moc_headers)} 个需要MOC的头文件: {moc_headers}")
    
    # 生成MOC文件
    moc_files = []
    for header in moc_headers:
        moc_target = os.path.join(obj_dir, f"{os.path.splitext(os.path.basename(header))[0]}.moc")
        env.MOC(moc_target, header)
        moc_files.append(moc_target)
        
    print(f"[OK] 生成 {len(moc_files)} 个MOC文件: {moc_files}")
else:
    print("[WARNING] 未找到MOC可执行文件")
    moc_files = []

# 编译源文件
print("[INFO] 编译源文件...")
for source in sources:
    source_name = os.path.basename(source)
    obj_name = os.path.splitext(source_name)[0] + '.obj'
    obj_path = os.path.join(obj_dir, 'src', obj_name)
    
    # 确保src子目录存在
    os.makedirs(os.path.dirname(obj_path), exist_ok=True)
    
    # 编译源文件
    env.Object(obj_path, source)
    print(f"[OK] 编译: {source} -> {obj_path}")

# 编译MOC文件成.obj文件
moc_obj_files = []
for moc_file in moc_files:
    if os.path.exists(moc_file):
        # 将MOC文件重命名为.cpp文件以便SCons识别
        moc_cpp_name = os.path.splitext(os.path.basename(moc_file))[0] + '.cpp'
        moc_cpp_path = os.path.join(obj_dir, moc_cpp_name)
        moc_obj_name = os.path.splitext(os.path.basename(moc_file))[0] + '.obj'
        moc_obj_path = os.path.join(obj_dir, moc_obj_name)
        moc_obj_files.append(moc_obj_path)
        
        # 复制MOC文件为.cpp文件
        if not os.path.exists(moc_cpp_path):
            shutil.copy2(moc_file, moc_cpp_path)
            print(f"[OK] 复制MOC文件: {moc_file} -> {moc_cpp_path}")
        
        # 编译MOC .cpp文件
        env.Object(moc_obj_path, moc_cpp_path)
        print(f"[OK] 编译MOC文件: {moc_cpp_path} -> {moc_obj_path}")

# 链接最终可执行文件
all_obj_files = []
for file in os.listdir(os.path.join(obj_dir, 'src')):
    if file.endswith('.obj'):
        all_obj_files.append(os.path.join(obj_dir, 'src', file))

all_obj_files.extend(moc_obj_files)

print(f"[INFO] 链接目标文件: {all_obj_files}")

# 生成最终可执行文件
exe_path = os.path.join(bin_dir, 'QtWebViewApp.exe')
env.Program(exe_path, all_obj_files)

print(f"[OK] 生成可执行文件: {exe_path}")

# 复制Qt6运行时文件
print("[INFO] 复制Qt6运行时文件...")

# 复制DLL文件
for file in os.listdir(qt_bin_path):
    if file.endswith('.dll') and file.startswith('Qt6'):
        src_dll = os.path.join(qt_bin_path, file)
        dst_dll = os.path.join(bin_dir, file)
        if not os.path.exists(dst_dll):
            shutil.copy2(src_dll, dst_dll)
            print(f"[OK] 复制DLL: {file}")

# 复制WebEngine特定DLL
webengine_dlls = [
    'Qt6WebEngineCore.dll',
    'Qt6WebEngineWidgets.dll', 
    'Qt6WebEngineProcess.exe'
]

for dll in webengine_dlls:
    src_path = os.path.join(qt_bin_path, dll)
    if os.path.exists(src_path):
        dst_path = os.path.join(bin_dir, dll)
        if not os.path.exists(dst_path):
            shutil.copy2(src_path, dst_path)
            print(f"[OK] 复制WebEngine DLL: {dll}")

# 复制插件目录
plugins_src = os.path.join(qt_plugins_path)
plugins_dst = os.path.join(bin_dir, 'plugins')

if os.path.exists(plugins_src):
    if os.path.exists(plugins_dst):
        shutil.rmtree(plugins_dst)
    shutil.copytree(plugins_src, plugins_dst)
    print(f"[OK] 复制插件目录: {plugins_dst}")

print("[INFO] 本地Qt6 WebEngine配置完成!")
print(f"[INFO] 可执行文件路径: {exe_path}")
print("[INFO] 运行命令: start " + exe_path)