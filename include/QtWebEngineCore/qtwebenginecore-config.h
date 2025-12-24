// Qt WebEngine Core 配置文件
// 自动生成的配置文件

#ifndef QTWEBENGINECORE_CONFIG_H
#define QTWEBENGINECORE_CONFIG_H

#include <QtCore/qglobal.h>

// WebEngine 版本信息
#define QTWEBENGINECORE_VERSION_STR "6.4.2"
#define QTWEBENGINECORE_VERSION 0x060402

// 启用 WebEngine 功能
#define QT_FEATURE_webengine 1
#define QT_FEATURE_webengine_printing_and_pdf 1
#define QT_FEATURE_webengine_spellchecker 1
#define QT_FEATURE_webengine_webrtc 1
#define QT_FEATURE_webengine_geolocation 1

// 平台相关配置
#ifdef Q_OS_WIN
#define QT_FEATURE_webengine_win_internet_disposition 1
#endif

#endif // QTWEBENGINECORE_CONFIG_H
