#ifndef MARKERGRAPH_H
#define MARKERGRAPH_H

#include <QWidget>
#include <QVector>
#include <QPainter>
#include <QRandomGenerator>
#include <algorithm>

class MarkerGraph : public QWidget
{
    Q_OBJECT
public:
    explicit MarkerGraph(QWidget *parent = nullptr) : QWidget{parent}
    {
        for (int i = 0; i < 5; ++i)
            vect.push_back({QRandomGenerator::global()->bounded(1, 11),
                            QRandomGenerator::global()->bounded(1, 11)});

        std::sort(vect.begin(), vect.end());

        painter = new QPainter();
    }
private:
    QVector <QPair<int, int>> vect;
    QPainter *painter;
protected:
    void paintEvent(QPaintEvent *event) override
    {
        Q_UNUSED(event);
        int dx = width() / 15;
        int dy = height() / 15;
        painter->begin(this);
        painter->translate(width() / 10, 3 * height() / 4);
        for (int i = 0; i < 5; ++i)
        {
            if (i < 4)
                painter->drawLine(vect[i].first * dx, -vect[i].second * dy,
                                  vect[i + 1].first * dx, -vect[i + 1].second * dy);
            painter->drawEllipse(vect[i].first * dx - 4, -vect[i].second * dy - 4, 8, 8);
            painter->drawText(QRect(vect[i].first * dx + 4, -vect[i].second * dy - 4, 50, 20),
                              "(" + QString::number(vect[i].first) + ", " + QString::number(vect[i].second) + ")");
        }
        painter->end();
    }
};

#endif // MARKERGRAPH_H
