#include "webviewwidget.h"
#include <QWebEngineView>
#include <QWebEngineHistory>
#include <QVBoxLayout>
#include <QContextMenuEvent>
#include <QMenu>
#include <QAction>
#include <QApplication>
#include <QClipboard>
#include <QDesktopServices>
#include <QDebug>

/**
 * 自定义WebEngine页面实现
 */
CustomWebPage::CustomWebPage(QObject *parent)
    : QWebEnginePage(parent)
{
}

/**
 * 处理右键菜单事件 - 添加开发工具选项
 */
void CustomWebPage::contextMenuEvent(QContextMenuEvent *event)
{
    QMenu *menu = createStandardContextMenu();
    
    if (menu) {
        // 添加分隔线
        menu->addSeparator();
        
        // 添加"检查元素"菜单项
        QAction *inspectAction = menu->addAction("检查元素");
        connect(inspectAction, &QAction::triggered, this, [this]() {
            this->triggerAction(QWebEnginePage::InspectElement);
        });
        
        // 添加"打开开发工具"菜单项
        QAction *devToolsAction = menu->addAction("打开开发工具");
        connect(devToolsAction, &QAction::triggered, this, [this]() {
            this->triggerAction(QWebEnginePage::InspectElement);
        });
        
        menu->exec(event->globalPos());
        delete menu;
    }
}

/**
 * 重写弹出窗口创建函数 - 在当前窗口打开
 */
QWebEnginePage* CustomWebPage::createWindow(WebWindowType type)
{
    // 返回当前页面，让弹出窗口在当前窗口打开
    return this;
}

/**
 * 构造函数 - 初始化WebView组件
 */
WebViewWidget::WebViewWidget(QWidget *parent)
    : QWidget(parent)
    , m_webView(nullptr)
    , m_homeUrl("https://www.funnyai.com")
    , m_currentUrl("")
    , m_currentTitle("欢迎使用Qt6 WebView")
{
    setupUI();
    setupConnections();
    
    qDebug() << "WebView组件已初始化";
}

/**
 * 析构函数 - 清理WebView资源
 */
WebViewWidget::~WebViewWidget()
{
    qDebug() << "WebView组件正在销毁";
}

/**
 * 初始化UI界面
 */
void WebViewWidget::setupUI()
{
    // 创建主布局
    QVBoxLayout *layout = new QVBoxLayout(this);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->setSpacing(0);
    
    // 创建WebEngineView
    m_webView = new QWebEngineView(this);
    
    // 设置自定义页面
    CustomWebPage *customPage = new CustomWebPage(m_webView);
    m_webView->setPage(customPage);
    
    // 添加到布局
    layout->addWidget(m_webView);
    
    qDebug() << "WebView UI已设置完成";
}

/**
 * 连接信号和槽
 */
void WebViewWidget::setupConnections()
{
    // 连接WebView信号
    connect(m_webView, &QWebEngineView::titleChanged, this, &WebViewWidget::onTitleChanged);
    connect(m_webView, &QWebEngineView::urlChanged, this, &WebViewWidget::onUrlChanged);
    connect(m_webView, &QWebEngineView::loadStarted, this, &WebViewWidget::onLoadStarted);
    connect(m_webView, &QWebEngineView::loadProgress, this, &WebViewWidget::onLoadProgress);
    connect(m_webView, &QWebEngineView::loadFinished, this, &WebViewWidget::onLoadFinished);
    
    qDebug() << "WebView信号连接完成";
}

/**
 * 加载指定URL
 */
void WebViewWidget::loadUrl(const QString &url)
{
    if (m_webView) {
        QUrl qurl(url);
        if (qurl.scheme().isEmpty()) {
            qurl.setScheme("https");
        }
        m_webView->load(qurl);
        qDebug() << "加载URL:" << url;
    }
}

/**
 * 导航到指定URL
 */
void WebViewWidget::navigate(const QString &url)
{
    loadUrl(url);
}

/**
 * 设置HTML内容
 */
void WebViewWidget::setHtml(const QString &html, const QString &baseUrl)
{
    if (m_webView) {
        m_webView->setHtml(html, QUrl(baseUrl));
    }
}

/**
 * 获取当前URL
 */
QString WebViewWidget::getCurrentUrl() const
{
    return m_currentUrl;
}

/**
 * 获取当前标题
 */
QString WebViewWidget::getCurrentTitle() const
{
    return m_currentTitle;
}

/**
 * 检查是否可以返回
 */
bool WebViewWidget::canGoBack() const
{
    return m_webView ? m_webView->history()->canGoBack() : false;
}

/**
 * 检查是否可以前进
 */
