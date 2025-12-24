#include "mainwindow.h"
#include "webviewwidget.h"
#include <QApplication>
#include <QGuiApplication>
#include <QClipboard>
#include <QAction>
#include <QKeySequence>
#include <QIcon>
#include <QFile>
#include <QTextStream>
#include <QMessageBox>
#include <QCloseEvent>
#include <QScreen>
#include <QStandardPaths>
#include <QDir>
#include <QSettings>
#include <QToolButton>
#include <QDebug>

/**
 * 构造函数 - 初始化主窗口和UI组件
 * @param parent 父窗口指针
 */
MainWindow::MainWindow(QWidget* parent)
    : QMainWindow(parent)
    , centralWidget(nullptr)
    , mainLayout(nullptr)
    , navigationLayout(nullptr)
    , mainToolBar(nullptr)
    , backAction(nullptr)
    , forwardAction(nullptr)
    , refreshAction(nullptr)
    , stopAction(nullptr)
    , homeAction(nullptr)
    , urlEdit(nullptr)
    , statusLabel(nullptr)
    , progressBar(nullptr)
    , menuBar(nullptr)
    , fileMenu(nullptr)
    , editMenu(nullptr)
    , viewMenu(nullptr)
    , helpMenu(nullptr)
    , webViewWidget(nullptr)
    , isLoading(false)
{
    // 设置窗口属性
    setWindowTitle("Qt6 WebView工具栏示例 - 欢迎使用");
    setMinimumSize(800, 600);
    
    // 初始化UI
    setupUi();
    createToolbarsAndMenus();
    createWebView();
    connectSignals();
    
    // 设置默认主页
    webViewWidget->setHomeUrl("https://www.funnyai.com");
    
    qDebug() << "主窗口已初始化";
}

/**
 * 析构函数 - 清理资源
 */
MainWindow::~MainWindow()
{
    qDebug() << "主窗口正在关闭";
}

/**
 * 初始化用户界面
 */
void MainWindow::setupUi()
{
    // 创建中央控件
    centralWidget = new QWidget(this);
    setCentralWidget(centralWidget);
    
    // 创建主布局
    mainLayout = new QVBoxLayout(centralWidget);
    mainLayout->setSpacing(0);
    mainLayout->setContentsMargins(0, 0, 0, 0);
    
    // 状态标签 - 减小尺寸
    statusLabel = new QLabel("就绪");
    statusLabel->setMinimumWidth(80);
    statusLabel->setMaximumWidth(120);
    statusLabel->setStyleSheet("QLabel { padding: 1px 4px; font-size: 11px; color: #666; }");
    
    // 进度条 - 减小高度
    progressBar = new QProgressBar();
    progressBar->setVisible(false);
    progressBar->setMaximumHeight(12);
    progressBar->setMinimumWidth(150);
    progressBar->setMaximumWidth(200);
    progressBar->setStyleSheet("QProgressBar { border: none; background: transparent; text-align: center; } QProgressBar::chunk { background-color: #0078d4; }");
    
    qDebug() << "UI界面已设置完成";
}

/**
 * 创建工具栏和菜单
 */
