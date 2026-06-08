from dataclasses import dataclass
from typing import Optional

import secrets

from crypto.elliptic import EllipticCurve
from crypto.fmt import deserialize_point
from crypto.fmt import serialize_int
from crypto.tzi_wrapper import belt_hash

_CERT_MAGIC = b"CERT1"


def _hash_to_scalar(curve: EllipticCurve, data: bytes) -> int:
    # belt_hash returns 256-bit digest; project code uses little-endian integers.
    return int.from_bytes(belt_hash(data), "little", signed=False) % curve.q


def _sig_len_for_curve(curve: EllipticCurve) -> int:
    # Two scalars of size 2*l bits.
    return 2 * (2 * curve.l // 8)


def _serialize_sig(curve: EllipticCurve, r: int, s: int) -> bytes:
    return serialize_int(r, 2 * curve.l) + serialize_int(s, 2 * curve.l)


def _deserialize_sig(curve: EllipticCurve, sig: bytes) -> tuple[int, int]:
    n = 2 * curve.l // 8
    if len(sig) != 2 * n:
        raise ValueError("invalid signature length")
    r = int.from_bytes(sig[:n], "little", signed=False)
    s = int.from_bytes(sig[n:], "little", signed=False)
    return r, s


def _ecdsa_sign(curve: EllipticCurve, privkey: int, msg: bytes) -> bytes:
    if not (1 <= privkey < curve.q):
        raise ValueError("invalid CA private key")

    e = _hash_to_scalar(curve, msg)
    if e == 0:
        e = 1

    while True:
        k = secrets.randbelow(curve.q)
        if k == 0:
            continue
        R = curve.mul(k, curve.G)
        if R is None:
            continue
        r = R[0] % curve.q
        if r == 0:
            continue
        kinv = pow(k, -1, curve.q)
        s = (kinv * (e + (privkey * r) % curve.q)) % curve.q
        if s == 0:
            continue
        return _serialize_sig(curve, r, s)


def _ecdsa_verify(curve: EllipticCurve, pubkey_point, msg: bytes, sig: bytes) -> bool:
    try:
        r, s = _deserialize_sig(curve, sig)
    except ValueError:
        return False

    if not (1 <= r < curve.q and 1 <= s < curve.q):
        return False

    if pubkey_point is None or not curve.is_on_curve(pubkey_point):
        return False

    e = _hash_to_scalar(curve, msg)
    if e == 0:
        e = 1

    w = pow(s, -1, curve.q)
    u1 = (e * w) % curve.q
    u2 = (r * w) % curve.q
    P = curve.add(curve.mul(u1, curve.G), curve.mul(u2, pubkey_point))
    if P is None:
        return False
    v = P[0] % curve.q
    return v == r


@dataclass(frozen=True)
class Certificate:
    id_name: str
    pubkey: bytes  # serialized EC point (4*l bits)
    sig: bytes  # BELT-MAC tag (8 bytes)

    def serialize(self) -> bytes:
        id_b = self.id_name.encode("utf-8")
        if len(id_b) > 0xFFFF:
            raise ValueError("id_name too long")
        if len(self.sig) == 0:
            raise ValueError("invalid signature length")
        if len(self.sig) != len(self.pubkey):
            raise ValueError("invalid signature length")

        return (
            _CERT_MAGIC
            + len(id_b).to_bytes(2, "little")
            + id_b
            + len(self.pubkey).to_bytes(2, "little")
            + self.pubkey
            + self.sig
        )

    @staticmethod
    def deserialize(data: bytes) -> "Certificate":
        if len(data) < len(_CERT_MAGIC) + 2 + 2 + 1:
            raise ValueError("certificate too short")
        if not data.startswith(_CERT_MAGIC):
            raise ValueError("invalid certificate magic")

        offset = len(_CERT_MAGIC)

        id_len = int.from_bytes(data[offset : offset + 2], "little")
        offset += 2
        if offset + id_len > len(data):
            raise ValueError("invalid certificate")
        id_name = data[offset : offset + id_len].decode("utf-8")
        offset += id_len

        pk_len = int.from_bytes(data[offset : offset + 2], "little")
        offset += 2
        if offset + pk_len > len(data):
            raise ValueError("invalid certificate length")

        pubkey = data[offset : offset + pk_len]
        offset += pk_len

        sig = data[offset:]
        if len(sig) == 0:
            raise ValueError("invalid certificate length")
        if len(sig) != pk_len:
            raise ValueError("invalid signature length")
        return Certificate(id_name=id_name, pubkey=pubkey, sig=sig)


@dataclass(frozen=True)
class RootCA:
    """Minimal root authority.

    This is a lab-style PKI: all participants are provisioned with the trusted
    root *public* key out-of-band. Only the RootCA holds the private signing key.
    """

    id_name: str
    curve: EllipticCurve
    pubkey: bytes  # serialized EC point
    privkey: Optional[int] = None

    @staticmethod
    def from_privkey(id_name: str, curve: EllipticCurve, privkey: int) -> "RootCA":
        if not (1 <= privkey < curve.q):
            raise ValueError("invalid CA private key")
        Q = curve.mul(privkey, curve.G)
        if Q is None or not curve.is_on_curve(Q):
            raise ValueError("invalid CA public key")
        from crypto.fmt import serialize_point

        pubkey = serialize_point(Q, curve.l, 4 * curve.l)
        return RootCA(id_name=id_name, curve=curve, pubkey=pubkey, privkey=privkey)

    def _tbs(self, id_name: str, pubkey: bytes) -> bytes:
        id_b = id_name.encode("utf-8")
        return _CERT_MAGIC + len(id_b).to_bytes(2, "little") + id_b + len(pubkey).to_bytes(2, "little") + pubkey

    def issue_cert(self, id_name: str, pubkey: bytes) -> Certificate:
        if self.privkey is None:
            raise ValueError("CA private key is not available")
        tbs = self._tbs(id_name, pubkey)
        sig = _ecdsa_sign(self.curve, self.privkey, tbs)
        return Certificate(id_name=id_name, pubkey=pubkey, sig=sig)


def verify_cert(
    cert_bytes: bytes,
    *,
    root_pubkey: bytes,
    curve: EllipticCurve,
    expected_id_name: Optional[str] = None,
) -> Certificate:
    """Verify a certificate with the RootCA public key.

    This function is intentionally outside of RootCA so any participant can
    verify independently without needing RootCA instance/state.
    """

    cert = Certificate.deserialize(cert_bytes)

    if expected_id_name is not None and cert.id_name != expected_id_name:
        raise ValueError("certificate id binding invalid")

    ca_Q = deserialize_point(root_pubkey, curve.l)
    if not curve.is_on_curve(ca_Q):
        raise ValueError("CA public key not on curve")

    tbs = _CERT_MAGIC + len(cert.id_name.encode("utf-8")).to_bytes(2, "little") + cert.id_name.encode("utf-8")
    tbs += len(cert.pubkey).to_bytes(2, "little") + cert.pubkey

    if not _ecdsa_verify(curve, ca_Q, tbs, cert.sig):
        raise ValueError("certificate signature invalid")

    Q = deserialize_point(cert.pubkey, curve.l)
    if not curve.is_on_curve(Q):
        raise ValueError("certificate public key not on curve")

    return cert
