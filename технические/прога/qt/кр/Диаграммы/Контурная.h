#ifndef CONTOURDIAG_H
#define CONTOURDIAG_H

#include <QWidget>
#include <QPainter>
#include <QVector>
#include <QRandomGenerator>

class ContourDiag : public QWidget
{
    Q_OBJECT
public:
    explicit ContourDiag(QWidget *parent = nullptr) : QWidget{parent}
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
    QPainter *painter;
    QVector <QVector<int>> vect;
protected:
    void paintEvent(QPaintEvent* event) override
    {
        Q_UNUSED(event);
        int dx = width() / 25;
        int dy = height() / 25;
        painter->begin(this);
        painter->translate(width() / 10, 3 * height() / 4);
        QColor col = Qt::blue;
        for (int i = 0; i < 5; ++i)
        {
            col.setAlpha(255. * vect[i][2] / 10);
            painter->setBrush(col);
            painter->drawEllipse(vect[i][0] * dx - 50, -vect[i][1] * dy - 50, 100, 100);
            painter->drawText(QRect(vect[i][0] * dx + 50, -vect[i][1] * dy - 50, 50, 20),
                              "(" + QString::number(vect[i][0]) + ", " + QString::number(vect[i][1]) + ", " +
                                  QString::number(vect[i][2]) + ")");
        }
        painter->end();
    }
};

#endif // CONTOURDIAG_H
