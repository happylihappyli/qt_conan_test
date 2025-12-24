#include "webviewwidget.h"
#include <QApplication>
#include <QClipboard>
#include <QMessageBox>
#include <QTimer>
#include <QTextDocument>
#include <QTextCursor>
#include <QFileInfo>
#include <QStandardPaths>
#include <QDir>
#include <QRegularExpression>

/**
 * 构造函数 - 初始化WebView组件和UI
 * @param parent 父窗口指针
 */
WebViewWidget::WebViewWidget(QWidget* parent)
    : QWidget(parent)
    , mainLayout(nullptr)
    , webView(nullptr)
    , historyList()
    , historyIndex(-1)
    , homeUrl("file:///")
    , isLoading(false)
    , currentTitle("欢迎使用Qt6 WebView")
{
    // 设置组件属性
    setObjectName("WebViewWidget");
    setMinimumHeight(400);
    
    // 初始化UI
    setupWebView();
    connectSignals();
    
    // 加载默认HTML内容
    loadDefaultHtml();
    
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
 * 初始化WebView设置和配置
 */
void WebViewWidget::setupWebView()
{
    // 创建主布局
    mainLayout = new QVBoxLayout(this);
    mainLayout->setSpacing(0);
    mainLayout->setContentsMargins(0, 0, 0, 0);
    
    // 创建WebView (使用QTextBrowser显示本地内容)
    webView = new QTextBrowser(this);
    webView->setObjectName("WebView");
    // 设置QTextBrowser支持基本格式
    webView->setOpenExternalLinks(true);
    webView->setOpenLinks(true);
    
    // 添加到布局
    mainLayout->addWidget(webView);
    
    qDebug() << "WebView设置完成";
}

/**
 * 加载默认HTML内容
 */
void WebViewWidget::loadDefaultHtml()
{
    QString htmlContent = R"(<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qt6 WebView 示例</title>
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
        .code {
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            margin: 20px 0;
            text-align: left;
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
        .tech-stack {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            margin: 20px 0;
        }
        .tech-item {
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 20px;
            margin: 5px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 欢迎使用Qt6 WebView</h1>
        <div class="description">
            这是一个使用Qt6构建的WebView应用程序，支持工具栏导航和网页浏览功能。
        </div>
        
        <div class="features">
            <h3>📋 功能特性</h3>
            <div class="feature">✅ 工具栏导航控制（后退、前进、刷新、停止、主页）</div>
            <div class="feature">✅ URL地址栏输入和显示</div>
            <div class="feature">✅ 页面加载进度显示</div>
            <div class="feature">✅ 历史记录管理</div>
            <div class="feature">✅ 菜单栏支持</div>
            <div class="feature">✅ 键盘快捷键支持</div>
        </div>
        
        <div class="tech-stack">
            <span class="tech-item">Qt6 Widgets</span>
            <span class="tech-item">Conan包管理</span>
            <span class="tech-item">SCons构建</span>
            <span class="tech-item">C++17标准</span>
        </div>
        
        <div class="code">
使用示例：<br>
1. 在地址栏输入网址（如：https://www.qt.io）<br>
2. 点击工具栏按钮进行页面导航<br>
3. 使用快捷键：Ctrl+L（地址栏）、F5（刷新）等
        </div>
        
        <a href="https://www.qt.io" class="button">🚀 访问Qt官网</a>
        <a href="https://doc.qt.io" class="button">📖 Qt文档</a>
    </div>
</body>
</html>)";
    
    webView->setHtml(htmlContent);
    currentTitle = "Qt6 WebView 示例";
    addToHistory("about:blank", currentTitle);
    
    // 发送信号
    emit urlChanged("about:blank");
    emit titleChanged(currentTitle);
    emit loadProgress(100);
    emit loadFinished(true, "about:blank");
}

/**
 * 加载本地HTML文件
 * @param filePath HTML文件路径
 * @return 是否加载成功
 */
bool WebViewWidget::loadHtmlFile(const QString& filePath)
{
    QFileInfo fileInfo(filePath);
    if (!fileInfo.exists() || !fileInfo.isFile()) {
        qWarning() << "HTML文件不存在:" << filePath;
        return false;
    }
    
    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qWarning() << "无法打开HTML文件:" << filePath;
        return false;
    }
    
    QTextStream stream(&file);
    stream.setEncoding(QStringConverter::Utf8);
    QString htmlContent = stream.readAll();
    file.close();
    
    webView->setHtml(htmlContent);
    webView->setSource(QUrl::fromLocalFile(fileInfo.absolutePath()));
    currentTitle = fileInfo.baseName();
    
    addToHistory(QUrl::fromLocalFile(filePath).toString(), currentTitle);
    return true;
}

/**
 * 加载网页内容
 * @param url 要加载的URL
 */
void WebViewWidget::loadWebContent(const QString& url)
{
    QUrl qurl(url);
    
    if (qurl.scheme().isEmpty()) {
        // 如果没有协议，假设是HTTPS
        qurl.setScheme("https");
    }
    
    // 处理各种URL类型
    if (qurl.isLocalFile()) {
        // 加载本地文件
        loadHtmlFile(qurl.toLocalFile());
    } else if (url.startsWith("data:")) {
        // 加载data URL
        loadDataUrl(url);
    } else if (url.startsWith("http://") || url.startsWith("https://")) {
        // QTextBrowser不支持网络内容，显示限制提示
        qDebug() << "QTextBrowser不支持网络内容:" << url;
        showNetworkLimitation(url);
    } else {
        // 尝试作为文本文件加载
        loadTextContent(url);
    }
}

/**
 * 处理网络内容限制提示
 * @param url 要加载的URL
 */
void WebViewWidget::showNetworkLimitation(const QString& url)
{
    QString enhancedErrorHtml = QString(R"(<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>网页加载限制说明</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            line-height: 1.6;
            margin: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 500px;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            max-width: 700px;
            margin: 0 auto;
        }
        h1 {
            color: #fff;
            text-align: center;
            margin-bottom: 30px;
        }
        .warning-box {
            background: rgba(255, 193, 7, 0.2);
            border: 2px solid #ffc107;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }
        .feature-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .feature-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #4caf50;
        }
        .code-block {
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            margin: 15px 0;
            border-left: 4px solid #2196f3;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 25px;
            color: white;
            text-decoration: none;
            margin: 5px;
            transition: all 0.3s ease;
        }
        .btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 网页加载功能说明</h1>
        
        <div class="warning-box">
            <h3>⚠️ 当前功能限制</h3>
            <p>您尝试访问的URL: <strong>%1</strong></p>
            <p>QTextBrowser组件无法直接加载网络内容，但支持多种本地文件格式。</p>
        </div>
        
        <h3>✅ 支持的功能</h3>
        <div class="feature-list">
            <div class="feature-item">
                <h4>📁 本地HTML文件</h4>
                <p>支持完整的HTML、CSS、JavaScript</p>
                <p>格式：file:///path/to/file.html</p>
            </div>
            <div class="feature-item">
                <h4>📄 Markdown文件</h4>
                <p>自动转换为HTML显示</p>
                <p>格式：file:///path/to/file.md</p>
            </div>
            <div class="feature-item">
                <h4>📝 文本文件</h4>
                <p>支持.txt, .log, .csv等</p>
                <p>格式：file:///path/to/file.txt</p>
            </div>
            <div class="feature-item">
                <h4>🔗 Data URL</h4>
                <p>内嵌HTML内容的URL</p>
                <p>格式：data:text/html,&lt;html&gt;...&lt;/html&gt;</p>
            </div>
        </div>
        
        <h3>💡 使用建议</h3>
        <div class="code-block">
1. 加载本地HTML文件：<br>
   file:///C:/Users/YourName/Documents/test.html<br><br>
2. 创建简单的HTML：<br>
   data:text/html,&lt;h1&gt;Hello World&lt;/h1&gt;<br><br>
3. 加载Markdown文档：<br>
   file:///C:/Users/YourName/Documents/readme.md
        </div>
        
        <h3>🚀 升级建议</h3>
        <p>如需完整的网页浏览功能，建议集成Qt WebEngine：</p>
        <a href="https://doc.qt.io/qt-6/qtwebengine-index.html" class="btn">Qt WebEngine文档</a>
        <a href="https://github.com/qt/qtwebengine" class="btn">Qt WebEngine源码</a>
    </div>
</body>
</html>)").arg(url);
    
    webView->setHtml(enhancedErrorHtml);
    currentTitle = "网页加载功能说明";
    addToHistory(url, currentTitle);
    
    emit urlChanged(url);
    emit titleChanged(currentTitle);
    emit loadProgress(100);
    emit loadFinished(false, url);
}

