import math
import random
import hashlib

def is_prime(n, k=100):
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
        if math.gcd(a, n) != 1:
            return False

        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

def mulmod(a, b, mod):
    return (a * b) % mod

def generate_prime(bits=1024):
    """Generate a prime number of the specified bit lengths using rnd.getrandbits."""
    while True:
        p = random.getrandbits(bits)
        # Ensure it's odd and the highest bit is set
        p |= (1 << (bits - 1)) | 1
        if is_prime(p):
            return p

def generate_p_q(bits_q=160, bits_p=1024, max_tries=100000):
    assert bits_p > bits_q

    q = generate_prime(bits_q)

    lower = 1 << (bits_p - bits_q - 1)
    upper = (1 << (bits_p - bits_q)) - 1

    for _ in range(max_tries):
        k = random.randrange(lower, upper)
        p = k * q + 1
        if p.bit_length() == bits_p and is_prime(p):
            return p, q

    raise ValueError("Failed to generate p and q.")

def gen(bits_p=1024, bits_q=160):
    p, q = generate_p_q(bits_q, bits_p)

    while True:
        alpha = random.randrange(2, p-1)
        g = pow(alpha, (p-1)//q, p)
        if g != 1:
            break
	
    x = random.randrange(1, q)
    y = pow(g, x, p)
    
    return (p, q, g), x, y

def sign(par, x, message):
    p, q, g = par

    k = random.randrange(1, q)
    k_inv = pow(k, -1, q)

    r = pow(g, k, p)

    if isinstance(message, str):
        message = message.encode('utf-8')
    h = int(hashlib.sha256(message).hexdigest(), 16) % q

    s = (k_inv * (h - x * r)) % q

    return (r, s)

def verify(par, y, message, signature):
    p, q, g = par
    r, s = signature

    if not (1 <= r < p):
        return False
    if not (1 <= s < q):
        return False

    if isinstance(message, str):
        message = message.encode('utf-8')

    h = int(hashlib.sha256(message).hexdigest(), 16) % q
    v1 = pow(g, h, p)
    v2 = (pow(y, r, p) * pow(r, s, p)) % p

    return v1 == v2

if __name__ == "__main__":
    params, x, y = gen(1024, 248)
    p, q, g = params
    print(f"p = {p}\nq = {q}\ng = {g}\nx = {x}\ny = {y}")

    message = "Hello, ElGamal!"
    r, s = sign(params, x, message)
    print(f"Signature: (r={r}, s={s})")

    valid = verify(params, y, message, (r, s))
    print(f"Valid: {valid}")
