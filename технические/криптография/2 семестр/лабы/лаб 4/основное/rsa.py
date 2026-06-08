from montgomery import montgomery_pow, extended_gcd
import random

def carmichael_rsa(p: int, q: int) -> int:
    """Compute Carmichael’s function λ(n) for RSA modulus n = p * q."""
    gcd, x, y = extended_gcd(p - 1, q - 1)
    return (p - 1) * (q - 1) // gcd

def fermat(n, k=100):
    """Perform the Fermat primality test."""
    if n < 2:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    for _ in range(k):
        a = random.randint(2, n - 1)
        gcd, x, y = extended_gcd(a, n)
        if gcd != 1 or montgomery_pow(a, n - 1, n) != 1:
            return False
    return True

def rabin_miller(n, k=100):
    """Perform the Miller–Rabin primality test."""
    if n < 2:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # write n-1 as 2^s * d
    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        gcd, x, y = extended_gcd(a, n)
        if gcd != 1:
            return False

        x = montgomery_pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = montgomery_pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

def jacobi(a: int, n: int) -> int:
    """
    Compute the Jacobi symbol (a/n):
    returns -1, 0, or +1.
    """
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be a positive odd integer")

    result = 1
    while a != 0:
        # 1) extract factor 2 from a
        k = (a & -a).bit_length() - 1  # count of trailing zero bits in a
        a >>= k
        # account for (2/n) factor
        if k % 2 == 1 and n % 8 in (3, 5):
            result = -result

        # 2) quadratic reciprocity adjustment
        if a % 4 == 3 and n % 4 == 3:
            result = -result

        # 3) swap (a, n) modulo
        a, n = n % a, a

    return result if n == 1 else 0

def solovay_strassen(n, k=100):
    """Perform the Solovay–Strassen primality test."""
    if n < 2:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    for _ in range(k):
        a = random.randint(2, n - 1)
        gcd, x, y = extended_gcd(a, n)
        if gcd != 1:
            return False
        
        x = montgomery_pow(a, (n - 1) // 2, n)
        if x != jacobi(a, n) % n:
            return False

    return True

def is_prime(n, k=100):
    """Check primality using three tests: Fermat, Miller–Rabin, and Solovay–Strassen."""
    return fermat(n, k) and rabin_miller(n, k) and solovay_strassen(n, k)

def generate_prime(bits=1024):
    """Generate a prime number of the specified bit length using rnd.getrandbits."""
    while True:
        p = random.getrandbits(bits)
        # Ensure it's odd and the highest bit is set
        p |= (1 << (bits - 1)) | 1
        if is_prime(p):
            return p

def generate_keys(bits=2048):
    """Generate RSA public and private key pairs."""
    e = 65537

    p = generate_prime((bits + 1) // 2)
    gcd1, _, _ = extended_gcd(e, p - 1)
    while gcd1 != 1:
        p = generate_prime((bits + 1) // 2)
        gcd1, _, _ = extended_gcd(e, p - 1)

    q = generate_prime((bits + 1) // 2)
    gcd2, _, _ = extended_gcd(e, q - 1)
    while gcd2 != 1:
        q = generate_prime((bits + 1) // 2)
        gcd2, _, _ = extended_gcd(e, q - 1)

    while p == q:
        q = generate_prime((bits + 1) // 2)
        gcd2, _, _ = extended_gcd(e, q - 1)
        while gcd2 != 1:
            q = generate_prime((bits + 1) // 2)
            gcd2, _, _ = extended_gcd(e, q - 1)


    n = p * q
    carmichael = carmichael_rsa(p, q)

    gcd, x, y = extended_gcd(e, carmichael)
    if gcd != 1:
        raise Exception("Modular inverse does not exist for chosen e")

    d = x % carmichael
    return (e, n), (d, n, p, q)

def encrypt(message: str, pubkey: tuple[int, int]) -> str:
    e, n = pubkey

    m_bytes = message.encode('utf-8')
    m_int = int.from_bytes(m_bytes, byteorder='big')
    if m_int >= n:
        raise ValueError("Message too long for this modulus")

    c_int = montgomery_pow(m_int, e, n)

    return hex(c_int)[2:]


def decrypt(cipher_hex: str, privkey: tuple[int, int, int, int]) -> str:
    d, n, p, q = privkey

    try:
        c_int = int(cipher_hex, 16)
    except ValueError:
        raise ValueError("cipher_hex is not valid hex")

    d1 = d % (p - 1)
    d2 = d % (q - 1)
    gcd, q_inv, _ = extended_gcd(q, p)

    x1 = montgomery_pow(c_int, d1, p)
    x2 = montgomery_pow(c_int, d2, q)
    h = (q_inv * (x1 - x2)) % p
    m_int = (x2 + q * h) % n

    length = (m_int.bit_length() + 7) // 8
    m_bytes = m_int.to_bytes(length, byteorder='big')

    return m_bytes.decode('utf-8', errors='replace')

if __name__ == '__main__':
    public_key, private_key = generate_keys(2048)
    print("Public key:", public_key)
    print("Private key:", private_key)

    word = "hello world!"
    encrypted = encrypt(word, public_key)

    numb = int(encrypted, 16)
    numb += 1
    encrypted = hex(numb)[2:]

    print("Encrypted:", encrypted)
    decrypted = decrypt(encrypted, private_key)
    print("Decrypted:", decrypted)

    if word == decrypted:
        print("Encryption/Decryption successful!")
    else:
        print("Encryption/Decryption failed!")
