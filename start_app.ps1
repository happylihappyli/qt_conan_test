# 设置PowerShell控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8

# 设置环境变量
$OutputEncoding = [System.Text.Encoding]::UTF8

# 启动应用程序
Write-Host "启动Qt6 WebView应用程序..." -ForegroundColor Green
Write-Host "编码设置: UTF-8" -ForegroundColor Cyan

.\bin\QtWebViewApp.exe