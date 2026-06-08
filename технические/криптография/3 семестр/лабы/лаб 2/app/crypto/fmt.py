from crypto.elliptic import ECPoint


def serialize_bytes(b: bytes, bit_length: int) -> bytes:
    if bit_length % 8 != 0:
        raise ValueError("invalid bit length")

    byte_length = bit_length // 8
    if len(b) > byte_length:
        return b[:byte_length]

    return b.ljust(byte_length, b'\x00')

def serialize_int(n: int, bit_length: int) -> bytes:
    byte_length = (bit_length + 7) // 8
    return n.to_bytes(byte_length, "little", signed=False)

def serialize_point(P: ECPoint, l: int, bit_length: int) -> bytes:
    if P is None:
        raise ValueError("cannot serialize point at infinity")

    if bit_length % 8 != 0:
        raise ValueError("invalid n")

    if bit_length > 4 * l:
        raise ValueError("invalid n")

    x, y = P
    x_b = serialize_int(x, 2 * l)
    y_b = serialize_int(y, 2 * l)

    b = x_b + y_b
    return b[: bit_length // 8]

def deserialize_point(b: bytes, l: int) -> ECPoint:
    if len(b) * 8 != 4 * l:
        raise ValueError("cannot deserialize")

    x_b = b[: len(b) // 2]
    y_b = b[len(b) // 2 :]

    x = int.from_bytes(x_b, "little", signed=False)
    y = int.from_bytes(y_b, "little", signed=False)

    return (x, y)