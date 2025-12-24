#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qt WebEngine集成脚本
当Conan依赖下载完成后，自动集成WebEngine功能
"""

import os
import shutil
from datetime import datetime

def check_conan_completion():
    """检查Conan是否完成依赖下载"""
    print("🔍 检查Conan构建状态...")
    
    # 检查是否有Qt WebEngine相关的包被下载
    conan_cache = "C:/Users/happyli/.conan2"
    
    if os.path.exists(conan_cache):
        # 检查Qt相关包
        qt_packages = []
        for root, dirs, files in os.walk(conan_cache):
            for dir_name in dirs:
                if "qt" in dir_name.lower() and "webengine" in dir_name.lower():
                    qt_packages.append(dir_name)
        
        if qt_packages:
            print(f"✅ 找到Qt WebEngine包: {qt_packages}")
            return True
        else:
            print("⏳ 正在下载Qt WebEngine依赖...")
            return False
    else:
        print("❌ Conan缓存目录不存在")
        return False

def create_webengine_webview():
    """创建WebEngine版本的WebViewWidget"""
    print("🔧 创建WebEngine版本的WebViewWidget...")
    
    # 备份当前版本
    backup_files = [
        ("src/webviewwidget.h", "src/webviewwidget.h.qtbrowser_backup"),
        ("src/webviewwidget.cpp", "src/webviewwidget.cpp.qtbrowser_backup")
    ]
    
    for src, dest in backup_files:
        if os.path.exists(src):
            shutil.copy2(src, dest)
            print(f"  📋 备份: {src} -> {dest}")
    
    # 创建WebEngine版本的头文件
    create_webengine_header()
    
    # 创建WebEngine版本的实现文件
    create_webengine_implementation()
    
    print("  ✅ WebEngine版本WebViewWidget已创建")

def create_webengine_header():
    """创建WebEngine版本头文件"""
    header_content = '''#ifndef WEBVIEWWIDGET_H
#define WEBVIEWWIDGET_H

#include <QWidget>
#include <QWebEngineView>
#include <QUrl>
#include <QString>
#include <QProgressBar>
#include <QLabel>

class WebViewWidget : public QWidget
{
    Q_OBJECT
    
public:
    explicit WebViewWidget(QWidget *parent = nullptr);
    ~WebViewWidget() override;
    
    void loadUrl(const QString &url);
    void setHtml(const QString &html, const QString &baseUrl = QString());
    QString getCurrentUrl() const;
    QString getCurrentTitle() const;
    bool canGoBack() const;
    bool canGoForward() const;
    
    void showWelcomePage();
    
public slots:
    void goBack();
    void goForward();
    void refresh();
    void stop();
    void setHomeUrl(const QString &url);
    void goHome();
    void copyUrl();
    void openInDefaultBrowser();
    
signals:
    void titleChanged(const QString &title);
    void urlChanged(const QString &url);
    void loadProgress(int progress);
    void loadFinished(bool ok);
    
private slots:
    void onLoadStarted();
    void onLoadProgress(int progress);
    void onLoadFinished(bool ok);
    void onTitleChanged(const QString &title);
    void onUrlChanged(const QUrl &url);
    
private:
    QWebEngineView *m_webView;
    QProgressBar *m_progressBar;
    QLabel *m_statusLabel;
    QString m_homeUrl;
    QString m_currentUrl;
    QString m_currentTitle;
    
    void setupUI();
    void setupConnections();
    QString generateWelcomePage();
};

#endif // WEBVIEWWIDGET_H
'''
    
    with open("src/webviewwidget.h", "w", encoding="utf-8") as f:
        f.write(header_content)

def create_webengine_implementation():
    """创建WebEngine版本实现文件"""
    implementation_content = '''#include "webviewwidget.h"
#include <QVBoxLayout>
#include <QClipboard>
#include <QApplication>
#include <QDesktopServices>
#include <QUrl>
#include <QString>
#include <QStandardPaths>
#include <QDir>

WebViewWidget::WebViewWidget(QWidget *parent) : QWidget(parent),
    m_webView(new QWebEngineView(this)),
    m_progressBar(new QProgressBar(this)),
    m_statusLabel(new QLabel("就绪", this)),
    m_homeUrl("https://www.baidu.com")
{
    setupUI();
    setupConnections();
    showWelcomePage();
}

WebViewWidget::~WebViewWidget()
{
}

void WebViewWidget::setupUI()
{
    QVBoxLayout *layout = new QVBoxLayout(this);
    layout->setContentsMargins(0, 0, 0, 0);
    
    // 进度条
    m_progressBar->setVisible(false);
    layout->addWidget(m_progressBar);
    
    // Web视图
    layout->addWidget(m_webView);
    
    // 状态标签
    m_statusLabel->setStyleSheet("QLabel { padding: 5px; background-color: #f0f0f0; border: 1px solid #ccc; }");
    layout->addWidget(m_statusLabel);
    
    setLayout(layout);
    
    // 设置WebEngine属性
    m_webView->settings()->setAttribute(QWebEngineSettings::JavascriptEnabled, true);
    m_webView->settings()->setAttribute(QWebEngineSettings::PluginsEnabled, true);
    m_webView->settings()->setAttribute(QWebEngineSettings::FullScreenSupportEnabled, true);
}

void WebViewWidget::setupConnections()
{
    connect(m_webView, &QWebEngineView::loadStarted,
            this, &WebViewWidget::onLoadStarted);
    connect(m_webView, &QWebEngineView::loadProgress,
            this, &WebViewWidget::onLoadProgress);
    connect(m_webView, &QWebEngineView::loadFinished,
            this, &WebViewWidget::onLoadFinished);
    connect(m_webView, &QWebEngineView::titleChanged,
            this, &WebViewWidget::onTitleChanged);
    connect(m_webView, &QWebEngineView::urlChanged,
            this, &WebViewWidget::onUrlChanged);
}

void WebViewWidget::loadUrl(const QString &url)
{
    QUrl qurl(url);
    
    if (qurl.scheme().isEmpty()) {
        // 如果没有协议，添加https://
        qurl = QUrl("https://" + url);
    }
    
    m_webView->setUrl(qurl);
    m_currentUrl = url;
    emit urlChanged(url);
}

void WebViewWidget::setHtml(const QString &html, const QString &baseUrl)
{
    m_webView->setHtml(html, QUrl(baseUrl));
}

QString WebViewWidget::getCurrentUrl() const
{
    return m_webView->url().toString();
}

QString WebViewWidget::getCurrentTitle() const
{
    return m_webView->title();
}

bool WebViewWidget::canGoBack() const
{
    return m_webView->history()->canGoBack();
}

bool WebViewWidget::canGoForward() const
{
    return m_webView->history()->canGoForward();
}

void WebViewWidget::showWelcomePage()
{
    m_webView->setHtml(generateWelcomePage());
}

void WebViewWidget::goBack()
{
    m_webView->back();
}

void WebViewWidget::goForward()
{
    m_webView->forward();
}

void WebViewWidget::refresh()
{
    m_webView->reload();
}

void WebViewWidget::stop()
{
    m_webView->stop();
}

void WebViewWidget::setHomeUrl(const QString &url)
{
    m_homeUrl = url;
}

void WebViewWidget::goHome()
{
    loadUrl(m_homeUrl);
}

void WebViewWidget::copyUrl()
{
    QClipboard *clipboard = QApplication::clipboard();
    clipboard->setText(getCurrentUrl());
    m_statusLabel->setText("URL已复制到剪贴板");
}

void WebViewWidget::openInDefaultBrowser()
{
    QDesktopServices::openUrl(QUrl(getCurrentUrl()));
}

void WebViewWidget::onLoadStarted()
{
    m_progressBar->setVisible(true);
    m_progressBar->setValue(0);
    m_statusLabel->setText("正在加载...");
}

void WebViewWidget::onLoadProgress(int progress)
{
    m_progressBar->setValue(progress);
    m_statusLabel->setText(QString("加载进度: %1%").arg(progress));
}

void WebViewWidget::onLoadFinished(bool ok)
{
    m_progressBar->setVisible(false);
    
    if (ok) {
        m_statusLabel->setText("加载完成");
        emit loadFinished(true);
    } else {
        m_statusLabel->setText("加载失败");
        emit loadFinished(false);
    }
}

void WebViewWidget::onTitleChanged(const QString &title)
{
    m_currentTitle = title;
    emit titleChanged(title);
}

void WebViewWidget::onUrlChanged(const QUrl &url)
{
    m_currentUrl = url.toString();
    emit urlChanged(m_currentUrl);
}

QString WebViewWidget::generateWelcomePage()
{
    return R"(<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qt WebEngine 浏览器演示</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            margin: 0;
            padding: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .container {
            max-width: 600px;
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .features {
            text-align: left;
            margin: 30px 0;
        }
        .feature {
            margin: 15px 0;
            padding: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            border-left: 4px solid #4CAF50;
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
            border: 2px solid transparent;
        }
        .demo-link:hover {
            background: rgba(255, 255, 255, 0.3);
            border-color: white;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 Qt WebEngine 浏览器</h1>
        <p>欢迎使用基于Qt WebEngine的浏览器演示程序！</p>
        
        <div class="features">
            <h3>🚀 支持的功能：</h3>
            <div class="feature">✅ 完整的网页浏览功能</div>
            <div class="feature">✅ HTTPS/SSL网站支持</div>
            <div class="feature">✅ JavaScript执行</div>
            <div class="feature">✅ 现代网页标准支持</div>
            <div class="feature">✅ 前进/后退导航</div>
            <div class="feature">✅ 页面刷新和停止</div>
            <div class="feature">✅ 进度条显示</div>
        </div>
        
        <div class="demo-links">
            <h3>🎯 快速测试：</h3>
            <a href="https://www.baidu.com" class="demo-link">百度搜索</a>
            <a href="https://www.github.com" class="demo-link">GitHub</a>
            <a href="https://www.funnyai.com" class="demo-link">FunnyAI</a>
        </div>
        
        <p style="margin-top: 30px; opacity: 0.8;">
            在地址栏中输入任何URL开始浏览！
        </p>
    </div>
</body>
</html>)";
}
'''
    
    with open("src/webviewwidget.cpp", "w", encoding="utf-8") as f:
        f.write(implementation_content)

def integrate_webengine():
    """主集成函数"""
    print("🔧 开始WebEngine集成...")
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查Conan是否完成
    if not check_conan_completion():
        print("⏳ 等待Conan完成依赖下载...")
        return False
    
    # 创建WebEngine版本
    create_webengine_webview()
    
    print("✅ WebEngine集成完成！")
    print("📝 下一步: 运行scons重新编译")
    
    return True

if __name__ == "__main__":
    success = integrate_webengine()
    if success:
        print("🎉 WebEngine集成成功！可以开始测试了。")
    else:
        print("⏳ 等待Conan完成后再试。")