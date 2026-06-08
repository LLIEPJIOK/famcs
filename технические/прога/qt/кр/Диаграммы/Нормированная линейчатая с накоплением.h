#ifndef NORMLINEARSTACKEDDIAG_H
#define NORMLINEARSTACKEDDIAG_H

#include <QWidget>
#include <QVector>
#include <QMap>
#include <QPainter>
#include <QRandomGenerator>

class NormLinearStackedDiag : public QWidget
{
    Q_OBJECT
public:
    explicit NormLinearStackedDiag(QWidget *parent = nullptr) : QWidget{parent}
    {
        QMap<QString, int> mp;

        mp["Алгебра"] = QRandomGenerator::global()->bounded(1, 11);
        mp["Геометрия"] = QRandomGenerator::global()->bounded(1, 11);
        mp["Программирование"] = QRandomGenerator::global()->bounded(1, 11);
        gist.push_back(qMakePair("Первый", mp));

        mp["Алгебра"] = QRandomGenerator::global()->bounded(1, 11);
        mp["Геометрия"] = QRandomGenerator::global()->bounded(1, 11);
        mp["Программирование"] = QRandomGenerator::global()->bounded(1, 11);
        gist.push_back(qMakePair("Второй", mp));

        mp["Алгебра"] = QRandomGenerator::global()->bounded(1, 11);
        mp["Геометрия"] = QRandomGenerator::global()->bounded(1, 11);
        mp["Программирование"] = QRandomGenerator::global()->bounded(1, 11);
        gist.push_back(qMakePair("Третий", mp));

        mp["Алгебра"] = QRandomGenerator::global()->bounded(1, 11);
        mp["Геометрия"] = QRandomGenerator::global()->bounded(1, 11);
        mp["Программирование"] = QRandomGenerator::global()->bounded(1, 11);
        gist.push_back(qMakePair("Четвёртый", mp));

        painter = new QPainter();
    }
private:
    QVector <QPair<QString, QMap<QString, qint32>>> gist;
    QPainter *painter;
protected:
    void paintEvent(QPaintEvent *event) override
    {
        Q_UNUSED(event);
        painter->begin(this);
        painter->setRenderHint(QPainter::Antialiasing);
        painter->translate(width () / 10, height() / 15);
        qreal w;
        painter->save();
        for (int i = 0; i < gist.size(); ++i)
        {
            int tmp1 = gist[i].second["Алгебра"];
            int tmp2 = gist[i].second["Геометрия"];
            int tmp3 = gist[i].second["Программирование"];
            int sum = tmp1 + tmp2 + tmp3;
            w = (qreal)tmp1 / sum * width() / 2;
            painter->drawRect(0, height() / 15, w, height() / 20);
            painter->drawText(QRect(0, 0, w, height() / 15), Qt::AlignCenter,
                              QString::number(100. * tmp1 / sum, 'g', 3) + "%");

            painter->drawRect(w, height() / 15, (qreal)tmp2 / sum * width() / 2, height() / 20);
            painter->drawText(QRect(w, 0, (qreal)tmp2 / sum * width() / 2, height() / 15), Qt::AlignCenter,
                              QString::number(100. * tmp2 / sum, 'g', 3) + "%");
            w += (qreal)tmp2 / sum * width() / 2;

            painter->drawRect(w, height() / 15, (qreal)tmp3 / sum * width() / 2, height() / 20);
            painter->drawText(QRect(w, 0, (qreal)tmp3 / sum * width() / 2, height() / 15), Qt::AlignCenter,
                              QString::number(100. * tmp3 / sum, 'g', 3) + "%");

            painter->drawText(QRect(-5 - 8 * width() / 50, height() / 15, 8 * width() / 50, height() / 20),
                              Qt::AlignVCenter | Qt::AlignRight, gist[i].first);

            painter->translate(0, 12 * height() / 50);
        }
        painter->restore();

        int tmp = 14 * height() / 45;
        painter->translate(width() / 1.5, tmp / 2);
        painter->drawRect(-5, -5, 10, 10);
        painter->drawText(QRect(8, -10, 200, 20), Qt::AlignVCenter, "Алгебра (слева)");

        painter->translate(0, tmp);
        painter->drawRect(-5, -5, 10, 10);
        painter->drawText(QRect(8, -10, 200, 20), Qt::AlignVCenter, "Геометрия (по центру)");

        painter->translate(0, tmp);
        painter->drawRect(-5, -5, 10, 10);
        painter->drawText(QRect(8, -10, 200, 20), Qt::AlignVCenter, "Программирование (справа)");
        painter->end();
    }
};

#endif // NORMLINEARSTACKEDDIAG_H