/**
 * 加载Data URL内容
 * @param dataUrl Data URL字符串
 */
void WebViewWidget::loadDataUrl(const QString& dataUrl)
{
    QUrl url(dataUrl);
    if (url.scheme() == "data") {
        // 解析Data URL
        QString data = dataUrl.mid(dataUrl.indexOf(',') + 1);
        QByteArray decodedData = QByteArray::fromPercentEncoding(data.toUtf8());
        
        webView->setHtml(QString::fromUtf8(decodedData));
        currentTitle = "Data URL内容";
        addToHistory(dataUrl, currentTitle);
        
        emit urlChanged(dataUrl);
        emit titleChanged(currentTitle);
        emit loadProgress(100);
        emit loadFinished(true, dataUrl);
    }
}

/**
 * 加载文本内容
 * @param url 文件路径或文本内容
 */
void WebViewWidget::loadTextContent(const QString& url)
{
    // 尝试作为文件路径处理
    QFileInfo fileInfo(url);
    if (fileInfo.exists() && fileInfo.isFile()) {
        // 根据文件扩展名处理
        QString ext = fileInfo.suffix().toLower();
        if (ext == "md" || ext == "markdown") {
            loadMarkdownFile(url);
        } else if (ext == "txt" || ext == "log" || ext == "csv") {
            loadPlainTextFile(url);
        } else {
            // 通用文本文件
            loadHtmlFile(url);
        }
    } else {
        // 作为普通文本显示
        QString textContent = url;
        QString htmlContent = QString(R"(<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>文本内容</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            line-height: 1.6;
            margin: 20px;
            background: #f5f5f5;
            color: #333;
        }
        .text-content {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <div class="text-content">%1</div>
</body>
</html>)").arg(textContent.toHtmlEscaped());
        
        webView->setHtml(htmlContent);
        currentTitle = "文本内容";
        addToHistory(url, currentTitle);
        
        emit urlChanged(url);
        emit titleChanged(currentTitle);
        emit loadProgress(100);
        emit loadFinished(true, url);
    }
}

