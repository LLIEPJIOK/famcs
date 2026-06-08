set I;
set J;

param A_orig {I, J};

param min_A_row {I};
param alpha;
param shift;
param A_mod {I, J};

var y {I} >= 0;

minimize InvValue_P1:
    sum {i in I} y[i];

subject to Constraints_P1 {j in J}:
    sum {i in I} A_mod[i, j] * y[i] >= 1;

param Value_mod;
param Value_orig;

param Optimal_P {I};
param Optimal_Q {J};
