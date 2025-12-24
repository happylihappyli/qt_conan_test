# 运行编译脚本
Write-Host "运行WebEngine编译测试..." -ForegroundColor Green

# 切换到项目目录
Set-Location "E:\GitHub3\cpp\qt_conan_test"

# 运行批处理文件
try {
    & ".\test_compile.bat"
} catch {
    Write-Host "运行批处理文件时出错: $_" -ForegroundColor Red
}

Write-Host "编译测试完成" -ForegroundColor Yellow