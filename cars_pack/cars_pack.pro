QT       += core gui widgets printsupport

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

INCLUDEPATH += \
    include \
    thirdparty/qcustomplot

HEADERS += \
    include/CarFlow.h \
    include/MainWindow.h \
    include/ModelBartlet.h \
    include/ModelPoisson.h \
    include/RandomGenerator.h \
    thirdparty/qcustomplot/qcustomplot.h

SOURCES += \
    src/CarFlow.cpp \
    src/MainWindow.cpp \
    src/ModelBartlet.cpp \
    src/ModelPoisson.cpp \
    src/RandomGenerator.cpp \
    src/main.cpp \
    thirdparty/qcustomplot/qcustomplot.cpp

FORMS += \
    ui/MainWindow.ui

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
