@echo off
echo ========================================
echo Qt6 WebEngine Build Script
echo ========================================
echo.

REM Setup VS2022 environment
set VS2022_PATH=D:\Code\VS2022\Community
set VCVARS_PATH=%VS2022_PATH%\VC\Auxiliary\Build\vcvars64.bat

echo Setting up VS2022 environment...
call "%VCVARS_PATH%" -vcvars_ver=14.29

echo.
echo VS2022 environment configured
echo.

REM Setup build directories
if exist obj rmdir /s /q obj
if exist bin rmdir /s /q bin
mkdir obj
mkdir bin

REM Set WebEngine include paths
set WEBENGINE_INCLUDE=-I"C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\webenginewidgets\api" -I"C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\webenginewidgets" -I"C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\core\api" -I"C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\core"

echo Compiling main.cpp...
cl /nologo /c /std:c++20 /utf-8 /W3 /EHsc %WEBENGINE_INCLUDE% src\main.cpp /Foobj\main.obj

echo Compiling mainwindow.cpp...
cl /nologo /c /std:c++20 /utf-8 /W3 /EHsc %WEBENGINE_INCLUDE% src\mainwindow.cpp /Foobj\mainwindow.obj

echo Compiling webviewwidget.cpp...
cl /nologo /c /std:c++20 /utf-8 /W3 /EHsc %WEBENGINE_INCLUDE% src\webviewwidget.cpp /Foobj\webviewwidget.obj

echo Linking program...
link /nologo /subsystem:windows /entry:mainCRTStartup obj\main.obj obj\mainwindow.obj obj\webviewwidget.obj /OUT:bin\Qt6WebViewApp.exe

echo.
echo Build completed!
echo Executable: bin\Qt6WebViewApp.exe

pause