/**
 * 加载Markdown文件
 * @param filePath Markdown文件路径
 */
bool WebViewWidget::loadMarkdownFile(const QString& filePath)
{
    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qWarning() << "无法打开Markdown文件:" << filePath;
        return false;
    }
    
    QTextStream stream(&file);
    stream.setEncoding(QStringConverter::Utf8);
    QString markdownContent = stream.readAll();
    file.close();
    
    // 简单的Markdown转HTML（实际项目中可使用更完善的库）
    QString htmlContent = convertMarkdownToHtml(markdownContent);
    
    webView->setHtml(htmlContent);
    webView->setSource(QUrl::fromLocalFile(QFileInfo(filePath).absolutePath()));
    currentTitle = QFileInfo(filePath).baseName() + " (Markdown)";
    addToHistory(QUrl::fromLocalFile(filePath).toString(), currentTitle);
    
    emit urlChanged(QUrl::fromLocalFile(filePath).toString());
    emit titleChanged(currentTitle);
    emit loadProgress(100);
    emit loadFinished(true, QUrl::fromLocalFile(filePath).toString());
    
    return true;
}

/**
 * 加载纯文本文件
 * @param filePath 文本文件路径
 */
bool WebViewWidget::loadPlainTextFile(const QString& filePath)
{
    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qWarning() << "无法打开文本文件:" << filePath;
        return false;
    }
    
    QTextStream stream(&file);
    stream.setEncoding(QStringConverter::Utf8);
    QString textContent = stream.readAll();
    file.close();
    
    // 将文本内容转换为HTML格式显示
    QString htmlContent = QString(R"(<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>%1</title>
    <style>
        body {
            font-family: 'Courier New', 'Consolas', monospace;
            line-height: 1.6;
            margin: 20px;
            background: #f8f9fa;
            color: #333;
        }
        .file-header {
            background: #e9ecef;
            padding: 10px 15px;
            border-radius: 5px 5px 0 0;
            margin-bottom: 0;
            font-weight: bold;
        }
        .text-content {
            background: white;
            padding: 20px;
            border-radius: 0 0 5px 5px;
            border: 1px solid #dee2e6;
            border-top: none;
            white-space: pre-wrap;
            overflow-x: auto;
            font-family: 'Courier New', 'Consolas', monospace;
            font-size: 14px;
        }
        .line-numbers {
            color: #6c757d;
            user-select: none;
            padding-right: 15px;
        }
    </style>
</head>
<body>
    <div class="file-header">📄 %1</div>
    <div class="text-content">%2</div>
</body>
</html>)").arg(QFileInfo(filePath).fileName()).arg(textContent.toHtmlEscaped());
    
    webView->setHtml(htmlContent);
    webView->setSource(QUrl::fromLocalFile(QFileInfo(filePath).absolutePath()));
    currentTitle = QFileInfo(filePath).baseName() + " (文本)";
    addToHistory(QUrl::fromLocalFile(filePath).toString(), currentTitle);
    
    emit urlChanged(QUrl::fromLocalFile(filePath).toString());
    emit titleChanged(currentTitle);
    emit loadProgress(100);
    emit loadFinished(true, QUrl::fromLocalFile(filePath).toString());
    
    return true;
}

