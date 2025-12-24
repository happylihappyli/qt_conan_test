# Qt6 Conan 编译磁盘空间不足解决方案

## 问题分析
Conan编译Qt6需要大量磁盘空间（约5-10GB），当前遇到"No space left on device"错误。

## 磁盘空间状态
- C盘: ~275GB (空间可能不足)
- D盘: ~58GB 可用空间
- E盘: ~12GB 可用空间
- F盘: ~53GB 可用空间

## 解决方案

### 方案1: 清理磁盘空间
清理临时文件和不需要的文件以释放更多空间。

### 方案2: 使用其他盘符进行Conan构建
将Conan缓存目录移动到有足够空间的盘符：
```bash
# 设置Conan使用F盘（~53GB空间）
export CONAN_USER_HOME=F:/conan_cache
conan install . --build=missing --update --profile:host=qt6_profile --profile:build=qt6_profile
```

### 方案3: 使用预编译Qt6二进制包
避免从源码编译，直接使用预编译的Qt6包：
```bash
# 使用shared库版本，减小磁盘占用
conan install qt/6.7.3@ -o qt:shared=True -o qt:qtwebengine=False
```

### 方案4: 最小化Qt6配置
只安装必需的Qt6模块：
```bash
# 只安装Core, Widgets, GUI模块
conan install qt/6.7.3@ -o qt:qtdeclarative=False -o qt:qtwebchannel=False -o qt:qtwebengine=False
```

### 方案5: 混合方案 - 本地Qt6 + Conan
使用本地Qt6安装 + Conan管理的其他依赖：
1. 下载并安装Qt6官方版本
2. 只用Conan管理非Qt依赖

## 推荐方案
建议使用**方案3（预编译二进制包）**或**方案5（混合方案）**，这样可以避免编译耗时和磁盘空间问题。