import secrets
from typing import Tuple

ECPoint = Tuple[int, int]  # None = точка на бесконечности


class EllipticCurve:
    def __init__(self,  l: int, p: str, a: str, b: str, q: str):
        self.l = l
        self.p = int.from_bytes(bytes.fromhex(p.replace(" ", "")), "little")
        self.a = int.from_bytes(bytes.fromhex(a.replace(" ", "")), "little")
        self.b = int.from_bytes(bytes.fromhex(b.replace(" ", "")), "little")
        self.q = int.from_bytes(bytes.fromhex(q.replace(" ", "")), "little")
        self.G = self._find_base_point()

    def default_curve() -> 'EllipticCurve':
        l = 128
        p = "43FFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF"
        a = "40FFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF"
        b = "F1039CD6 6B7D2EB2 53928B97 6950F54C BEFBD8E4 AB3AC1D2 EDA8F315 156CCE77"
        q = "07663D26 99BF5A7E FC4DFB0D D68E5CD9 FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF"

        return EllipticCurve(l, p, a, b, q)

    def is_on_curve(self, P: ECPoint) -> bool:
        if P is None:
            return True

        x, y = P
        return (y * y - (x * x * x + self.a * x + self.b)) % self.p == 0

    def inv(self, x: int) -> int:
        return pow(x, -1, self.p)

    def add(self, P: ECPoint, Q: ECPoint) -> ECPoint:
        if P is None:
            return Q
        if Q is None:
            return P

        x1, y1 = P
        x2, y2 = Q

        if x1 == x2 and (y1 + y2) % self.p == 0:
            return None

        if P != Q:
            lam = ((y2 - y1) * self.inv(x2 - x1)) % self.p
        else:
            lam = ((3 * x1 * x1 + self.a) * self.inv(2 * y1)) % self.p

        x3 = (lam * lam - x1 - x2) % self.p
        y3 = (lam * (x1 - x3) - y1) % self.p
        return (x3, y3)

    def neg(self, P: ECPoint) -> ECPoint:
        if P is None:
            return None
        x, y = P
        return (x, (-y) % self.p)

    def sub(self, P: ECPoint, Q: ECPoint) -> ECPoint:
        return self.add(P, self.neg(Q))

    def mul(self, k: int, P: ECPoint) -> ECPoint:
        R = None
        Q = P

        while k > 0:
            if k & 1:
                R = self.add(R, Q)
            Q = self.add(Q, Q)
            k >>= 1

        return R

    def _find_base_point(self) -> ECPoint:
        x = 0
        y = pow(self.b, (self.p + 1) // 4, self.p)
        
        return (x, y)

    def _generate_keypair(self) -> Tuple[int, ECPoint]:
        d = 0
        while d == 0:
            d = secrets.randbelow(2 * self.l // 8)
            d |= 1 << (2 * self.l - 1)
            d %= self.q

        q = self.mul(d, self.G)
        return d, q
