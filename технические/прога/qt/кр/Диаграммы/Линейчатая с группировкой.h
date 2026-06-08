#ifndef LINIARGROUPDIAG_H
#define LINIARGROUPDIAG_H

#include <QWidget>
#include <QVector>
#include <QMap>
#include <QPainter>
#include <QRandomGenerator>

class LinearGroupDiag : public QWidget
{
    Q_OBJECT
public:
    explicit LinearGroupDiag(QWidget *parent = nullptr) : QWidget{parent}
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
        painter->save();
        for (int i = 0; i < gist.size(); ++i)
        {
            tmp = gist[i].second["Алгебра"];
            painter->drawRect(0, 0, tmp * width () / 25, height() / 20);
            painter->drawText(QRect(5 + tmp * width () / 25, 0,
                                    25, height() / 20), Qt::AlignVCenter | Qt::AlignLeft, QString::number(tmp));

            tmp = gist[i].second["Геометрия"];
            painter->drawRect(0, height() / 15, tmp * width () / 25, height() / 20);
            painter->drawText(QRect(5 + tmp * width () / 25, height() / 15,
                                    25, height() / 20), Qt::AlignVCenter | Qt::AlignLeft, QString::number(tmp));

            painter->drawRect(0, 2 * height() / 15, tmp * width () / 25, height() / 20);
            painter->drawText(QRect(5 + tmp * width () / 25, 2 *  height() / 15,
                                    25, height() / 20), Qt::AlignVCenter | Qt::AlignLeft, QString::number(tmp));

            painter->drawText(QRect(-5 - 8 * width() / 50, height() / 15, 8 * width() / 50, height() / 20),
                              Qt::AlignVCenter | Qt::AlignRight, gist[i].first);

            painter->translate(0, 12 * height() / 50);
        }
        painter->restore();
        painter->end();
    }
};

#endif // LINIARGROUPDIAG_H