void MainWindow::createToolbarsAndMenus()
{
    // 创建操作图标（使用默认图标）
    QIcon backIcon = style()->standardIcon(QStyle::SP_ArrowBack);
    QIcon forwardIcon = style()->standardIcon(QStyle::SP_ArrowForward);
    QIcon refreshIcon = style()->standardIcon(QStyle::SP_BrowserReload);
    QIcon stopIcon = style()->standardIcon(QStyle::SP_BrowserStop);
    QIcon homeIcon = style()->standardIcon(QStyle::SP_DialogApplyButton);
    
    // 创建工具栏操作
    backAction = new QAction(backIcon, "返回(&B)", this);
    backAction->setShortcut(QKeySequence::Back);
    backAction->setEnabled(false);
    connect(backAction, &QAction::triggered, this, &MainWindow::goBack);
    
    forwardAction = new QAction(forwardIcon, "前进(&F)", this);
    forwardAction->setShortcut(QKeySequence::Forward);
    forwardAction->setEnabled(false);
    connect(forwardAction, &QAction::triggered, this, &MainWindow::goForward);
    
    refreshAction = new QAction(refreshIcon, "刷新(&R)", this);
    refreshAction->setShortcut(QKeySequence::Refresh);
    connect(refreshAction, &QAction::triggered, this, &MainWindow::refresh);
    
    stopAction = new QAction(stopIcon, "停止(&S)", this);
    stopAction->setShortcut(QKeySequence::Cancel);
    stopAction->setEnabled(false);
    connect(stopAction, &QAction::triggered, this, &MainWindow::stop);
    
    homeAction = new QAction(homeIcon, "主页(&H)", this);
    homeAction->setShortcut(QKeySequence::HelpContents);
    connect(homeAction, &QAction::triggered, this, &MainWindow::goHome);
    
    // 地址栏 - 增加宽度
    urlEdit = new QLineEdit();
    urlEdit->setPlaceholderText("输入网址...");
    urlEdit->setMinimumWidth(500);
    urlEdit->setMaximumWidth(800);
    urlEdit->setText("https://www.funnyai.com");
    urlEdit->setStyleSheet("QLineEdit { padding: 4px 8px; border: 1px solid #ccc; border-radius: 4px; }");
    connect(urlEdit, &QLineEdit::returnPressed, this, &MainWindow::navigateToUrl);
    
    // 创建主工具栏并添加控件
    mainToolBar = addToolBar("主工具栏");
    mainToolBar->setMovable(false);
    mainToolBar->setFloatable(false);
    mainToolBar->setStyleSheet("QToolBar { spacing: 4px; padding: 2px; }");
    mainToolBar->addAction(backAction);
    mainToolBar->addAction(forwardAction);
    mainToolBar->addSeparator();
    mainToolBar->addAction(refreshAction);
    mainToolBar->addAction(stopAction);
    mainToolBar->addSeparator();
    mainToolBar->addAction(homeAction);
    mainToolBar->addSeparator();
    mainToolBar->addWidget(urlEdit);
    
    // 创建菜单栏
    menuBar = new QMenuBar(this);
    setMenuBar(menuBar);
    
    // 文件菜单
    fileMenu = menuBar->addMenu("文件(&F)");
    QAction* exitAction = new QAction("退出(&X)", this);
    exitAction->setShortcut(QKeySequence::Quit);
    connect(exitAction, &QAction::triggered, this, &MainWindow::exitApp);
    fileMenu->addAction(exitAction);
    
    // 编辑菜单
    editMenu = menuBar->addMenu("编辑(&E)");
    QAction* copyAction = new QAction("复制(&C)", this);
    copyAction->setShortcut(QKeySequence::Copy);
    connect(copyAction, &QAction::triggered, [this]() {
        if (webViewWidget) {
            // 复制当前URL
            QClipboard* clipboard = QApplication::clipboard();
            clipboard->setText(webViewWidget->getCurrentUrl());
            statusLabel->setText("URL已复制");
        }
    });
    editMenu->addAction(copyAction);
    
    // 视图菜单
    viewMenu = menuBar->addMenu("视图(&V)");
    QAction* fullscreenAction = new QAction("全屏(&F)", this);
    fullscreenAction->setShortcut(QKeySequence::FullScreen);
    connect(fullscreenAction, &QAction::triggered, [this]() {
        if (isFullScreen()) {
            showNormal();
        } else {
            showFullScreen();
        }
    });
    viewMenu->addAction(fullscreenAction);
    
    // 帮助菜单
    helpMenu = menuBar->addMenu("帮助(&H)");
    QAction* aboutAction = new QAction("关于(&A)", this);
    connect(aboutAction, &QAction::triggered, this, &MainWindow::about);
    helpMenu->addAction(aboutAction);
    
    QAction* aboutQtAction = new QAction("关于Qt(&Q)", this);
    connect(aboutQtAction, &QAction::triggered, []() {
        QMessageBox::aboutQt(nullptr, "关于Qt");
    });
    helpMenu->addAction(aboutQtAction);
    
    qDebug() << "工具栏和菜单已创建";
}

/**
 * 创建WebView组件
 */
void MainWindow::createWebView()
{
    webViewWidget = new WebViewWidget(this);
    mainLayout->addWidget(webViewWidget);
    
    // 设置WebView的伸缩因子，让它占据更多空间
    mainLayout->setStretchFactor(webViewWidget, 1);
    
    // 在布局底部添加状态栏组件 - 减小高度
    QWidget* statusWidget = new QWidget();
    statusWidget->setMaximumHeight(22);
    statusWidget->setStyleSheet("QWidget { background-color: #f5f5f5; border-top: 1px solid #e0e0e0; }");
    
    QHBoxLayout* statusLayout = new QHBoxLayout(statusWidget);
    statusLayout->setContentsMargins(8, 2, 12, 2);
    statusLayout->setSpacing(8);
    statusLayout->addWidget(statusLabel);
    statusLayout->addStretch();
    statusLayout->addWidget(progressBar);
    
    mainLayout->addWidget(statusWidget);
    
    qDebug() << "WebView组件已创建";
}

