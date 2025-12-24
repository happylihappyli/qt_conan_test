@echo off
chcp 65001 > nul
setlocal
echo @echo off > "%~dp0/deactivate_conanbuildenv-release-x86_64.bat"
echo echo Restoring environment >> "%~dp0/deactivate_conanbuildenv-release-x86_64.bat"
for %%v in (QT_PLUGIN_PATH QT_HOST_PATH) do (
    set foundenvvar=
    for /f "delims== tokens=1,2" %%a in ('set') do (
        if /I "%%a" == "%%v" (
            echo set "%%a=%%b">> "%~dp0/deactivate_conanbuildenv-release-x86_64.bat"
            set foundenvvar=1
        )
    )
    if not defined foundenvvar (
        echo set %%v=>> "%~dp0/deactivate_conanbuildenv-release-x86_64.bat"
    )
)
endlocal


set "QT_PLUGIN_PATH=C:\Users\happyli\.conan2\p\b\qtb73b254637aeb\p\plugins"
set "QT_HOST_PATH=C:\Users\happyli\.conan2\p\b\qtb73b254637aeb\p"