#pragma once
#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QToolBar>
#include <QAction>
#include <QComboBox>
#include <QLineEdit>
#include <QLabel>
#include <QProgressBar>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QWidget>
#include <QMenu>
#include <QMenuBar>

class WebViewWidget;

/**
 * 主窗口类 - 实现Qt6工具栏和WebView集成
 * 包含地址栏、导航按钮、工具栏等功能
 */
class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    /**
     * 构造函数 - 初始化主窗口
     * @param parent 父窗口指针，默认为nullptr
     */
    explicit MainWindow(QWidget* parent = nullptr);

    /**
     * 析构函数 - 清理资源
     */
    ~MainWindow() override;

private slots:
    /**
     * 槽函数 - 导航到指定URL
     */
    void navigateToUrl();

    /**
     * 槽函数 - 返回上一页
     */
    void goBack();

    /**
     * 槽函数 - 返回下一页
     */
    void goForward();

    /**
     * 槽函数 - 刷新当前页面
     */
    void refresh();

    /**
     * 槽函数 - 停止加载
     */
    void stop();

    /**
     * 槽函数 - 主页按钮
     */
    void goHome();

    /**
     * 槽函数 - 地址栏文本改变
     * @param text 新的地址栏文本
     */
    void onUrlChanged(const QString& text);

    /**
     * 槽函数 - 网页标题改变
     * @param title 新的网页标题
     */
    void onTitleChanged(const QString& title);

    /**
     * 槽函数 - 加载进度改变
     * @param progress 加载进度百分比
     */
    void onLoadProgress(int progress);

    /**
     * 槽函数 - 关于对话框
     */
    void about();

    /**
     * 槽函数 - 退出应用
     */
    void exitApp();

private:
    /**
     * 初始化UI界面
     */
    void setupUi();

    /**
     * 创建工具栏和菜单
     */
    void createToolbarsAndMenus();

    /**
     * 创建WebView组件
     */
    void createWebView();

    /**
     * 连接信号和槽
     */
    void connectSignals();

    /**
     * 更新工具栏状态
     */
    void updateToolBarState();

protected:
    /**
     * 重写关闭事件 - 处理应用退出
     * @param event 关闭事件
     */
    void closeEvent(QCloseEvent* event) override;

private:
    // UI组件
    QWidget* centralWidget;
    QVBoxLayout* mainLayout;
    QHBoxLayout* navigationLayout;
    
    // 工具栏组件
    QToolBar* mainToolBar;
    QAction* backAction;
    QAction* forwardAction;
    QAction* refreshAction;
    QAction* stopAction;
    QAction* homeAction;
    
    // 导航组件
    QLineEdit* urlEdit;
    QLabel* statusLabel;
    QProgressBar* progressBar;
    
    // 菜单组件
    QMenuBar* menuBar;
    QMenu* fileMenu;
    QMenu* editMenu;
    QMenu* viewMenu;
    QMenu* helpMenu;
    
    // WebView组件
    WebViewWidget* webViewWidget;
    
    // 状态管理
    bool isLoading;
};

#endif // MAINWINDOW_H