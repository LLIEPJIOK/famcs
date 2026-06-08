include "alldifferent.mzn";

int: N = 8;
set of int: TEAMS = 0..N-1;
int: W = N - 1;
int: P = N div 2;
set of int: WEEKS = 1..W;
set of int: PERIODS = 1..P;

array[TEAMS, WEEKS] of var TEAMS: Opponent;
array[TEAMS, WEEKS] of var 0..1: IsHome;
array[TEAMS, WEEKS] of var PERIODS: GamePeriod;

constraint forall(t in TEAMS, w in WEEKS)(
    Opponent[t,w] != t /\
    Opponent[Opponent[t,w], w] = t /\
    GamePeriod[t,w] = GamePeriod[Opponent[t,w], w] /\
    sum(t2 in TEAMS)(bool2int(GamePeriod[t2,w] = GamePeriod[t,w])) = 2
);

constraint forall(t in TEAMS)(
    alldifferent([Opponent[t,w] | w in WEEKS])
);

constraint forall(t in TEAMS, w in WEEKS)(
    IsHome[t,w] = 1 - IsHome[Opponent[t,w], w]
);

solve satisfy;

output [
    "Количество команд (N): \(N) | Количество недель (W): \(W)\n",
    "Расписание турнира:\n\n"
] ++
[
    "Неделя \(w): | " ++
    concat([
        show(t) ++ "v" ++ show(Opponent[t,w]) ++ "(P" ++ show(GamePeriod[t,w]) ++ ") | "
        | t in TEAMS
    ]) ++ "\n"
    | w in WEEKS
];
