#ifndef WEBVIEWWIDGET_H
#define WEBVIEWWIDGET_H

#include <QWidget>
#include <QUrl>
#include <QString>

// 前向声明
QT_BEGIN_NAMESPACE
class QWebEngineView;
QT_END_NAMESPACE

class WebViewWidget : public QWidget
{
    Q_OBJECT
    
public:
    explicit WebViewWidget(QWidget *parent = nullptr);
    ~WebViewWidget() override;
    
    void loadUrl(const QString &url);
    void navigate(const QString &url);  // 添加navigate方法
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
    void loadStarted();  // 添加loadStarted信号
    
private slots:
    void onLoadStarted();
    void onLoadProgress(int progress);
    void onLoadFinished(bool ok);
    void onTitleChanged(const QString &title);
    void onUrlChanged(const QUrl &url);
    
private:
    QWebEngineView *m_webView;
    QString m_homeUrl;
    QString m_currentUrl;
    QString m_currentTitle;
    
    void setupUI();
    void setupConnections();
    QString generateWelcomePage();
};

#endif // WEBVIEWWIDGET_H
