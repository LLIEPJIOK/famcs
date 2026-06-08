import math
from elgamal import gen

def big_little_step(g, y, p):
    m = math.isqrt(p - 1) + 1

    little_steps = {}
    cur = 1
    for j in range(m):
        if cur not in little_steps:
            little_steps[cur] = j
        cur = (cur * g) % p

    inv_g_m = pow(g, m * (p - 2), p)

    gamma = y
    for i in range(m):
        if gamma in little_steps:
            return i * m + little_steps[gamma]
        gamma = (gamma * inv_g_m) % p

    return None

def pollard_rho(g, y, p, q):
    m = math.isqrt(p - 1) + 1
    def subset(z):
        t = (p - 1) // 3
        if z <= t:
            return 0
        elif z <= 2*t:
            return 1
        return 2

    def step(z, u, v):
        c = subset(z)
        if c == 0:
            return (y * z) % p, u, (v + 1) % q
        elif c == 1:
            return pow(z, 2, p), (2 * u) % q, (2 * v) % q
        else:
            return (g * z) % p, (u + 1) % q, v

    tame = {}
    zt, ut, vt = 1, 0, 0
    for _ in range(m):
        if zt in tame:
            u_prev, v_prev = tame[zt]
            if v_prev == vt:
                continue
            return (ut - u_prev) * pow(v_prev - vt, -1, q) % q

        tame[zt] = (ut, vt)
        zt, ut, vt = step(zt, ut, vt)

    return None

if __name__ == "__main__":
    params, x, y = gen(32, 8)
    p, q, g = params

    print(params)
    x_found = pollard_rho(g, y, p, q)
    print(f"x = {x_found}")
    if x != x_found:
        print("Error: x does not match!")
