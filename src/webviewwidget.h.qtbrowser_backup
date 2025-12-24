#pragma once
#ifndef WEBVIEWWIDGET_H
#define WEBVIEWWIDGET_H

#include <QWidget>
#include <QVBoxLayout>
#include <QTextBrowser>
#include <QProgressBar>
#include <QLabel>
#include <QFile>
#include <QTextStream>
#include <QDir>
#include <QUrl>
#include <QStringList>

/**
 * WebView组件类 - 简化版WebView功能
 * 提供基本的网页显示功能，导航控制由MainWindow处理
 */
class WebViewWidget : public QWidget
{
    Q_OBJECT

public:
    /**
     * 构造函数 - 初始化WebView组件
     * @param parent 父窗口指针，默认为nullptr
     */
    explicit WebViewWidget(QWidget* parent = nullptr);

    /**
     * 析构函数 - 清理WebView资源
     */
    ~WebViewWidget() override;

    /**
     * 导航到指定URL
     * @param url 目标URL地址
     */
    void navigate(const QString& url);

    /**
     * 获取当前URL
     * @return 当前页面URL字符串
     */
    QString getCurrentUrl() const;

    /**
     * 获取当前页面标题
     * @return 当前页面标题字符串
     */
    QString getTitle() const;

    /**
     * 检查是否可以返回
     * @return true如果可以返回上一页
     */
    bool canGoBack() const;

    /**
     * 检查是否可以前进
     * @return true如果可以前进到下一页
     */
    bool canGoForward() const;

    /**
     * 返回上一页
     */
    void goBack();

    /**
     * 前进到下一页
     */
    void goForward();

    /**
     * 刷新当前页面
     */
    void refresh();

    /**
     * 停止加载
     */
    void stop();

    /**
     * 跳转到主页
     */
    void goHome();

    /**
     * 设置主页URL
     * @param url 主页URL地址
     */
    void setHomeUrl(const QString& url);

signals:
    /**
     * URL改变信号
     * @param url 新的URL地址
     */
    void urlChanged(const QString& url);

    /**
     * 页面标题改变信号
     * @param title 新的页面标题
     */
    void titleChanged(const QString& title);

    /**
     * 加载进度改变信号
     * @param progress 加载进度百分比 (0-100)
     */
    void loadProgress(int progress);

    /**
     * 开始加载信号
     * @param url 加载的URL
     */
    void loadStarted(const QString& url);

    /**
     * 加载完成信号
     * @param success 加载是否成功
     * @param url 加载的URL
     */
    void loadFinished(bool success, const QString& url);

private:
    /**
     * 初始化WebView设置
     */
    void setupWebView();

    /**
     * 连接信号和槽
     */
    void connectSignals();

    /**
     * 添加到历史记录
     * @param url 要添加的URL
     * @param title 页面标题
     */
    void addToHistory(const QString& url, const QString& title = QString());

    /**
     * 加载默认HTML内容
     */
    void loadDefaultHtml();

    /**
     * 加载网页内容
     * @param url 要加载的URL
     */
    void loadWebContent(const QString& url);

    /**
     * 加载本地HTML文件
     * @param filePath HTML文件路径
     * @return 是否加载成功
     */
    bool loadHtmlFile(const QString& filePath);

    /**
     * 显示网络内容限制提示
     * @param url 要加载的URL
     */
    void showNetworkLimitation(const QString& url);

    /**
     * 加载Data URL内容
     * @param dataUrl Data URL字符串
     */
    void loadDataUrl(const QString& dataUrl);

    /**
     * 加载文本内容
     * @param url 文件路径或文本内容
     */
    void loadTextContent(const QString& url);

    /**
     * 加载Markdown文件
     * @param filePath Markdown文件路径
     * @return 是否加载成功
     */
    bool loadMarkdownFile(const QString& filePath);

    /**
     * 加载纯文本文件
     * @param filePath 文本文件路径
     * @return 是否加载成功
     */
    bool loadPlainTextFile(const QString& filePath);

    /**
     * 简单的Markdown转HTML转换
     * @param markdown Markdown内容
     * @return 转换后的HTML内容
     */
    QString convertMarkdownToHtml(const QString& markdown);

private:
    // 主布局
    QVBoxLayout* mainLayout;
    
    // WebView组件
    QTextBrowser* webView;
    
    // 进度显示
    QProgressBar* progressBar;
    QLabel* statusLabel;
    
    // 配置
    QString homeUrl;
    bool isLoading;
    QString currentTitle;
    
    // 历史记录管理
    QStringList historyList;
    int historyIndex;
};

#endif // WEBVIEWWIDGET_H