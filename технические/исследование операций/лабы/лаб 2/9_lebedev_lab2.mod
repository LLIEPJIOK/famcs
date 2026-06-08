set NODES;

param balance{NODES};

set ARCS within NODES cross NODES;

param cost{ARCS};
param capacity{ARCS} >= 0;

var Flow{ARCS};

minimize Total_Cost:
    sum{(i,j) in ARCS} cost[i,j] * Flow[i,j];

subject to Flow_Conservation {k in NODES}:
    sum{(k,j) in ARCS} Flow[k,j] - sum{(i,k) in ARCS} Flow[i,k] = balance[k];

subject to Capacity_Constraint {(i,j) in ARCS}:
    0 <= Flow[i,j] <= capacity[i,j];