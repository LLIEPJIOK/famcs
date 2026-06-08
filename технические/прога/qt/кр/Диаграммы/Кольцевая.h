#ifndef RINGDIAG_H
#define RINGDIAG_H

#include <QWidget>
#include <QVector>
#include <QRandomGenerator>
#include <QPainter>
#include <algorithm>

class RingDiag : public QWidget
{
    Q_OBJECT
public:
    explicit RingDiag(QWidget *parent = nullptr) : QWidget{parent}
    {
        for (int i = 0; i < 5; ++i)
            vect.push_back(QRandomGenerator::global()->bounded(1, 101));
        painter = new QPainter();
    }
private:
    QVector <int> vect;
    QPainter *painter;
protected:
    void paintEvent(QPaintEvent *event) override
    {
        Q_UNUSED(event);
        painter->begin(this);
        painter->setRenderHint(QPainter::Antialiasing);
        painter->translate(width() / 2, height() / 2);
        painter->rotate(-90);
        qreal angle = -90;
        int sum = std::accumulate(vect.cbegin(), vect.cend(), 0);
        int r = qMin(width() / 8, height() / 5);
        for (int i = 0; i < 5; ++i)
        {
            qreal tmp = 360. * vect[i] / sum;
            painter->setBrush(Qt::blue);
            painter->drawPie(QRect(-r, -r, 2 * r, 2 * r), 0, -tmp * 16);
            painter->rotate(tmp / 2);
            angle += tmp / 2;
            painter->save();
            painter->translate(qMin(13 * width() / 80, 13 * height() / 50), 0);
            painter->rotate(-angle);
            painter->drawText(QRect(0, -10, 50, 20), QString::number(qRound(tmp / 36 * 10)) + "%");
            painter->restore();
            painter->rotate(tmp / 2);
            angle += tmp / 2;
        }
        painter->setBrush(Qt::white); // скорее всего нужно будет palette().color(QPalette::Window)
        painter->drawEllipse(-r / 2, -r / 2, r, r);
        painter->end();
    }
};

#endif // RINGDIAG_H
