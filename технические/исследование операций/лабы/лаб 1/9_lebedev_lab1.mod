param price_goat;
param price_oldman;
param price_troika;

param labor_goat;
param labor_oldman;
param labor_troika;

param labor_limit;
param goat_limit;
param oldman_limit;
param troika_limit;

var x1 >= 0;
var x2 >= 0;
var x3 >= 0;

maximize Total_Revenue: 
    price_goat * x1 + price_oldman * x2 + price_troika * x3;

subject to Labor_Constraint:
    labor_goat * x1 + labor_oldman * x2 + labor_troika * x3 <= labor_limit;

subject to Goat_Sale_Limit: x1 <= goat_limit;
subject to Old_Man_Sale_Limit: x2 <= oldman_limit;
subject to Troika_Sale_Limit: x3 <= troika_limit;
