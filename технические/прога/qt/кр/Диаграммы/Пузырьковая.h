#ifndef BUBLEDIAG_H
#define BUBLEDIAG_H

#include <QWidget>
#include <QVector>
#include <QPainter>
#include <QRandomGenerator>

class BubleDiag : public QWidget
{
    Q_OBJECT
public:
    explicit BubleDiag(QWidget *parent = nullptr) : QWidget(parent)
    {
        QVector <int> a(3);
        for (int i = 0; i < 5; ++i)
        {
            for (int j = 0; j < 3; ++j)
                a[j] = QRandomGenerator::global()->bounded(1, 11);
            vect.push_back(a);
        }

        painter = new QPainter();
    }
private:
    QVector <QVector<int>> vect;
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
            int r = qMin(dx, dy) * vect[i][2] / 5;
            painter->drawEllipse(vect[i][0] * dx - r / 2, -vect[i][1] * dy - r / 2, r, r);
            painter->drawText(QRect(vect[i][0] * dx + r / 2, -vect[i][1] * dy - r / 2, 50, 20),
                              "(" + QString::number(vect[i][0]) + ", " + QString::number(vect[i][1]) + ", " +
                                  QString::number(vect[i][2]) + ")");
        }
        painter->end();
    }
};

#endif // BUBLEDIAG_H
