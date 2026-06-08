import os
import secrets
from dataclasses import dataclass
from typing import Optional

from binascii import hexlify

from crypto.cert import RootCA, verify_cert
from crypto.elliptic import ECPoint, EllipticCurve
from crypto.fmt import deserialize_point, serialize_bytes, serialize_int, serialize_point
from crypto.tzi_wrapper import bake_kdf, belt_hash, belt_mac


def _hx(b: bytes) -> str:
    return hexlify(b).decode("ascii")


def _log_bytes(prefix: str, name: str, value: bytes):
    print(f"{prefix}{name} = {_hx(value)}")


@dataclass
class BMQVMessage0:
    hello_a: bytes

@dataclass
class BMQVMessage1:
    hello_b: bytes
    cert_b: bytes
    v_b: bytes

@dataclass
class BMQVMessage2:
    cert_a: bytes
    v_a: bytes
    t_a: Optional[bytes] = None

@dataclass
class BMQVMessage3:
    t_b: Optional[bytes] = None

class BMQVParticipant:
    def __init__(
        self,
        id_name: str,
        curve: EllipticCurve,
        hello: bytes,
        cert: Optional[bytes],
        root_ca: RootCA,
        *,
        d: Optional[int] = None,
        Q: Optional[ECPoint] = None,
    ):
        self.id_name = id_name
        self.curve = curve
        self.hello = hello

        if root_ca is None:
            raise ValueError("root_ca is required")

        if d is not None and Q is not None:
            self.d, self.Q = d, Q
        else:
            self.d, self.Q = self.generate_keypair()

        print(f"[{self.id_name}] static keypair")
        _log_bytes(f"[{self.id_name}] ", "d", serialize_int(self.d, 2 * self.curve.l))
        _log_bytes(
            f"[{self.id_name}] ",
            "Q",
            serialize_point(self.Q, self.curve.l, 4 * self.curve.l),
        )

        self.root_ca = root_ca

        if cert is None:
            self.cert = self.root_ca.issue_cert(
                self.id_name,
                serialize_point(self.Q, self.curve.l, 4 * self.curve.l),
            ).serialize()
        else:
            parsed = verify_cert(
                cert,
                root_pubkey=self.root_ca.pubkey,
                curve=self.curve,
                expected_id_name=self.id_name,
            )
            if parsed.pubkey != serialize_point(self.Q, self.curve.l, 4 * self.curve.l):
                raise ValueError("certificate does not match participant public key")
            self.cert = cert

        _log_bytes(f"[{self.id_name}] ", "cert", self.cert)

        self.cert_a = None
        self.Q_a = None
        self.hello_a = None
        self.u_a = None
        self.v_a = None

        self.cert_b = None
        self.Q_b = None
        self.hello_b = None
        self.u_b = None
        self.v_b = None

        self.K0 = None

    def generate_keypair(self):
        d = 0
        while d == 0:
            d = secrets.randbelow(2 * self.curve.l // 8)
            d |= 1 << (2 * self.curve.l - 1)
            d %= self.curve.q

        q = self.curve.mul(d, self.curve.G)
        return d, q

    def process_init(self) -> BMQVMessage0:
        """Alice returns M0"""

        print(f"[{self.id_name}] M0 ->")
        _log_bytes(f"[{self.id_name}] ", "hello", self.hello)

        return BMQVMessage0(
            hello_a=self.hello
        )

    def process_m0(
        self,
        m0: BMQVMessage0,
        *,
        expected_v_b: Optional[bytes] = None,
    ) -> BMQVMessage1:
        """Bob processes M0 and returns M1
        
        Args:
            m0: Message from Alice
            expected_v_b: Expected V_B value for verification (optional, for testing)
        """

        print(f"[{self.id_name}] <- M0")
        _log_bytes(f"[{self.id_name}] ", "hello_a", m0.hello_a)

        u_b = 0
        while u_b == 0:
            u_b = secrets.randbelow(self.curve.q)

        v_b = self.curve.mul(u_b, self.curve.G)
        v_b_bytes = serialize_point(v_b, self.curve.l, 4 * self.curve.l)

        if expected_v_b is not None and v_b_bytes != expected_v_b:
            raise ValueError(f"V_B mismatch: {_hx(v_b_bytes)} != {_hx(expected_v_b)}")

        self.hello_a = m0.hello_a
        self.u_b = u_b
        self.v_b = v_b

        print(f"[{self.id_name}] M1 ->")
        _log_bytes(f"[{self.id_name}] ", "u_b", serialize_int(u_b, 2 * self.curve.l))
        _log_bytes(f"[{self.id_name}] ", "v_b", v_b_bytes)
        _log_bytes(f"[{self.id_name}] ", "cert_b", self.cert)

        return BMQVMessage1(
            hello_b=self.hello,
            cert_b=self.cert,
            v_b=v_b_bytes
        )


    def process_m1(
        self,
        m1: BMQVMessage1,
        *,
        expected_v_a: Optional[bytes] = None,
        expected_t: Optional[bytes] = None,
        expected_s_a: Optional[bytes] = None,
        expected_K: Optional[bytes] = None,
        expected_K0: Optional[bytes] = None,
        expected_K1: Optional[bytes] = None,
        expected_T_a: Optional[bytes] = None,
    ) -> BMQVMessage2:
        """Alice processes M1 and returns M2
        
        Args:
            m1: Message from Bob
            expected_v_a: Expected V_A value (optional, for testing)
            expected_t: Expected t value (optional, for testing)
            expected_s_a: Expected s_A value (optional, for testing)
            expected_K: Expected K value (optional, for testing)
            expected_K0: Expected K0 value (optional, for testing)
            expected_K1: Expected K1 value (optional, for testing)
            expected_T_a: Expected T_A value (optional, for testing)
        """

        print(f"[{self.id_name}] <- M1")
        _log_bytes(f"[{self.id_name}] ", "hello_b", m1.hello_b)
        _log_bytes(f"[{self.id_name}] ", "cert_b", m1.cert_b)
        _log_bytes(f"[{self.id_name}] ", "v_b(raw)", m1.v_b)

        cert_b = verify_cert(m1.cert_b, root_pubkey=self.root_ca.pubkey, curve=self.curve)
        Q_b = deserialize_point(cert_b.pubkey, self.curve.l)
        _log_bytes(f"[{self.id_name}] ", "Q_b", cert_b.pubkey)

        v_b = deserialize_point(m1.v_b, self.curve.l)
        if not self.curve.is_on_curve(v_b):
            raise ValueError("Invalid point")

        u_a = 0
        while u_a == 0:
            u_a = secrets.randbelow(self.curve.q)

        v_a = self.curve.mul(u_a, self.curve.G)
        v_a_bytes = serialize_point(v_a, self.curve.l, 4 * self.curve.l)

        if expected_v_a is not None and v_a_bytes != expected_v_a:
            raise ValueError(f"V_A mismatch: {_hx(v_a_bytes)} != {_hx(expected_v_a)}")

        _log_bytes(f"[{self.id_name}] ", "u_a", serialize_int(u_a, 2 * self.curve.l))
        _log_bytes(f"[{self.id_name}] ", "v_a", v_a_bytes)

        t = int.from_bytes(
            serialize_bytes(
                belt_hash(
                    serialize_point(v_a, self.curve.l, 2 * self.curve.l) + 
                    serialize_point(v_b, self.curve.l, 2 * self.curve.l)
                ),
                self.curve.l
            ),
            "little"
        )
        t_bytes = serialize_int(t, self.curve.l)

        if expected_t is not None and t_bytes != expected_t:
            raise ValueError(f"t mismatch: {_hx(t_bytes)} != {_hx(expected_t)}")

        m = pow(2, self.curve.l, self.curve.q) + t
        s_a = (u_a - m * self.d) % self.curve.q
        s_a_bytes = serialize_int(s_a, 2 * self.curve.l)

        if expected_s_a is not None and s_a_bytes != expected_s_a:
            raise ValueError(f"s_A mismatch: {_hx(s_a_bytes)} != {_hx(expected_s_a)}")

        _log_bytes(f"[{self.id_name}] ", "t", t_bytes)
        _log_bytes(f"[{self.id_name}] ", "m", serialize_int(m, 2 * self.curve.l))
        _log_bytes(f"[{self.id_name}] ", "s_a", s_a_bytes)
        
        K = self.curve.mul(s_a, self.curve.sub(v_b, self.curve.mul(m, Q_b)))
        if K is None:
            K = self.curve.G
        K_bytes = serialize_point(K, self.curve.l, 4 * self.curve.l)

        if expected_K is not None and K_bytes != expected_K:
            raise ValueError(f"K mismatch: {_hx(K_bytes)} != {_hx(expected_K)}")

        _log_bytes(f"[{self.id_name}] ", "K", K_bytes)

        K0 = bake_kdf(
            serialize_point(K, self.curve.l, 2 * self.curve.l),
            self.cert + m1.cert_b + self.hello + m1.hello_b, 
            0,
        )

        if expected_K0 is not None and K0 != expected_K0:
            raise ValueError(f"K0 mismatch: {_hx(K0)} != {_hx(expected_K0)}")

        _log_bytes(f"[{self.id_name}] ", "K0", K0)

        self.cert_b = m1.cert_b
        self.Q_b = Q_b
        self.hello_b = m1.hello_b
        self.v_b = v_b
        self.u_a = u_a
        self.v_a = v_a
        self.K0 = K0

        K1 = bake_kdf(
            serialize_point(K, self.curve.l, 2 * self.curve.l),
            self.cert + m1.cert_b + self.hello + m1.hello_b, 
            1,
        )

        if expected_K1 is not None and K1 != expected_K1:
            raise ValueError(f"K1 mismatch: {_hx(K1)} != {_hx(expected_K1)}")

        # T_A = belt-mac(0^128, K_1) - сообщение 0^128 (16 нулевых байт), ключ K1
        T_a = belt_mac(K1, bytes(16))

        if expected_T_a is not None and T_a != expected_T_a:
            raise ValueError(f"T_A mismatch: {_hx(T_a)} != {_hx(expected_T_a)}")

        _log_bytes(f"[{self.id_name}] ", "K1", K1)
        _log_bytes(f"[{self.id_name}] ", "T_a", T_a)

        print(f"[{self.id_name}] M2 ->")
        _log_bytes(f"[{self.id_name}] ", "cert_a", self.cert)
        _log_bytes(
            f"[{self.id_name}] ",
            "v_a(raw)",
            serialize_point(v_a, self.curve.l, 4 * self.curve.l),
        )

        return BMQVMessage2(
            cert_a=self.cert,
            v_a=v_a_bytes,
            t_a=T_a,
        )

    def process_m2(
        self,
        m2: BMQVMessage2,
        *,
        expected_s_b: Optional[bytes] = None,
        expected_K: Optional[bytes] = None,
        expected_K0: Optional[bytes] = None,
        expected_K1: Optional[bytes] = None,
        expected_T_b: Optional[bytes] = None,
    ) -> BMQVMessage3:
        """Bob processes M2 and returns M3
        
        Args:
            m2: Message from Alice
            expected_s_b: Expected s_B value (optional, for testing)
            expected_K: Expected K value (optional, for testing)
            expected_K0: Expected K0 value (optional, for testing)
            expected_K1: Expected K1 value (optional, for testing)
            expected_T_b: Expected T_B value (optional, for testing)
        """

        print(f"[{self.id_name}] <- M2")
        _log_bytes(f"[{self.id_name}] ", "cert_a", m2.cert_a)
        _log_bytes(f"[{self.id_name}] ", "v_a(raw)", m2.v_a)
        if m2.t_a is not None:
            _log_bytes(f"[{self.id_name}] ", "T_a(recv)", m2.t_a)

        cert_a = verify_cert(m2.cert_a, root_pubkey=self.root_ca.pubkey, curve=self.curve)
        Q_a = deserialize_point(cert_a.pubkey, self.curve.l)
        _log_bytes(f"[{self.id_name}] ", "Q_a", cert_a.pubkey)

        v_a = deserialize_point(m2.v_a, self.curve.l)
        if not self.curve.is_on_curve(v_a):
            raise ValueError("Invalid point")

        self.cert_a = m2.cert_a
        self.Q_a = Q_a
        self.v_a = v_a

        u_b = self.u_b
        v_b = self.v_b

        t = int.from_bytes(
            serialize_bytes(
                belt_hash(
                    serialize_point(v_a, self.curve.l, 2 * self.curve.l) + 
                    serialize_point(v_b, self.curve.l, 2 * self.curve.l)
                ),
                self.curve.l
            ),
            "little"
        )

        m = pow(2, self.curve.l, self.curve.q) + t
        s_b = (u_b - m * self.d) % self.curve.q
        s_b_bytes = serialize_int(s_b, 2 * self.curve.l)

        if expected_s_b is not None and s_b_bytes != expected_s_b:
            raise ValueError(f"s_B mismatch: {_hx(s_b_bytes)} != {_hx(expected_s_b)}")

        _log_bytes(f"[{self.id_name}] ", "t", serialize_int(t, self.curve.l))
        _log_bytes(f"[{self.id_name}] ", "m", serialize_int(m, 2 * self.curve.l))
        _log_bytes(f"[{self.id_name}] ", "s_b", s_b_bytes)
        
        K = self.curve.mul(s_b, self.curve.sub(v_a, self.curve.mul(m, Q_a)))
        if K is None:
            K = self.curve.G
        K_bytes = serialize_point(K, self.curve.l, 4 * self.curve.l)

        if expected_K is not None and K_bytes != expected_K:
            raise ValueError(f"K mismatch: {_hx(K_bytes)} != {_hx(expected_K)}")

        _log_bytes(f"[{self.id_name}] ", "K", K_bytes)

        K0 = bake_kdf(
            serialize_point(K, self.curve.l, 2 * self.curve.l),
            m2.cert_a + self.cert + self.hello_a + self.hello,
            0,
        )
        self.K0 = K0

        if expected_K0 is not None and K0 != expected_K0:
            raise ValueError(f"K0 mismatch: {_hx(K0)} != {_hx(expected_K0)}")

        _log_bytes(f"[{self.id_name}] ", "K0", K0)

        K1 = bake_kdf(
            serialize_point(K, self.curve.l, 2 * self.curve.l),
            m2.cert_a + self.cert + self.hello_a + self.hello,
            1,
        )

        if expected_K1 is not None and K1 != expected_K1:
            raise ValueError(f"K1 mismatch: {_hx(K1)} != {_hx(expected_K1)}")

        # T_A = belt-mac(0^128, K_1) - сообщение 0^128 (16 нулевых байт), ключ K1
        T_a = belt_mac(K1, bytes(16))
        _log_bytes(f"[{self.id_name}] ", "K1", K1)
        _log_bytes(f"[{self.id_name}] ", "T_a(calc)", T_a)
        if T_a != m2.t_a:
            raise ValueError("T_A verification failed")

        # T_B = belt-mac(1^128, K_1) - сообщение 1^128 (16 байт 0xFF), ключ K1
        T_b = belt_mac(K1, bytes([0xFF] * 16))

        if expected_T_b is not None and T_b != expected_T_b:
            raise ValueError(f"T_B mismatch: {_hx(T_b)} != {_hx(expected_T_b)}")

        _log_bytes(f"[{self.id_name}] ", "T_b", T_b)
        print(f"[{self.id_name}] M3 ->")

        return BMQVMessage3(
            t_b=T_b,
        )

    def process_m3(self, m3: BMQVMessage3):
        """Alice processes M3"""

        print(f"[{self.id_name}] <- M3")
        if m3.t_b is not None:
            _log_bytes(f"[{self.id_name}] ", "T_b(recv)", m3.t_b)

        t = int.from_bytes(
            serialize_bytes(
                belt_hash(
                    serialize_point(self.v_a, self.curve.l, 2 * self.curve.l) + 
                    serialize_point(self.v_b, self.curve.l, 2 * self.curve.l)
                ),
                self.curve.l
            ),
            "little"
        )

        m = pow(2, self.curve.l, self.curve.q) + t
        s_a = (self.u_a - m * self.d) % self.curve.q
        
        K = self.curve.mul(s_a, self.curve.sub(self.v_b, self.curve.mul(m, self.Q_b)))
        if K is None:
            K = self.curve.G

        K0 = bake_kdf(
            serialize_point(K, self.curve.l, 2 * self.curve.l),
            self.cert + self.cert_b + self.hello + self.hello_b,
            0,
        )

        K1 = bake_kdf(
            serialize_point(K, self.curve.l, 2 * self.curve.l),
            self.cert + self.cert_b + self.hello + self.hello_b,
            1,
        )
        # T_B = belt-mac(1^128, K_1) - сообщение 1^128 (16 байт 0xFF), ключ K1
        T_b = belt_mac(K1, bytes([0xFF] * 16))
        _log_bytes(f"[{self.id_name}] ", "K0", K0)
        _log_bytes(f"[{self.id_name}] ", "K1", K1)
        _log_bytes(f"[{self.id_name}] ", "T_b(calc)", T_b)
        if T_b != m3.t_b:
            raise ValueError("T_B verification failed")

        print(f"[{self.id_name}] key agreement OK")

    def get_shared_key(self):
        return self.K0
