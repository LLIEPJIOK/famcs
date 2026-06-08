#ifndef LINEARSTACKEDDIAG_H
#define LINEARSTACKEDDIAG_H

#include <QWidget>
#include <QVector>
#include <QMap>
#include <QPainter>
#include <QRandomGenerator>

class LinearStackedDiag : public QWidget
{
    Q_OBJECT
public:
    explicit LinearStackedDiag(QWidget *parent = nullptr) : QWidget(parent)
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
        int tmp;
        int w;
        painter->save();
        for (int i = 0; i < gist.size(); ++i)
        {
            tmp = gist[i].second["Алгебра"];
            w = tmp * width () / 50;
            painter->drawRect(0, height() / 15, w, height() / 20);
            painter->drawText(QRect(0, 0, w, height() / 15), Qt::AlignCenter, QString::number(tmp));

            tmp = gist[i].second["Геометрия"];
            painter->drawRect(w, height() / 15, tmp * width () / 50, height() / 20);
            painter->drawText(QRect(w, 0, tmp * width () / 50, height() / 15), Qt::AlignCenter,
                              QString::number(tmp));
            w += tmp * width () / 50;

            painter->drawRect(w, height() / 15, tmp * width () / 50, height() / 20);
            painter->drawText(QRect(w, 0, tmp * width () / 50, height() / 15), Qt::AlignCenter,
                              QString::number(tmp));

            painter->drawText(QRect(-5 - 8 * width() / 50, height() / 15, 8 * width() / 50, height() / 20),
                              Qt::AlignVCenter | Qt::AlignRight, gist[i].first);

            painter->translate(0, 12 * height() / 50);
        }
        painter->restore();

        tmp = 14 * height() / 45;
        painter->translate(width() / 2, tmp / 2);
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

#endif // LINEARSTACKEDDIAG_H
