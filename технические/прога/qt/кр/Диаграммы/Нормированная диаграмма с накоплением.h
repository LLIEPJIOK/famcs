#ifndef NORMSTACKGIST_H
#define NORMSTACKGIST_H

#include <QWidget>
#include <QVector>
#include <QPainter>
#include <QMap>
#include <QRandomGenerator>

class NormStackGist : public QWidget
{
    Q_OBJECT
public:
    explicit NormStackGist(QWidget *parent = nullptr) : QWidget{parent}
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
        painter->translate(5 * width() / 50, 3 * height() / 4);
        painter->save();
        int h;
        for (int i = 0; i < gist.size(); ++i)
        {
            int tmp1 = gist[i].second["Алгебра"];
            int tmp2 = gist[i].second["Геометрия"];
            int tmp3 = gist[i].second["Программирование"];
            int sum = tmp1 + tmp2 + tmp3;
            h = (qreal)-tmp1 / sum * 3 * height() / 5;
            painter->drawRect(0, h, width () / 25, -h);
            painter->drawText(QRect(width () / 25, h,  width() / 25, -h), Qt::AlignCenter,
                              QString::number(qRound(100. * tmp1 / sum)) + "%");

            painter->drawRect(0, h - (qreal)tmp2 / sum * 3 * height() / 5, width () / 25,
                              (qreal)tmp2 / sum * 3 * height() / 5);
            painter->drawText(QRect(width () / 25, h - (qreal)tmp2 / sum * 3 * height() / 5,
                                    width () / 25, (qreal)tmp2 / sum * 3 * height() / 5), Qt::AlignCenter,
                              QString::number(qRound(100. * tmp2 / sum)) + "%");
            h -= (qreal)tmp2 / sum * 3 * height() / 5;

            painter->drawRect(0, h - (qreal)tmp3 / sum * 3 * height() / 5, width () / 25,
                              (qreal)tmp3 / sum * 3 * height() / 5);
            painter->drawText(QRect(width () / 25, h - (qreal)tmp3 / sum * 3 * height() / 5,
                                    width () / 25, (qreal)tmp3 / sum * 3 * height() / 5), Qt::AlignCenter,
                              QString::number(qRound(100. * tmp3 / sum)) + "%");

            painter->drawText(QRect(-4 *  width() / 50, 0, 10 * width() / 50, 20), Qt::AlignCenter, gist[i].first);

            painter->translate(12 * width() / 50, 0);
        }
        painter->end();
    }
};

#endif // NORMSTACKGIST_H
