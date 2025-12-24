@echo off
echo ========================================
echo WebEngine编译批处理文件
echo ========================================
echo.

REM 设置VS2022环境
set VS2022_PATH=D:\Code\VS2022\Community
set VCVARS_PATH=%VS2022_PATH%\VC\Auxiliary\Build\vcvars64.bat

echo 设置VS2022环境...
call "%VCVARS_PATH%" -vcvars_ver=14.29

echo.
echo VS2022环境已设置
echo CL版本: 
cl /version

echo.
echo 编译项目...

REM 清理之前的编译结果
if exist obj rmdir /s /q obj
if exist bin rmdir /s /q bin
mkdir obj
mkdir bin

REM 设置WebEngine头文件路径
set WEBENGINE_INCLUDE_PATHS=-I"C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\webenginewidgets\api" -I"C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\webenginewidgets" -I"C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\core\api" -I"C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\core"

REM 编译main.cpp
echo 编译main.cpp...
cl /nologo /c /std:c++17 /utf-8 /W3 /EHsc %WEBENGINE_INCLUDE_PATHS% src\main.cpp /Foobj\main.obj

echo.
echo 编译mainwindow.cpp...
cl /nologo /c /std:c++17 /utf-8 /W3 /EHsc %WEBENGINE_INCLUDE_PATHS% src\mainwindow.cpp /Foobj\mainwindow.obj

echo.
echo 编译webviewwidget.cpp...
cl /nologo /c /std:c++17 /utf-8 /W3 /EHsc %WEBENGINE_INCLUDE_PATHS% src\webviewwidget.cpp /Foobj\webviewwidget.obj

echo.
echo 链接程序...
link /nologo /subsystem:windows /entry:mainCRTStartup obj\main.obj obj\mainwindow.obj obj\webviewwidget.obj /OUT:bin\Qt6WebViewApp.exe

echo.
echo 编译完成！
echo 可执行文件位置: bin\Qt6WebViewApp.exe

pause