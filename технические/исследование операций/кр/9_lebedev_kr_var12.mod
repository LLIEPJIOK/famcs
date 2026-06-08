set ITEMS;
param value{ITEMS} >= 0;

# x[i] = 1, если предмет i получает —ын 1
# x[i] = 0, если предмет i получает —ын 2
var x{ITEMS} binary;

param TotalValue := sum{i in ITEMS} value[i];

# s Ч суммарна€ стоимость доли —ына 1
var s;

# z Ч модуль разницы между дол€ми
var z >= 0;

s.t. def_s:
    s = sum{i in ITEMS} value[i] * x[i];

# ќграничени€, линеаризующие |2s - TotalValue|
s.t. diff_pos:
    2 * s - TotalValue <= z;

s.t. diff_neg:
    TotalValue - 2 * s <= z;

# ”словие неделимости собак
s.t. dogs_together:
    x["dog1"] = x["dog2"];

# ÷елева€ функци€ Ч минимизировать разницу в стоимости долей
minimize diff:
    z;
