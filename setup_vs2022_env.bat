@echo off
echo 配置Visual Studio 2022环境...

REM 设置VS2022路径
set VS2022_PATH=D:\Code\VS2022\Community

REM 激活VS2022环境
call "%VS2022_PATH%\VC\Auxiliary\Build\vcvars64.bat" -vcvars_ver=14.29

REM 显示环境信息
echo 设置PATH环境变量...
echo INCLUDE=%INCLUDE%
echo LIB=%LIB%
echo LIBPATH=%LIBPATH%

REM 执行后续命令
%*