bool WebViewWidget::canGoForward() const
{
    return m_webView ? m_webView->history()->canGoForward() : false;
}

/**
 * 显示欢迎页面
 */
void WebViewWidget::showWelcomePage()
{
    QString html = generateWelcomePage();
    setHtml(html);
}

/**
 * 返回上一页
 */
void WebViewWidget::goBack()
{
    if (m_webView && m_webView->history()->canGoBack()) {
        m_webView->back();
        qDebug() << "返回上一页";
    }
}

/**
 * 前进到下一页
 */
void WebViewWidget::goForward()
{
    if (m_webView && m_webView->history()->canGoForward()) {
        m_webView->forward();
        qDebug() << "前进到下一页";
    }
}

/**
 * 刷新当前页面
 */
void WebViewWidget::refresh()
{
    if (m_webView) {
        m_webView->reload();
        qDebug() << "刷新页面";
    }
}

/**
 * 停止加载
 */
void WebViewWidget::stop()
{
    if (m_webView) {
        m_webView->stop();
        qDebug() << "停止加载";
    }
}

/**
 * 设置主页URL
 */
void WebViewWidget::setHomeUrl(const QString &url)
{
    m_homeUrl = url;
    qDebug() << "主页URL已设置:" << url;
}

/**
 * 跳转到主页
 */
void WebViewWidget::goHome()
{
    loadUrl(m_homeUrl);
    qDebug() << "跳转到主页";
}

/**
 * 复制当前URL
 */
void WebViewWidget::copyUrl()
{
    if (!m_currentUrl.isEmpty()) {
        QClipboard *clipboard = QApplication::clipboard();
        clipboard->setText(m_currentUrl);
        qDebug() << "URL已复制到剪贴板";
    }
}

/**
 * 在默认浏览器中打开
 */
void WebViewWidget::openInDefaultBrowser()
{
    if (!m_currentUrl.isEmpty()) {
        QDesktopServices::openUrl(QUrl(m_currentUrl));
        qDebug() << "在默认浏览器中打开:" << m_currentUrl;
    }
}

/**
 * 开始加载处理
 */
void WebViewWidget::onLoadStarted()
{
    emit loadStarted();
    qDebug() << "页面开始加载";
}

/**
 * 加载进度处理
 */
void WebViewWidget::onLoadProgress(int progress)
{
    emit loadProgress(progress);
}

/**
 * 加载完成处理
 */
void WebViewWidget::onLoadFinished(bool ok)
{
    emit loadFinished(ok);
    qDebug() << "页面加载完成, 状态:" << (ok ? "成功" : "失败");
}

/**
 * 标题改变处理
 */
void WebViewWidget::onTitleChanged(const QString &title)
{
    m_currentTitle = title;
    emit titleChanged(title);
    qDebug() << "页面标题改变:" << title;
}

/**
 * URL改变处理
 */
void WebViewWidget::onUrlChanged(const QUrl &url)
{
    m_currentUrl = url.toString();
    emit urlChanged(m_currentUrl);
    qDebug() << "URL改变:" << m_currentUrl;
}

/**
 * 生成欢迎页面HTML
 */
QString WebViewWidget::generateWelcomePage()
{
    return R"(<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>欢迎使用Qt6 WebView</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            line-height: 1.6;
            margin: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 500px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            max-width: 600px;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        .description {
            font-size: 1.2em;
            margin-bottom: 30px;
            opacity: 0.9;
        }
        .features {
            text-align: left;
            margin: 20px 0;
        }
        .feature {
            margin: 10px 0;
            padding: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
        }
        .button {
            display: inline-block;
            padding: 12px 24px;
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 25px;
            color: white;
            text-decoration: none;
            margin: 10px;
            transition: all 0.3s ease;
        }
        .button:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 欢迎使用Qt6 WebView</h1>
        <div class="description">
            这是一个使用Qt6 WebEngine构建的WebView应用程序，支持工具栏导航和网页浏览功能。
        </div>
        
        <div class="features">
            <h3>📋 功能特性</h3>
            <div class="feature">✅ 工具栏导航控制（后退、前进、刷新、停止、主页）</div>
            <div class="feature">✅ URL地址栏输入和显示</div>
            <div class="feature">✅ 页面加载进度显示</div>
            <div class="feature">✅ 历史记录管理</div>
            <div class="feature">✅ 右键菜单开发工具</div>
            <div class="feature">✅ 弹出窗口在当前窗口打开</div>
        </div>
        
        <a href="https://www.funnyai.com" class="button">🚀 访问FunnyAI</a>
    </div>
</body>
</html>)";
}
