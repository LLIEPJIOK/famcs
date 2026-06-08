var xA integer >= 0;
var xB integer >= 0;

var rI  >= 0;
var rII >= 0;
var rIII >= 0;
var rIV >= 0;

param pA;
param pB;

param S_I;
param S_II;
param S_III;
param S_IV;

maximize Z: pA*xA + pB*xB;

subject to resI:   2*xA + 3*xB + rI   = S_I;
subject to resII:    xA        + rII  = S_II;
subject to resIII:          xB + rIII = S_III;
subject to resIV:  2*xA +   xB + rIV  = S_IV;

subject to minresI:   rI  >= 0;
subject to minresII:  rII >= 0;
subject to minresIII: rIII>= 0;
subject to minresIV:  rIV >= 0;
