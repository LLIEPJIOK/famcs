#ifndef STACKGIST_H
#define STACKGIST_H

#include <QWidget>
#include <QVector>
#include <QPainter>
#include <QMap>
#include <QRandomGenerator>

class StackGist : public QWidget
{
    Q_OBJECT
public:
    explicit StackGist(QWidget *parent = nullptr) : QWidget{parent}
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
            h = -tmp1 * height() / 40;
            painter->drawRect(0, h, width () / 25, -h);
            painter->drawText(QRect(width () / 25, h,  width() / 25, -h), Qt::AlignCenter,
                              QString::number(tmp1));

            int tmp2 = gist[i].second["Геометрия"];
            painter->drawRect(0, h - tmp2 * height() / 40, width () / 25, tmp2 * height() / 40);
            painter->drawText(QRect(width () / 25, h - tmp2 * height() / 40,
                                    width () / 25, tmp2 * height() / 40), Qt::AlignCenter, QString::number(tmp2));
            h -= tmp2 * height() / 40;

            int tmp3 = gist[i].second["Программирование"];
            painter->drawRect(0, h - tmp3 * height() / 40, width () / 25, tmp3 * height() / 40);
            painter->drawText(QRect(width () / 25, h - tmp3 * height() / 40,
                                    width () / 25, tmp3 * height() / 40), Qt::AlignCenter, QString::number(tmp3));

            painter->drawText(QRect(-4 *  width() / 50, 0, 10 * width() / 50, 20), Qt::AlignCenter, gist[i].first);

            painter->translate(12 * width() / 50, 0);
        }
        painter->end();
    }
};

#endif // STACKGIST_H
