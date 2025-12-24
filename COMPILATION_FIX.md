# Qt6 WebView项目编译问题解决方案

## 问题分析
编译失败的根本原因：**系统中未安装Qt6或Qt6路径配置不正确**

错误信息：`fatal error C1083: 无法打开包括文件: "QtWidgets": No such file or directory`

## 解决方案

### 方案一：安装Qt6 (推荐)

#### 1. 下载Qt6
- 访问：https://www.qt.io/download
- 选择 "Qt Online Installer for Windows"
- 或直接下载：https://download.qt.io/online_installers/

#### 2. 安装选项 (重要!)
在Qt安装向导中**必须**选择以下组件：
- ✅ Qt 6.5.x (或更新版本)
- ✅ **Qt WebEngine** (在"Qt > Additional Libraries"中)
- ✅ MSVC 2019 64-bit
- ✅ CMake Tools
- ✅ Ninja (可选)

**关键提示**: Qt WebEngine是必需的，不要遗漏！

#### 3. 推荐安装路径
```
D:\Qt\6.5.0\msvc2019_64
```

#### 4. 环境变量设置
安装完成后设置环境变量：
```cmd
set QTDIR=D:\Qt\6.5.0\msvc2019_64
set PATH=%QTDIR%\bin;%PATH%
set QT_PLUGIN_PATH=%QTDIR%\plugins
```

### 方案二：使用Visual Studio 2022的Qt扩展

如果您使用Visual Studio 2022：
1. 打开Visual Studio 2022
2. 转到"扩展" > "管理扩展"
3. 搜索并安装"Qt Visual Studio Tools"
4. 通过VS2022的Qt项目管理器安装Qt6

### 方案三：创建虚拟环境编译 (仅演示)

如果暂时无法安装Qt6，可以创建模拟环境进行演示：

```cmd
# 创建Qt6目录结构 (仅演示)
mkdir D:\Qt\6.5.0\msvc2019_64\include\Qt6
mkdir D:\Qt\6.5.0\msvc2019_64\include\Qt6Core
mkdir D:\Qt\6.5.0\msvc2019_64\include\Qt6Widgets
mkdir D:\Qt\6.5.0\msvc2019_64\include\Qt6Gui
mkdir D:\Qt\6.5.0\msvc2019_64\include\Qt6WebEngineWidgets
mkdir D:\Qt\6.5.0\msvc2019_64\lib
mkdir D:\Qt\6.5.0\msvc2019_64\bin
```

**注意**: 这只是创建目录结构，不会真正解决编译问题，需要实际安装Qt6。

## 修复步骤

### 1. 安装Qt6后执行：
```cmd
# 设置环境变量
setup_qt_env.bat

# 重新编译
scons
```

### 2. 备选编译方案 (CMake)
如果SCons仍有问题，使用CMake：
```cmd
# 创建构建目录
mkdir build && cd build

# 配置项目
cmake .. -G "Visual Studio 16 2019" -A x64

# 编译
cmake --build . --config Release

# 运行
..\bin\QtWebViewApp.exe
```

### 3. Visual Studio直接编译
如果您有Visual Studio项目经验：
1. 打开Visual Studio 2019/2022
2. 创建新项目 > "Qt Widgets Application"
3. 复制源代码文件
4. 配置Qt6路径
5. 编译运行

## 常见问题

### Q: 安装了Qt6但仍然找不到头文件？
A: 检查Qt6安装路径是否正确，确保选择了WebEngine组件

### Q: 出现"access denied"错误？
A: 确保没有其他程序使用Qt6库文件，关闭相关进程后重试

### Q: WebEngine不工作？
A: 确保安装了完整的Qt WebEngine组件，不只是Qt6基础包

## 验证安装

运行以下命令验证Qt6安装：
```cmd
qmake --version
```

应该显示类似：
```
QMake version 3.1
Using Qt version 6.5.0 in D:\Qt\6.5.0\msvc2019_64\lib
```

## 下一步
安装Qt6后，重新运行：
```cmd
python test/verify_project.py
python test/completion_tts.py
```

然后尝试编译：
```cmd
scons
```