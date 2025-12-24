/****************************************************************************
** Meta object code from reading C++ file 'webviewwidget.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.14.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../src/webviewwidget.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'webviewwidget.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.14.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_WebViewWidget_t {
    QByteArrayData data[24];
    char stringdata0[248];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_WebViewWidget_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_WebViewWidget_t qt_meta_stringdata_WebViewWidget = {
    {
QT_MOC_LITERAL(0, 0, 13), // "WebViewWidget"
QT_MOC_LITERAL(1, 14, 12), // "titleChanged"
QT_MOC_LITERAL(2, 27, 0), // ""
QT_MOC_LITERAL(3, 28, 5), // "title"
QT_MOC_LITERAL(4, 34, 10), // "urlChanged"
QT_MOC_LITERAL(5, 45, 3), // "url"
QT_MOC_LITERAL(6, 49, 12), // "loadProgress"
QT_MOC_LITERAL(7, 62, 8), // "progress"
QT_MOC_LITERAL(8, 71, 12), // "loadFinished"
QT_MOC_LITERAL(9, 84, 2), // "ok"
QT_MOC_LITERAL(10, 87, 11), // "loadStarted"
QT_MOC_LITERAL(11, 99, 6), // "goBack"
QT_MOC_LITERAL(12, 106, 9), // "goForward"
QT_MOC_LITERAL(13, 116, 7), // "refresh"
QT_MOC_LITERAL(14, 124, 4), // "stop"
QT_MOC_LITERAL(15, 129, 10), // "setHomeUrl"
QT_MOC_LITERAL(16, 140, 6), // "goHome"
QT_MOC_LITERAL(17, 147, 7), // "copyUrl"
QT_MOC_LITERAL(18, 155, 20), // "openInDefaultBrowser"
QT_MOC_LITERAL(19, 176, 13), // "onLoadStarted"
QT_MOC_LITERAL(20, 190, 14), // "onLoadProgress"
QT_MOC_LITERAL(21, 205, 14), // "onLoadFinished"
QT_MOC_LITERAL(22, 220, 14), // "onTitleChanged"
QT_MOC_LITERAL(23, 235, 12) // "onUrlChanged"

    },
    "WebViewWidget\0titleChanged\0\0title\0"
    "urlChanged\0url\0loadProgress\0progress\0"
    "loadFinished\0ok\0loadStarted\0goBack\0"
    "goForward\0refresh\0stop\0setHomeUrl\0"
    "goHome\0copyUrl\0openInDefaultBrowser\0"
    "onLoadStarted\0onLoadProgress\0"
    "onLoadFinished\0onTitleChanged\0"
    "onUrlChanged"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_WebViewWidget[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
      18,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       5,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    1,  104,    2, 0x06 /* Public */,
       4,    1,  107,    2, 0x06 /* Public */,
       6,    1,  110,    2, 0x06 /* Public */,
       8,    1,  113,    2, 0x06 /* Public */,
      10,    0,  116,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
      11,    0,  117,    2, 0x0a /* Public */,
      12,    0,  118,    2, 0x0a /* Public */,
      13,    0,  119,    2, 0x0a /* Public */,
      14,    0,  120,    2, 0x0a /* Public */,
      15,    1,  121,    2, 0x0a /* Public */,
      16,    0,  124,    2, 0x0a /* Public */,
      17,    0,  125,    2, 0x0a /* Public */,
      18,    0,  126,    2, 0x0a /* Public */,
      19,    0,  127,    2, 0x08 /* Private */,
      20,    1,  128,    2, 0x08 /* Private */,
      21,    1,  131,    2, 0x08 /* Private */,
      22,    1,  134,    2, 0x08 /* Private */,
      23,    1,  137,    2, 0x08 /* Private */,

 // signals: parameters
    QMetaType::Void, QMetaType::QString,    3,
    QMetaType::Void, QMetaType::QString,    5,
    QMetaType::Void, QMetaType::Int,    7,
    QMetaType::Void, QMetaType::Bool,    9,
    QMetaType::Void,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::QString,    5,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,    7,
    QMetaType::Void, QMetaType::Bool,    9,
    QMetaType::Void, QMetaType::QString,    3,
    QMetaType::Void, QMetaType::QUrl,    5,

       0        // eod
};

void WebViewWidget::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<WebViewWidget *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->titleChanged((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 1: _t->urlChanged((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 2: _t->loadProgress((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 3: _t->loadFinished((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 4: _t->loadStarted(); break;
        case 5: _t->goBack(); break;
        case 6: _t->goForward(); break;
        case 7: _t->refresh(); break;
        case 8: _t->stop(); break;
        case 9: _t->setHomeUrl((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 10: _t->goHome(); break;
        case 11: _t->copyUrl(); break;
        case 12: _t->openInDefaultBrowser(); break;
        case 13: _t->onLoadStarted(); break;
        case 14: _t->onLoadProgress((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 15: _t->onLoadFinished((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 16: _t->onTitleChanged((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 17: _t->onUrlChanged((*reinterpret_cast< const QUrl(*)>(_a[1]))); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (WebViewWidget::*)(const QString & );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&WebViewWidget::titleChanged)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (WebViewWidget::*)(const QString & );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&WebViewWidget::urlChanged)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (WebViewWidget::*)(int );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&WebViewWidget::loadProgress)) {
                *result = 2;
                return;
            }
        }
        {
            using _t = void (WebViewWidget::*)(bool );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&WebViewWidget::loadFinished)) {
                *result = 3;
                return;
            }
        }
        {
            using _t = void (WebViewWidget::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&WebViewWidget::loadStarted)) {
                *result = 4;
                return;
            }
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject WebViewWidget::staticMetaObject = { {
    QMetaObject::SuperData::link<QWidget::staticMetaObject>(),
    qt_meta_stringdata_WebViewWidget.data,
    qt_meta_data_WebViewWidget,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *WebViewWidget::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *WebViewWidget::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_WebViewWidget.stringdata0))
        return static_cast<void*>(this);
    return QWidget::qt_metacast(_clname);
}

int WebViewWidget::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QWidget::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 18)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 18;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 18)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 18;
    }
    return _id;
}

// SIGNAL 0
void WebViewWidget::titleChanged(const QString & _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}

// SIGNAL 1
void WebViewWidget::urlChanged(const QString & _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 1, _a);
}

// SIGNAL 2
void WebViewWidget::loadProgress(int _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 2, _a);
}

// SIGNAL 3
void WebViewWidget::loadFinished(bool _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 3, _a);
}

// SIGNAL 4
void WebViewWidget::loadStarted()
{
    QMetaObject::activate(this, &staticMetaObject, 4, nullptr);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
