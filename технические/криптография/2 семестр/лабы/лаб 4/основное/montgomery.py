def extended_gcd(a, b):
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y

    return (old_r, old_x, old_y)

def montgomery_pow(base, exp, mod):
    if mod <= 0:
        raise ValueError("Modulus must be positive")
    if exp < 0:
        raise ValueError("Exponent should be non-negative")
    
    base %= mod

    # 1. Choose R and compute constants
    bits = mod.bit_length()
    r = 1 << bits

    # Find R_inv and modulus_prime such that R_inv * R - modulus_prime * mod = 1
    gcd, r_inv, modulus_prime_neg = extended_gcd(r, mod)
    assert gcd == 1, "r and modulus must be coprime"
    modulus_prime = -modulus_prime_neg % r

    def montgomery_reduce(T):
        """
        Montgomery reduction. Computes (T * R_inv) % mod.
        T must be < mod * R.
        """
        # m = (T * modulus_prime) % R
        m = (T * modulus_prime) & (r - 1)
        # t = (T + m * mod) / R
        t = (T + m * mod) >> bits
        if t >= mod:
            return t - mod
        else:
            return t

    # 2. Convert to Montgomery form
    r2 = (r * r) % mod
    base_mont = montgomery_reduce(base * r2)
    result_mont = montgomery_reduce(1 * r2)

    # 3. Exponentiation in Montgomery form (right-to-left method)
    while exp > 0:
        if (exp & 1) == 1:
            result_mont = montgomery_reduce(result_mont * base_mont)
        base_mont = montgomery_reduce(base_mont * base_mont)
        exp >>= 1

    # 4. Convert result back from Montgomery form
    result = montgomery_reduce(result_mont)

    return result
