#!/usr/bin/env pwsh
# -*- coding: utf-8 -*-
"""
使用VS2022编译Qt6 WebEngine项目的PowerShell脚本
"""

param(
    [switch]$Clean,
    [switch]$Verbose
)

# 设置开始时间
$StartTime = Get-Date
Write-Host "[$StartTime] 开始Qt6 WebEngine编译任务" -ForegroundColor Green

# 清理之前的编译结果
if ($Clean) {
    Write-Host "清理之前的编译结果..." -ForegroundColor Yellow
    if (Test-Path "obj") { Remove-Item -Recurse -Force "obj" }
    if (Test-Path "bin") { Remove-Item -Recurse -Force "bin" }
}

# 创建构建目录
New-Item -ItemType Directory -Force -Path "obj" | Out-Null
New-Item -ItemType Directory -Force -Path "bin" | Out-Null

# 设置VS2022环境
Write-Host "设置VS2022编译环境..." -ForegroundColor Yellow
$VS2022Path = "D:\Code\VS2022\Community"
$VCVARSPath = "$VS2022Path\VC\Auxiliary\Build\vcvars64.bat"

if (-not (Test-Path $VCVARSPath)) {
    Write-Error "未找到VCVARS脚本: $VCVARSPath"
    exit 1
}

# 设置环境变量
Write-Host "激活VS2022 x64环境..." -ForegroundColor Cyan
& $VCVARSPath -vcvars_ver=14.29

# 检查编译器是否可用
Write-Host "检查编译器版本..." -ForegroundColor Yellow
try {
    $ClVersion = cl /version 2>&1 | Select-Object -First 1
    Write-Host "CL版本: $ClVersion" -ForegroundColor Green
} catch {
    Write-Error "无法启动编译器"
    exit 1
}

# 设置WebEngine头文件路径
$WebEnginePaths = @(
    "C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\webenginewidgets\api",
    "C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\webenginewidgets",
    "C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\core\api",
    "C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\core",
    "C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\src\webengine",
    "C:\Users\happyli\.conan2\p\qt4048dd8d846aa\s\src\qtwebengine\tools\mkspecs"
)

# 验证路径存在性
$ValidPaths = @()
foreach ($path in $WebEnginePaths) {
    if (Test-Path $path) {
        $ValidPaths += $path
        Write-Host "✓ WebEngine头文件路径: $path" -ForegroundColor Green
    } else {
        Write-Host "✗ 路径不存在: $path" -ForegroundColor Red
    }
}

# 构建包含路径参数
$IncludeArgs = $ValidPaths | ForEach-Object { "/I `"$_`"" }
$IncludeString = $IncludeArgs -join " "

# 设置编译参数
$CompileFlags = "/nologo /c /std:c++20 /utf-8 /W3 /EHsc"
$LinkFlags = "/nologo /subsystem:windows /entry:mainCRTStartup"

Write-Host "开始编译源文件..." -ForegroundColor Yellow

# 编译源文件
$SourceFiles = @(
    @{ Name = "main"; File = "src\main.cpp" },
    @{ Name = "mainwindow"; File = "src\mainwindow.cpp" },
    @{ Name = "webviewwidget"; File = "src\webviewwidget.cpp" }
)

$CompileResults = @()
foreach ($src in $SourceFiles) {
    if (-not (Test-Path $src.File)) {
        Write-Host "✗ 源文件不存在: $($src.File)" -ForegroundColor Red
        $CompileResults += @{ Success = $false; Name = $src.Name }
        continue
    }
    
    Write-Host "编译: $($src.Name)" -ForegroundColor Cyan
    $OutputFile = "obj\$($src.Name).obj"
    
    $Command = "cl $CompileFlags $IncludeString `"$($src.File)`" /Fo$OutputFile"
    
    if ($Verbose) {
        Write-Host "执行: $Command" -ForegroundColor Gray
    }
    
    try {
        $Result = Invoke-Expression $Command 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ 编译成功: $($src.Name)" -ForegroundColor Green
            $CompileResults += @{ Success = $true; Name = $src.Name; Output = $OutputFile }
        } else {
            Write-Host "✗ 编译失败: $($src.Name)" -ForegroundColor Red
            if ($Verbose) {
                $Result | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
            }
            $CompileResults += @{ Success = $false; Name = $src.Name; Error = $Result }
        }
    } catch {
        Write-Host "✗ 编译异常: $($src.Name)" -ForegroundColor Red
        if ($Verbose) {
            Write-Host "  $_" -ForegroundColor Red
        }
        $CompileResults += @{ Success = $false; Name = $src.Name; Error = $_ }
    }
}

# 检查编译结果
$FailedCompiles = $CompileResults | Where-Object { -not $_.Success }
if ($FailedCompiles.Count -gt 0) {
    Write-Host "❌ 有 $($FailedCompiles.Count) 个文件编译失败" -ForegroundColor Red
    exit 1
}

Write-Host "✓ 所有源文件编译成功" -ForegroundColor Green

# 链接程序
Write-Host "链接程序..." -ForegroundColor Yellow
$ObjectFiles = $CompileResults | Where-Object { $_.Success } | ForEach-Object { $_.Output }
$ObjectString = $ObjectFiles -join " "
$OutputExe = "bin\Qt6WebViewApp.exe"

$LinkCommand = "link $LinkFlags $ObjectString /OUT:$OutputExe"

Write-Host "执行: $LinkCommand" -ForegroundColor Cyan

try {
    $LinkResult = Invoke-Expression $LinkCommand 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ 链接成功: $OutputExe" -ForegroundColor Green
        
        # 检查输出文件
        if (Test-Path $OutputExe) {
            $FileSize = (Get-Item $OutputExe).Length
            Write-Host "✓ 可执行文件生成成功: $OutputExe (大小: $FileSize 字节)" -ForegroundColor Green
        }
    } else {
        Write-Host "✗ 链接失败" -ForegroundColor Red
        if ($Verbose) {
            $LinkResult | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
        }
        exit 1
    }
} catch {
    Write-Host "✗ 链接异常: $_" -ForegroundColor Red
    exit 1
}

# 完成任务
$EndTime = Get-Date
$Duration = $EndTime - $StartTime
Write-Host "[$EndTime] Qt6 WebEngine编译任务完成" -ForegroundColor Green
Write-Host "编译耗时: $($Duration.TotalSeconds.ToString('F2')) 秒" -ForegroundColor Cyan
Write-Host "输出文件: $OutputExe" -ForegroundColor Green