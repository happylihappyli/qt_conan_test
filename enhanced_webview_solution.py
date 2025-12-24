# -*- coding: utf-8 -*-
"""
增强WebView解决方案
提供多种Web浏览功能的替代实现
"""

import os
import shutil
from pathlib import Path

def create_enhanced_webview():
    """创建增强版WebViewWidget，支持更多功能"""
    
    print("🔧 创建增强版WebViewWidget...")
    
    # 备份当前文件
    for file in ["src/webviewwidget.h", "src/webviewwidget.cpp"]:
        if os.path.exists(file):
            backup_name = f"{file}.qtbrowser_backup"
            shutil.copy2(file, backup_name)
            print(f"  ✅ 备份: {file} -> {backup_name}")
    
    # 创建增强版头文件
    enhanced_header = '''#pragma once

#include <QWidget>
#include <QVBoxLayout>
#include <QToolBar>
#include <QAction>
#include <QLineEdit>
#include <QPushButton>
#include <QLabel>
#include <QProgressBar>
#include <QTextBrowser>
#include <QUrl>
#include <QString>
#include <QStringList>
#include <QFile>
#include <QTextStream>
#include <QFileInfo>
#include <QDir>
#include <QMessageBox>
#include <QClipboard>
#include <QApplication>
#include <QDesktopServices>
#include <QDebug>

class WebViewWidget : public QWidget
{
    Q_OBJECT

public:
    explicit WebViewWidget(QWidget *parent = nullptr);
    ~WebViewWidget() = default;

signals:
    void urlChanged(const QString &url);
    void titleChanged(const QString &title);
    void loadStarted();
    void loadProgress(int progress);
    void loadFinished(bool ok);

public slots:
    void loadUrl(const QString &url);
    void setHtml(const QString &html, const QString &baseUrl = QString());
    void showOfflinePage();
    void showErrorPage(const QString &url);
    void showWelcomePage();
    void copyUrl();
    void openInDefaultBrowser();

private slots:
    void onAnchorClicked(const QUrl &url);

private:
    void setupUI();
    void setupConnections();
    QString loadTemplateFile(const QString &templateName);
    void createErrorHtml(const QString &url, const QString &error);
    void createWelcomeHtml();
    void createOfflineHtml();

    QVBoxLayout *m_layout;
    QTextBrowser *m_textBrowser;
    QProgressBar *m_progressBar;
    QLabel *m_statusLabel;
    QString m_currentUrl;
    QString m_currentTitle;
}'''
    
    # 创建增强版实现文件
    enhanced_implementation = '''#include "webviewwidget.h"
#include <QStandardPaths>
#include <QWebEngineView>  // 为将来升级准备
#include <QWebEnginePage>  // 为将来升级准备

WebViewWidget::WebViewWidget(QWidget *parent)
    : QWidget(parent)
    , m_layout(nullptr)
    , m_textBrowser(nullptr)
    , m_progressBar(nullptr)
    , m_statusLabel(nullptr)
{
    setupUI();
    setupConnections();
    showWelcomePage();
}

void WebViewWidget::setupUI()
{
    m_layout = new QVBoxLayout(this);
    m_layout->setContentsMargins(5, 5, 5, 5);
    m_layout->setSpacing(5);

    // 进度条
    m_progressBar = new QProgressBar(this);
    m_progressBar->setVisible(false);
    m_layout->addWidget(m_progressBar);

    // 文本浏览器
    m_textBrowser = new QTextBrowser(this);
    m_textBrowser->setOpenExternalLinks(true);
    m_textBrowser->setOpenLinks(true);
    m_layout->addWidget(m_textBrowser);

    // 状态标签
    m_statusLabel = new QLabel("就绪", this);
    m_statusLabel->setStyleSheet("QLabel { color: gray; font-size: 12px; }");
    m_layout->addWidget(m_statusLabel);

    setLayout(m_layout);
}

void WebViewWidget::setupConnections()
{
    // 连接文本浏览器信号
    connect(m_textBrowser, &QTextBrowser::sourceChanged, this, [this](const QUrl &url) {
        m_currentUrl = url.toString();
        emit urlChanged(m_currentUrl);
    });
}

void WebViewWidget::loadUrl(const QString &url)
{
    qDebug() << "尝试加载URL:" << url;
    
    // 清理URL
    QString cleanUrl = url.trimmed();
    if (!cleanUrl.isEmpty()) {
        // 如果没有协议，添加http://
        if (!cleanUrl.startsWith("http://") && !cleanUrl.startsWith("https://") && 
            !cleanUrl.startsWith("file://") && !cleanUrl.startsWith("data:")) {
            cleanUrl = "http://" + cleanUrl;
        }
    }
    
    // 检查URL类型
    QUrl qurl(cleanUrl);
    
    if (qurl.scheme() == "file") {
        // 本地文件
        loadFile(cleanUrl);
    } else if (qurl.scheme() == "http" || qurl.scheme() == "https") {
        // 网络URL - 显示错误页面而不是加载失败
        showErrorPage(cleanUrl);
    } else if (cleanUrl.startsWith("data:")) {
        // 数据URL
        setHtml(cleanUrl.mid(5));
    } else {
        // 其他情况，显示错误页面
        showErrorPage(cleanUrl);
    }
}

void WebViewWidget::setHtml(const QString &html, const QString &baseUrl)
{
    qDebug() << "设置HTML内容";
    m_progressBar->setVisible(false);
    m_statusLabel->setText("已加载HTML内容");
    
    m_textBrowser->setHtml(html, QUrl(baseUrl));
}

void WebViewWidget::showWelcomePage()
{
    QString welcomeHtml = R"(<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>欢迎使用 Qt6 浏览器</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            text-align: center;
            max-width: 600px;
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .features {
            text-align: left;
            margin: 30px 0;
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
        }
        .feature {
            margin: 10px 0;
            padding: 8px 0;
        }
        .feature::before {
            content: "✓ ";
            color: #4CAF50;
            font-weight: bold;
        }
        .demo-links {
            margin-top: 30px;
        }
        .demo-link {
            display: inline-block;
            margin: 10px;
            padding: 12px 24px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            transition: all 0.3s ease;
        }
        .demo-link:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        .note {
            margin-top: 30px;
            padding: 20px;
            background: rgba(255, 193, 7, 0.2);
            border-radius: 10px;
            border-left: 4px solid #FFC107;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 欢迎使用 Qt6 浏览器</h1>
        <p>这是一个基于Qt6开发的轻量级浏览器演示程序</p>
        
        <div class="features">
            <h3>🎯 主要功能</h3>
            <div class="feature">工具栏导航控制</div>
            <div class="feature">地址栏输入</div>
            <div class="feature">本地HTML文件浏览</div>
            <div class="feature">进度条显示</div>
            <div class="feature">右键菜单功能</div>
            <div class="feature">UTF-8编码支持</div>
        </div>
        
        <div class="demo-links">
            <h3>📄 演示内容</h3>
            <a href="data:text/html;charset=utf-8,<h1>这是一个数据URL示例</h1><p>可以直接在地址栏输入 data: 开头的内容</p>" class="demo-link">数据URL示例</a>
            <a href="file://" class="demo-link">本地文件</a>
        </div>
        
        <div class="note">
            <strong>💡 使用提示:</strong><br>
            • 在地址栏输入本地HTML文件路径<br>
            • 输入 data: 开头的内容查看数据URL<br>
            • 网络URL将在未来版本中支持完整WebEngine
        </div>
    </div>
</body>
</html>)";
    
    setHtml(welcomeHtml);
    m_currentTitle = "欢迎使用 Qt6 浏览器";
    emit titleChanged(m_currentTitle);
}

void WebViewWidget::showOfflinePage()
{
    QString offlineHtml = R"(<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>离线模式</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 40px;
            background: #f5f5f5;
            color: #333;
            text-align: center;
        }
        .offline-container {
            max-width: 500px;
            margin: 50px auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .offline-icon {
            font-size: 4em;
            margin-bottom: 20px;
        }
        h1 {
            color: #666;
            margin-bottom: 20px;
        }
        p {
            color: #888;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="offline-container">
        <div class="offline-icon">📱</div>
        <h1>离线模式</h1>
        <p>您当前处于离线状态。程序将在未来版本中支持完整的网络浏览功能。</p>
        <p>现在您可以：</p>
        <p>• 查看本地HTML文件<br>• 使用数据URL<br>• 享受离线浏览体验</p>
    </div>
</body>
</html>)";
    
    setHtml(offlineHtml);
}

void WebViewWidget::showErrorPage(const QString &url)
{
    QString errorHtml = fR"(<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>页面加载失败</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 40px;
            background: #fff3f3;
            color: #333;
            text-align: center;
        }}
        .error-container {{
            max-width: 600px;
            margin: 50px auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #f44336;
        }}
        .error-icon {{
            font-size: 4em;
            margin-bottom: 20px;
            color: #f44336;
        }}
        h1 {{
            color: #f44336;
            margin-bottom: 20px;
        }}
        .url-display {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            font-family: monospace;
            margin: 20px 0;
            word-break: break-all;
        }}
        .solutions {{
            text-align: left;
            margin-top: 30px;
        }}
        .solution {{
            margin: 15px 0;
            padding: 10px;
            background: #f9f9f9;
            border-radius: 5px;
        }}
        .solution::before {{
            content: "💡 ";
        }}
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-icon">⚠️</div>
        <h1>当前功能限制</h1>
        <p>您尝试访问的URL: <strong>{url}</strong></p>
        <div class="url-display">{url}</div>
        <p>QTextBrowser组件无法直接加载网络内容，但支持多种本地文件格式。</p>
        
        <div class="solutions">
            <h3>🔧 解决方案</h3>
            <div class="solution"><strong>本地文件:</strong> 输入文件路径，如: C:\\Users\\Desktop\\example.html</div>
            <div class="solution"><strong>数据URL:</strong> 输入 data: 开头的内容</div>
            <div class="solution"><strong>WebEngine:</strong> 正在集成Qt WebEngine，未来版本将支持完整网络浏览</div>
            <div class="solution"><strong>外部浏览器:</strong> 右键点击链接，选择"在默认浏览器中打开"</div>
        </div>
        
        <p style="margin-top: 30px; color: #666; font-size: 0.9em;">
            如需完整的网页浏览功能，建议集成Qt WebEngine。
        </p>
    </div>
</body>
</html>)";
    
    setHtml(errorHtml);
    m_currentTitle = "页面加载失败";
    emit titleChanged(m_currentTitle);
    m_statusLabel->setText("网络功能受限 - 请查看解决方案");
}

void WebViewWidget::copyUrl()
{
    if (!m_currentUrl.isEmpty()) {
        QApplication::clipboard()->setText(m_currentUrl);
        m_statusLabel->setText("URL已复制到剪贴板");
    }
}

void WebViewWidget::openInDefaultBrowser()
{
    if (!m_currentUrl.isEmpty()) {
        QDesktopServices::openUrl(QUrl(m_currentUrl));
        m_statusLabel->setText("已在默认浏览器中打开");
    }
}

void WebViewWidget::onAnchorClicked(const QUrl &url)
{
    QString scheme = url.scheme();
    
    if (scheme == "http" || scheme == "https") {
        // 网络链接 - 显示错误页面
        showErrorPage(url.toString());
    } else if (scheme == "file") {
        // 本地文件
        loadFile(url.toString());
    } else {
        // 其他类型
        QDesktopServices::openUrl(url);
    }
}

void WebViewWidget::loadFile(const QString &filePath)
{
    QFile file(filePath);
    if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        QTextStream stream(&file);
        stream.setEncoding(QStringConverter::Utf8);
        QString content = stream.readAll();
        file.close();
        
        setHtml(content, QUrl(filePath).toString(QUrl::RemoveFilename));
        m_statusLabel->setText("已加载本地文件");
    } else {
        showErrorPage(filePath);
    }
}'''
    
    # 写入文件
    with open("src/webviewwidget.h", "w", encoding="utf-8") as f:
        f.write(enhanced_header)
    
    with open("src/webviewwidget.cpp", "w", encoding="utf-8") as f:
        f.write(enhanced_implementation)
    
    print("  ✅ 增强版WebViewWidget已创建")
    print("  🎯 新增功能:")
    print("    • 改进的错误页面显示")
    print("    • 更友好的用户界面")
    print("    • 本地文件加载优化")
    print("    • 数据URL支持")
    print("    • 外部浏览器集成")
    print("    • 为未来WebEngine升级预留接口")

def main():
    """主函数"""
    print("🚀 创建增强WebView解决方案")
    print("=" * 50)
    
    create_enhanced_webview()
    
    print("=" * 50)
    print("✅ 增强WebViewWidget创建完成！")
    print()
    print("📋 接下来请运行:")
    print("   scons")
    print("   ./bin/qt_toolbar_webview.exe")
    print()
    print("🎯 新增功能亮点:")
    print("   • 美观的欢迎页面")
    print("   • 智能错误处理")
    print("   • 本地文件优化加载")
    print("   • 为WebEngine升级做准备")

if __name__ == "__main__":
    main()