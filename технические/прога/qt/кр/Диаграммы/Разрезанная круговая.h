#ifndef SLICEDCIRCLEDIAG_H
#define SLICEDCIRCLEDIAG_H

#include <QWidget>
#include <QVector>
#include <QRandomGenerator>
#include <QPainter>
#include <algorithm>

class SlicedCircleDiag : public QWidget
{
    Q_OBJECT
public:
    explicit SlicedCircleDiag(QWidget *parent = nullptr) : QWidget{parent}
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
        for (int i = 0; i < 5; ++i)
        {
            qreal tmp = 360. * vect[i] / sum;
            painter->rotate(tmp / 2);
            painter->save();
            int r = qMin(width() / 16, height() / 10);
            painter->translate(r, 0);
            painter->drawPie(QRect(-2 * r, -2 * r, 4 * r, 4 * r), tmp * 8, -tmp * 16);
            angle += tmp / 2;
            painter->save();
            painter->translate(qMin(13 * width() / 80, 13 * height() / 50), 0);
            painter->rotate(-angle);
            painter->drawText(QRect(0, -10, 50, 20), QString::number(tmp / 36 * 10, 'g', 3) + "%");
            painter->restore();
            painter->restore();
            painter->rotate(tmp / 2);
            angle += tmp / 2;
        }
        painter->end();
    }
};

#endif // SLICEDCIRCLEDIAG_H
