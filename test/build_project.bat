@echo off
REM Qt6工具栏+WebView项目构建脚本
REM 支持自动检测Qt安装并编译项目

echo ========================================
echo Qt6工具栏+WebView项目构建脚本
echo ========================================
echo.

REM 检查当前目录
if not exist "src\main.cpp" (
    echo 错误: 未找到src\main.cpp，请确保在项目根目录运行此脚本
    pause
    exit /b 1
)

echo 步骤1: 检测Qt安装...
python test\detect_qt_installation.py
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Qt安装检测失败！
    echo 请按照Qt6_Installation_Guide.md中的指导安装Qt6
    echo 安装完成后重新运行此脚本
    pause
    exit /b 1
)

echo.
echo 步骤2: 编译项目...
scons
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  编译失败！
    echo 请检查错误信息并确保Qt6正确安装
    pause
    exit /b 1
)

echo.
echo 步骤3: 验证构建结果...
if exist "bin\QtToolbarDemo.exe" (
    echo ✅ 构建成功！
    echo.
    echo 生成的文件:
    echo   - bin\QtToolbarDemo.exe (主程序)
    echo.
    echo 运行程序:
    echo   bin\QtToolbarDemo.exe
    echo.
    echo 程序功能:
    echo   ✓ 工具栏演示
    echo   ✓ 菜单栏 (文件/编辑/帮助)
    echo   ✓ 状态栏
    echo   ✓ 文本编辑功能
    echo   ✓ 按钮交互
    echo.
    echo 要运行程序吗？(Y/N)
    set /p choice="输入选择: "
    if /i "%choice%"=="Y" (
        echo 启动Qt6工具栏演示程序...
        bin\QtToolbarDemo.exe
    )
) else (
    echo ⚠️  未找到生成的可执行文件
    echo 请检查编译过程是否有错误
)

echo.
echo ========================================
echo 项目构建完成！
echo ========================================
pause