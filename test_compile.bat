@echo off
cd /d "E:\GitHub3\cpp\qt_conan_test"
echo Setting up VS2022 environment...
call "D:\Code\VS2022\Community\VC\Auxiliary\Build\vcvars64.bat" -vcvars_ver=14.29
echo VS2022 environment activated
echo.
echo Checking Qt WebEngine headers...
dir "C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\webenginewidgets\api"
echo.
echo Starting compilation...
set INCLUDE=-I"C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\webenginewidgets\api" -I"C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\webenginewidgets"
echo Compiling main.cpp...
cl /nologo /c /std:c++20 /utf-8 /W3 /EHsc %INCLUDE% src\main.cpp /Foobj\main.obj
if %errorlevel% neq 0 goto :error
echo Compiling mainwindow.cpp...
cl /nologo /c /std:c++20 /utf-8 /W3 /EHsc %INCLUDE% src\mainwindow.cpp /Foobj\mainwindow.obj
if %errorlevel% neq 0 goto :error
echo Compiling webviewwidget.cpp...
cl /nologo /c /std:c++20 /utf-8 /W3 /EHsc %INCLUDE% src\webviewwidget.cpp /Foobj\webviewwidget.obj
if %errorlevel% neq 0 goto :error
echo.
echo Linking...
link /nologo /subsystem:windows /entry:mainCRTStartup obj\main.obj obj\mainwindow.obj obj\webviewwidget.obj /OUT:bin\Qt6WebViewApp.exe
if %errorlevel% neq 0 goto :error
echo.
echo Compilation successful!
echo Generated: bin\Qt6WebViewApp.exe
goto :end
:error
echo.
echo Compilation failed!
echo Check the error messages above.
exit /b 1
:end
pause