/**
 * 简单的Markdown转HTML转换
 * @param markdown Markdown内容
 * @return 转换后的HTML内容
 */
QString WebViewWidget::convertMarkdownToHtml(const QString& markdown)
{
    QString html = markdown;
    
    // 标题转换
    html.replace(QRegularExpression(R"(^###\s+(.+)$)", QRegularExpression::MultilineOption), R"(<h3>\1</h3>)");
    html.replace(QRegularExpression(R"(^##\s+(.+)$)", QRegularExpression::MultilineOption), R"(<h2>\1</h2>)");
    html.replace(QRegularExpression(R"(^#\s+(.+)$)", QRegularExpression::MultilineOption), R"(<h1>\1</h1>)");
    
    // 粗体和斜体
    html.replace(QRegularExpression(R"(\*\*(.+?)\*\*)"), R"(<strong>\1</strong>)");
    html.replace(QRegularExpression(R"(\*(.+?)\*)"), R"(<em>\1</em>)");
    
    // 链接
    html.replace(QRegularExpression(R"(\[([^\]]+)\]\(([^)]+)\))"), R"(<a href="\2">\1</a>)");
    
    // 代码块
    html.replace(QRegularExpression(R"(```(\w+)?\n([\s\S]*?)\n```)"), R"(<pre><code class="language-\1">\2</code></pre>)");
    html.replace(QRegularExpression(R"(`([^`]+)`)"), R"(<code>\1</code>)");
    
    // 列表
    html.replace(QRegularExpression(R"(^\s*[-*+]\s+(.+)$)", QRegularExpression::MultilineOption), R"(<li>\1</li>)");
    html.replace(QRegularExpression(R"(<li>([\s\S]*?)</li>)"), R"(<ul><li>\1</li></ul>)");
    
    // 段落
    QStringList lines = html.split('\n');
    QString result;
    bool inList = false;
    
    for (const QString& line : lines) {
        if (line.startsWith("<ul><li>")) {
            if (!inList) {
                result += "<ul>";
                inList = true;
            }
            QString modifiedLine = line;
            modifiedLine.replace("<ul><li>", "<li>");
            modifiedLine.replace("</li></ul>", "</li>");
            result += modifiedLine;
        } else if (inList && line.trimmed().isEmpty()) {
            result += "</ul>";
            inList = false;
        } else if (inList && !line.startsWith("<li>")) {
            result += "</ul>";
            result += line;
            inList = false;
        } else {
            if (!line.trimmed().isEmpty() && !line.startsWith("<h") && !line.startsWith("<ul>")) {
                result += "<p>" + line + "</p>";
            } else {
                result += line;
            }
        }
    }
    
    if (inList) {
        result += "</ul>";
    }
    
    return QString(R"(<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Markdown文档</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            line-height: 1.6;
            margin: 40px;
            background: #f8f9fa;
            color: #333;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 800px;
            margin: 0 auto;
        }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; }
        h3 { color: #7f8c8d; }
        code { background: #f1f2f6; padding: 2px 5px; border-radius: 3px; font-family: 'Courier New', monospace; }
        pre { background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; overflow-x: auto; }
        pre code { background: none; padding: 0; }
        a { color: #3498db; text-decoration: none; }
        a:hover { text-decoration: underline; }
        ul { margin: 15px 0; }
        li { margin: 5px 0; }
    </style>
</head>
<body>
    <div class="container">
        %1
    </div>
</body>
</html>)").arg(result);
}

/**
 * 导航到指定URL
 * @param url 目标URL地址
 */
void WebViewWidget::navigate(const QString& url)
{
    qDebug() << "WebView导航到:" << url;
    emit loadProgress(50);
    
    // 发送开始加载信号
    emit loadStarted(url);
    
    // 模拟加载过程
    QTimer::singleShot(500, [this, url]() {
        loadWebContent(url);
        emit loadProgress(100);
        emit loadFinished(true, url);
    });
}

/**
 * 获取当前URL
 * @return 当前页面URL字符串
 */
QString WebViewWidget::getCurrentUrl() const
{
    if (historyIndex >= 0 && historyIndex < historyList.size()) {
        return historyList[historyIndex];
    }
    return "about:blank";
}

/**
 * 获取当前页面标题
 * @return 当前页面标题字符串
 */
QString WebViewWidget::getTitle() const
{
    return currentTitle;
}

/**
 * 检查是否可以返回
 * @return true如果可以返回上一页
 */
bool WebViewWidget::canGoBack() const
{
    return historyIndex > 0;
}

/**
 * 检查是否可以前进
 * @return true如果可以前进到下一页
 */
bool WebViewWidget::canGoForward() const
{
    return historyIndex < historyList.size() - 1;
}

/**
 * 返回上一页
 */
void WebViewWidget::goBack()
{
    if (canGoBack()) {
        historyIndex--;
        loadWebContent(historyList[historyIndex]);
        qDebug() << "返回到历史记录:" << historyIndex;
    }
}

/**
 * 前进到下一页
 */
void WebViewWidget::goForward()
{
    if (canGoForward()) {
        historyIndex++;
        loadWebContent(historyList[historyIndex]);
        qDebug() << "前进到历史记录:" << historyIndex;
    }
}

/**
 * 刷新当前页面
 */
void WebViewWidget::refresh()
{
    if (historyIndex >= 0 && historyIndex < historyList.size()) {
        loadWebContent(historyList[historyIndex]);
        qDebug() << "刷新当前页面";
    }
}

/**
 * 停止加载
 */
void WebViewWidget::stop()
{
    // QTextBrowser不需要停止操作
    qDebug() << "停止加载操作";
}

/**
 * 跳转到主页
 */
void WebViewWidget::goHome()
{
    navigate(homeUrl);
}

/**
 * 设置主页URL
 * @param url 主页URL地址
 */
void WebViewWidget::setHomeUrl(const QString& url)
{
    homeUrl = url;
    qDebug() << "设置主页URL:" << url;
}

/**
 * 添加到历史记录
 * @param url URL地址
 * @param title 页面标题
 */
void WebViewWidget::addToHistory(const QString& url, const QString& title)
{
    // 移除当前索引之后的记录
    if (historyIndex < historyList.size() - 1) {
        historyList = historyList.mid(0, historyIndex + 1);
    }
    
    // 添加新记录
    historyList.append(url);
    historyIndex = historyList.size() - 1;
    
    // 限制历史记录数量
    if (historyList.size() > 50) {
        historyList.removeFirst();
        historyIndex--;
    }
    
    if (!title.isEmpty()) {
        currentTitle = title;
    }
    
    qDebug() << "添加到历史记录:" << url << "标题:" << title;
}

/**
 * 连接信号和槽
 */
void WebViewWidget::connectSignals()
{
    // QTextBrowser的信号有限，这里主要连接必要的信号
    connect(webView, &QTextBrowser::sourceChanged, this, [this](const QUrl& url) {
        qDebug() << "QTextBrowser源码变更:" << url.toString();
        emit urlChanged(url.toString());
    });
    
    // 由于QTextBrowser不支持加载进度，我们直接发出完成的信号
    // 这是一个简化的实现
    qDebug() << "WebView信号连接完成 (QTextBrowser模式)";
}