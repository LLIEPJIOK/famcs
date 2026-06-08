#ifndef DOTMARKERSDIAG_H
#define DOTMARKERSDIAG_H

#include <QWidget>
#include <QVector>
#include <QPainter>
#include <QRandomGenerator>

class DotMarkersDiag : public QWidget
{
    Q_OBJECT
public:
    explicit DotMarkersDiag(QWidget *parent = nullptr) : QWidget{parent}
    {
        for (int i = 0; i < 5; ++i)
            vect.push_back({QRandomGenerator::global()->bounded(1, 11),
                            QRandomGenerator::global()->bounded(1, 11)});

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
            painter->drawEllipse(vect[i].first * dx - 4, -vect[i].second * dy - 4, 8, 8);
            painter->drawText(QRect(vect[i].first * dx + 4, -vect[i].second * dy - 4, 50, 20),
                              "(" + QString::number(vect[i].first) + ", " + QString::number(vect[i].second) + ")");
        }
        painter->end();
    }
};

#endif // DOTMARKERSDIAG_H
