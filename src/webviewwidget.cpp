#include "webviewwidget.h"
#include <QVBoxLayout>
#include <QClipboard>
#include <QApplication>
#include <QDesktopServices>
#include <QUrl>
#include <QString>
#include <qwebengineview.h>
#include <qwebenginesettings.h>
#include <qwebenginehistory.h>
#include <qtwebenginewidgetsglobal.h>

WebViewWidget::WebViewWidget(QWidget *parent) : QWidget(parent),
    m_webView(new QWebEngineView(this)),
    m_homeUrl("https://www.funnyai.com")
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
    
    layout->addWidget(m_webView);
    
    setLayout(layout);
    
    m_webView->settings()->setAttribute(QWebEngineSettings::JavascriptEnabled, true);
    m_webView->settings()->setAttribute(QWebEngineSettings::PluginsEnabled, true);
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
}

void WebViewWidget::openInDefaultBrowser()
{
    QDesktopServices::openUrl(QUrl(getCurrentUrl()));
}

void WebViewWidget::onLoadStarted()
{
    emit loadStarted();
}

void WebViewWidget::navigate(const QString &url)
{
    loadUrl(url);
}

void WebViewWidget::onLoadProgress(int progress)
{
    emit loadProgress(progress);
}

void WebViewWidget::onLoadFinished(bool ok)
{
    emit loadFinished(ok);
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
    <title>Qt WebEngine 浏览器</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; }
        .features { text-align: left; max-width: 400px; margin: 20px auto; }
    </style>
</head>
<body>
    <h1>🌐 Qt WebEngine 浏览器演示</h1>
    <p>完整的网页浏览功能现已启用！</p>
    <div class="features">
        <h3>支持的功能：</h3>
        <ul>
            <li>✅ 完整的网页浏览</li>
            <li>✅ HTTPS/SSL支持</li>
            <li>✅ JavaScript执行</li>
            <li>✅ 现代网页标准</li>
        </ul>
    </div>
    <p>在地址栏输入任何URL开始浏览！</p>
</body>
</html>)";
}
