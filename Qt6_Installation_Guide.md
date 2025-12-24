# Qt6 安装指导

## 项目状态
✅ 已完成：
- 创建了简化版Qt6工具栏演示应用（不包含WebEngine）
- 配置了SCons编译脚本
- 分析了Conan Qt6包的问题

⚠️ 当前问题：
- 系统未检测到Qt6安装
- Conan上的Qt6包存在配置问题

## 解决方案

### 方案1：直接安装Qt6（推荐）

#### 1.1 下载Qt6
访问 [Qt官方下载页面](https://www.qt.io/download) 下载Qt6：

**推荐的Qt6版本：**
- Qt 6.5.0 或更新版本
- 选择 "Qt Online Installer for Windows"

#### 1.2 安装选项
在Qt安装器中选择以下组件：

**必需组件：**
- ✅ Qt 6.5.0
  - ✅ MSVC2019 64-bit
  - ✅ Qt WebEngine (用于WebView功能)
  - ✅ Qt SVG (用于图标支持)

**安装路径：**
- 默认路径：`C:\Qt\6.5.0\msvc2019_64\`
- 或 `D:\Qt\6.5.0\msvc2019_64\`

#### 1.3 环境变量配置
安装完成后，添加以下环境变量：

```powershell
# 添加到系统PATH变量
C:\Qt\6.5.0\msvc2019_64\bin
C:\Qt\6.5.0\msvc2019_64\include
```

### 方案2：使用Qt在线安装器自动配置

#### 2.1 下载在线安装器
- 访问：https://www.qt.io/download-qt-installer
- 下载 `qt-unified-windows-x64-[version]-online.exe`

#### 2.2 安装步骤
1. 运行安装器
2. 使用Qt账户登录（或创建免费账户）
3. 选择自定义安装
4. 选择Qt 6.5.0版本
5. 确保勾选：
   - MSVC2019 64-bit
   - Qt WebEngine模块
   - 开发工具

### 方案3：手动环境配置

#### 3.1 如果已安装Qt但未检测到
检查以下路径是否存在：
```powershell
# 检查这些路径是否存在
C:\Qt\6.5.0\msvc2019_64\include\Qt6Core
D:\Qt\6.5.0\msvc2019_64\include\Qt6Core
C:\Qt\6.5.0\msvc2019_64\lib\Qt6Core.lib
D:\Qt\6.5.0\msvc2019_64\lib\Qt6Core.lib
```

#### 3.2 手动设置环境变量
```powershell
# 在系统环境变量中添加
QT_HOME = C:\Qt\6.5.0\msvc2019_64
PATH = %PATH%;%QT_HOME%\bin
```

## 验证安装

### 4.1 运行我们的Qt检测脚本
```powershell
python test\detect_qt_installation.py
```

### 4.2 手动验证
```powershell
# 检查qmake是否可用
qmake --version

# 检查示例
dir "C:\Qt\6.5.0\msvc2019_64\include\Qt6Core"
```

## 编译项目

### 5.1 安装完成后
1. 重新运行Qt检测脚本：
   ```powershell
   python test\detect_qt_installation.py
   ```

2. 编译项目：
   ```powershell
   scons
   ```

3. 运行生成的可执行文件：
   ```powershell
   bin\QtToolbarDemo.exe
   ```

### 5.2 预期结果
如果安装成功，您将看到：
- ✅ 检测到Qt6安装
- ✅ 生成编译配置
- ✅ 成功编译
- ✅ 运行带有工具栏、菜单栏、状态栏的Qt应用

## WebView功能说明

当前的简化版本**不包含WebView功能**，因为：
1. Qt WebEngine需要额外的依赖
2. Conan上的Qt6包有配置问题
3. 本地安装的Qt6可以完美支持WebView

**当Qt6安装完成后**，我们可以轻松添加WebView功能：
- 使用 `QWebEngineView` 组件
- 添加Web导航工具栏
- 支持网页浏览功能

## 故障排除

### 常见问题1：qmake找不到
**解决方案：**
```powershell
# 检查PATH环境变量
echo %PATH%
# 确保包含Qt的bin目录
```

### 常见问题2：链接错误
**解决方案：**
- 确保选择了正确的编译器版本（MSVC2019 64-bit）
- 检查库文件路径配置

### 常见问题3：运行时错误
**解决方案：**
- 确保DLL文件在PATH中或与exe文件同目录
- 运行 `windeployqt` 工具部署依赖

## 下一步

1. **立即行动**：安装Qt6（推荐方案1或方案2）
2. **验证安装**：运行检测脚本
3. **编译项目**：使用SCons编译
4. **测试功能**：运行演示程序
5. **添加WebView**：安装完成后添加WebEngine功能

安装完成后，我们就可以完全实现您最初的需求：**Conan安装Qt6 + 工具栏+WebView + SCons编译**！