/**
 * 连接信号和槽
 */
void MainWindow::connectSignals()
{
    // 连接WebView信号
    if (webViewWidget) {
        connect(webViewWidget, &WebViewWidget::urlChanged, 
                this, &MainWindow::onUrlChanged);
        connect(webViewWidget, &WebViewWidget::titleChanged, 
                this, &MainWindow::onTitleChanged);
        connect(webViewWidget, &WebViewWidget::loadProgress, 
                this, &MainWindow::onLoadProgress);
        connect(webViewWidget, &WebViewWidget::loadStarted, 
                [this]() {
                    isLoading = true;
                    updateToolBarState();
                    statusLabel->setText("正在加载...");
                });
        connect(webViewWidget, &WebViewWidget::loadFinished, 
                [this](bool success) {
                    isLoading = false;
                    updateToolBarState();
                    statusLabel->setText(success ? "加载完成" : "加载失败");
                });
    }
    
    qDebug() << "信号和槽连接完成";
}

/**
 * 导航到指定URL
 */
void MainWindow::navigateToUrl()
{
    QString urlText = urlEdit->text().trimmed();
    if (urlText.isEmpty()) {
        return;
    }
    
    // 如果输入的文本不包含协议，添加https://
    if (!urlText.contains("://")) {
        urlText = "https://" + urlText;
    }
    
    // 使用WebViewWidget导航
    if (webViewWidget) {
        webViewWidget->navigate(urlText);
    }
    
    qDebug() << "导航到URL:" << urlText;
}

/**
 * 返回上一页
 */
void MainWindow::goBack()
{
    if (webViewWidget) {
        webViewWidget->goBack();
    }
}

/**
 * 前进到下一页
 */
void MainWindow::goForward()
{
    if (webViewWidget) {
        webViewWidget->goForward();
    }
}

/**
 * 刷新当前页面
 */
void MainWindow::refresh()
{
    if (webViewWidget) {
        webViewWidget->refresh();
    }
}

/**
 * 停止加载
 */
void MainWindow::stop()
{
    if (webViewWidget) {
        webViewWidget->stop();
    }
}

/**
 * 主页按钮
 */
void MainWindow::goHome()
{
    if (webViewWidget) {
        webViewWidget->goHome();
    }
}

/**
 * 地址栏文本改变
 */
void MainWindow::onUrlChanged(const QString& url)
{
    if (urlEdit && urlEdit->text() != url) {
        urlEdit->setText(url);
    }
}

/**
 * 网页标题改变
 */
void MainWindow::onTitleChanged(const QString& title)
{
    if (!title.isEmpty()) {
        setWindowTitle("Qt6 WebView - " + title);
    }
}

/**
 * 加载进度改变
 */
void MainWindow::onLoadProgress(int progress)
{
    if (progressBar) {
        if (progress > 0 && progress < 100) {
            progressBar->setVisible(true);
            progressBar->setValue(progress);
            progressBar->setFormat("加载中... %p%");
        } else {
            progressBar->setVisible(false);
        }
    }
}

/**
 * 更新工具栏状态
 */
void MainWindow::updateToolBarState()
{
    if (webViewWidget) {
        if (backAction) {
            backAction->setEnabled(webViewWidget->canGoBack());
        }
        if (forwardAction) {
            forwardAction->setEnabled(webViewWidget->canGoForward());
        }
        if (stopAction) {
            stopAction->setEnabled(isLoading);
        }
    }
}

/**
 * 关于对话框
 */
void MainWindow::about()
{
    QMessageBox::about(this, "关于", 
        "Qt6 WebView工具栏示例\n\n"
        "本程序演示了如何使用Qt6创建带工具栏的WebView应用程序。\n\n"
        "功能特性：\n"
        "• 工具栏导航控制\n"
        "• URL地址栏\n"
        "• 页面加载进度显示\n"
        "• 历史记录管理\n\n"
        "技术栈：\n"
        "• Qt6 Widgets\n"
        "• Conan包管理\n"
        "• SCons构建系统");
}

/**
 * 退出应用
 */
void MainWindow::exitApp()
{
    close();
}

/**
 * 窗口关闭事件处理
 */
void MainWindow::closeEvent(QCloseEvent* event)
{
    // 保存窗口设置
    QSettings settings("QtWebView", "MainWindow");
    settings.setValue("geometry", saveGeometry());
    settings.setValue("windowState", saveState());
    
    QMainWindow::closeEvent(event);
}