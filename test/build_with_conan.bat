@echo off
REM Conan Qt6项目构建脚本
echo [Conan Qt6 WebView项目构建]
echo ===============================

echo.
echo 步骤1: 检查Conan安装...
conan --version
if %ERRORLEVEL% NEQ 0 (
    echo Conan未安装，正在安装...
    python -m pip install conan
)

echo.
echo 步骤2: 清理之前的构建...
if exist "build" rmdir /s /q "build"
if exist "bin" rmdir /s /q "bin"
if exist "obj" rmdir /s /q "obj"

echo.
echo 步骤3: 使用Conan安装Qt6...
conan install . --build=missing --update

echo.
echo 步骤4: 使用SCons构建...
scons

echo.
echo 步骤5: 检查构建结果...
if exist "bin\QtWebViewApp.exe" (
    echo ✓ 构建成功！可执行文件: bin\QtWebViewApp.exe
    echo 运行程序: bin\QtWebViewApp.exe
) else (
    echo ✗ 构建失败，请检查错误信息
)

echo.
pause
