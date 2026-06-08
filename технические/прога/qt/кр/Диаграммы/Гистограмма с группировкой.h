#ifndef GROUPGIST_H
#define GROUPGIST_H

#include <QWidget>
#include <QVector>
#include <QPainter>
#include <QMap>
#include <QRandomGenerator>

class GroupGist : public QWidget
{
    Q_OBJECT
public:
    explicit GroupGist(QWidget *parent = nullptr) : QWidget(parent)
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
        painter->translate(3 * width () / 50, 2 * height() / 3);
        painter->save();
        int tmp;
        for (int i = 0; i < gist.size(); ++i)
        {
            tmp = gist[i].second["Алгебра"];
            painter->drawRect(0, -tmp * height() / 20, width () / 25, tmp * height() / 20);
            painter->drawText(QRect(0, -tmp * height() / 20 - 20,
                                    width () / 25, 20), Qt::AlignHCenter | Qt::AlignBottom, QString::number(tmp));

            tmp = gist[i].second["Геометрия"];
            painter->drawRect(3 * width() / 50, -tmp * height() / 20, width () / 25, tmp * height() / 20);
            painter->drawText(QRect(3 * width() / 50, -tmp * height() / 20 - 20,
                                    width () / 25, 20), Qt::AlignHCenter | Qt::AlignBottom, QString::number(tmp));

            tmp = gist[i].second["Программирование"];
            painter->drawRect(6 * width() / 50, -tmp * height() / 20, width () / 25, tmp * height() / 20);
            painter->drawText(QRect(6 * width() / 50, -tmp * height() / 20 - 20,
                                    width () / 25, 20), Qt::AlignHCenter | Qt::AlignBottom, QString::number(tmp));

            painter->drawText(QRect(0, 0, 8 * width() / 50, 20), Qt::AlignCenter, gist[i].first);

            painter->translate(12 * width() / 50, 0);
        }
        painter->end();
    }
};

#endif // GROUPGIST_H
