// main.cpp - Qt6工具栏+Widgets示例程序入口点
#include <QApplication>
#include <QCoreApplication>
#include <iostream>
#include <windows.h>
#include "mainwindow.h"

int main(int argc, char *argv[])
{
    // 设置Windows控制台编码为UTF-8
    SetConsoleOutputCP(65001);
    SetConsoleCP(65001);
    
    // 设置高DPI缩放支持
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
    QCoreApplication::setAttribute(Qt::AA_UseHighDpiPixmaps);

    QApplication app(argc, argv);

    // 设置应用程序信息
    QCoreApplication::setOrganizationName("Qt演示");
    QCoreApplication::setApplicationName("Qt6工具栏演示");
    QCoreApplication::setApplicationVersion("1.0.0");

    // 创建主窗口
    MainWindow window;
    window.show();

    return app.exec();
}