#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QString>

#include "CarFlow.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    static QString generateLog(const std::vector<CarsPack>& temp);

public slots:
    void createPacks();

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
