#ifndef STACKEDGRAPH_H
#define STACKEDGRAPH_H

#include <QWidget>
#include <QVector>
#include <QMap>
#include <QRandomGenerator>
#include <QPainter>

class StackedGraph : public QWidget
{
    Q_OBJECT
public:
    explicit StackedGraph(QWidget *parent = nullptr) : QWidget{parent}
    {
        QVector<int> a;
        for (int i = 0; i < 5; ++i)
            a.push_back(QRandomGenerator::global()->bounded(1, 11));
        std::sort(a.begin(), a.end());
        QVector <QPair<int, int>> vect;
        for (int i = 0; i < 3; ++i)
        {
            vect.clear();
            for (int j = 0; j < 5; ++j)
                vect.push_back({a[j], QRandomGenerator::global()->bounded(1, 11)});
            mp[i] = vect;
        }

        painter = new QPainter();
    }
private:
    QMap<int, QVector<QPair<int, int>>> mp;
    QPainter *painter;
protected:
    void paintEvent(QPaintEvent *event) override
    {
        Q_UNUSED(event);
        int dx = width() / 15;
        int dy = height() / 35;
        painter->begin(this);
        painter->translate(width() / 10, 9 * height() / 10);
        for (int i = 0; i < 5; ++i)
        {
            painter->drawText(QRect(mp[0][i].first * dx + 4, -mp[0][i].second * dy - 4, 50, 20),
                              "(" + QString::number(mp[0][i].first) + ", " + QString::number(mp[0][i].second) + ")");
            painter->drawText(QRect(mp[0][i].first * dx + 4,
                                    -(mp[0][i].second + mp[1][i].second) * dy - 4, 50, 20),
                              "(" + QString::number(mp[1][i].first) + ", " + QString::number(mp[1][i].second) + ")");
            painter->drawText(QRect(mp[0][i].first * dx + 4,
                                    -(mp[0][i].second + mp[1][i].second + mp[2][i].second) * dy - 4, 50, 20),
                              "(" + QString::number(mp[2][i].first) + ", " + QString::number(mp[2][i].second) + ")");
            if (i < 4)
            {
                painter->drawLine(mp[0][i].first * dx, -mp[0][i].second * dy,
                                  mp[0][i + 1].first * dx, -mp[0][i + 1].second * dy);
                painter->drawLine(mp[0][i].first * dx, -(mp[0][i].second + mp[1][i].second) * dy,
                                  mp[0][i + 1].first * dx, -(mp[0][i + 1].second + mp[1][i + 1].second) * dy);
                painter->drawLine(mp[0][i].first * dx,
                                  -(mp[0][i].second + mp[1][i].second + mp[2][i].second) * dy,
                                  mp[0][i + 1].first * dx,
                                  -(mp[0][i + 1].second + mp[1][i + 1].second + mp[2][i + 1].second) * dy);
            }
        }
        painter->end();
    }
};

#endif // STACKEDGRAPH_H
