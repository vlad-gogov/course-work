#include "MainWindow.h"
#include "ui_mainwindow.h"

#include <QString>
#include <QVector>
#include <QPushButton>

#include "CarFlow.h"

using namespace QCP;

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), ui(new Ui::MainWindow) {
    ui->setupUi(this);

    connect(ui->button_create_pack, &QPushButton::clicked, this, &MainWindow::createPacks);
}

MainWindow::~MainWindow() {
    delete ui;
}

void MainWindow::createPacks() {
    double lambda = ui->spinner_lambda->value();
    double time = ui->spinner_time->value();
    double r = ui->spinner_r->value();
    double g = ui->spinner_g->value();

    CarFlow flow(lambda, time, r, g);

    std::vector<CarsPack> packs = flow.createFlow();

    ui->text_log->clear();
    ui->text_log->appendPlainText(generateLog(packs));


    QVector<double> cars;

    for (const auto& pack : packs) {
        for (const auto& car : pack.second) {
            cars.push_back(car);
        }
    }

    QVector<double> y(cars.size(), 0);

    QCPScatterStyle style(QCPScatterStyle::ssSquare, Qt::red, Qt::red, 5);

    for (int i = 0; i < ui->graph->graphCount(); i++)
        ui->graph->removeGraph(i);

    ui->graph->addGraph();
    ui->graph->graph(0)->setData({0, flow.getTime()}, {0, 0});
    ui->graph->graph(0)->setPen(QPen(Qt::black));

    ui->graph->addGraph();
    ui->graph->graph(1)->setData(cars, y);
    ui->graph->graph(1)->setPen(QPen(Qt::black));
    ui->graph->graph(1)->setScatterStyle(style);
    ui->graph->xAxis->setLabel("t");
    //ui->graph->yAxis->axisRect()->setRangeDrag(Qt::Horizontal);
    ui->graph->yAxis->setVisible(false);
    ui->graph->graph(1)->rescaleAxes();
    ui->graph->setInteractions(QCP::iRangeDrag | QCP::iRangeZoom | QCP::iSelectPlottables);
    ui->graph->replot();

}

QString MainWindow::generateLog(const std::vector<CarsPack>& temp) {
    QString result;
    size_t count_pack = temp.size();
    for (size_t i = 0; i < count_pack; i++) {
        size_t size_pack = temp[i].first;
        result += "#" + QString::number(i + 1) + " pack: ";
        result += QString::number(temp[i].second[0], 'g', 6);
        for (size_t j = 1; j < size_pack; j++) {
            result += ", " + QString::number(temp[i].second[j], 'g', 6);
        }
        result += "\n";
    }
    return result;
}
