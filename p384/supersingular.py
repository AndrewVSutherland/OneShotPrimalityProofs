#!/usr/bin/env python3
"""One-shot ECPP certificate via the supersingular shortcut.

For p = 3 mod 4, the curve y^2 = x^3 + x over F_p is supersingular: trace 0,
order exactly p+1, already Montgomery (A=0). If the n^4-smooth part S of p+1
exceeds L = (p^(1/4)+1)^2, a one-shot certificate exists with no discriminant
search and no class polynomial. Generalized-Mersenne primes (NIST P-384,
P-521 = 2^521-1, ...) have algebraically structured p+1, which makes them
unusually likely to pass this gate. Usage: supersingular.py [p]  (default P-384)
"""
import sys, math, random

def rho_split(v, budget=1 << 22):
    if v % 2 == 0: return 2
    for c in (1, 3, 5, 7, 11):
        x = y = 2; d = 1; k = 0
        while d == 1 and k < budget:
            x = (x*x + c) % v
            y = (y*y + c) % v; y = (y*y + c) % v
            d = math.gcd(abs(x - y), v); k += 1
        if 1 < d < v: return d
    return None

def is_prime(v):
    if v < 2: return False
    for q in (2,3,5,7,11,13,17,19,23,29,31,37): 
        if v % q == 0: return v == q
    d, s = v-1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x = pow(a, d, v)
        if x in (1, v-1): continue
        for _ in range(s-1):
            x = x*x % v
            if x == v-1: break
        else: return False
    return True

def smooth_factor(N, y):
    """Return ({prime: mult} of the y-smooth part, leftover rough part)."""
    fac, stack, roughp = {}, [N], 1
    while stack:
        v = stack.pop()
        for q in range(2, 100000):
            while v % q == 0: fac[q] = fac.get(q, 0) + 1; v //= q
        if v == 1: continue
        if is_prime(v):
            if v <= y: fac[v] = fac.get(v, 0) + 1
            else: roughp *= v
            continue
        d = rho_split(v)
        if d is None:
            # Budget (1<<22 iters) finds factors up to ~2^40 whp, and n^4 < 2^40
            # for all n < 1024: an unsplittable composite has all factors > n^4,
            # hence is entirely rough. Conservative and safe for the gate.
            roughp *= v
            continue
        stack += [d, v // d]
    return fac, roughp

# --- affine arithmetic on y^2 = x^3 + x over F_p ---
def ec_add(P, Q, p):
    if P is None: return Q
    if Q is None: return P
    (x1,y1),(x2,y2) = P,Q
    if x1 == x2:
        if (y1 + y2) % p == 0: return None
        lam = (3*x1*x1 + 1) * pow(2*y1, -1, p) % p
    else:
        lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
    x3 = (lam*lam - x1 - x2) % p
    return (x3, (lam*(x1 - x3) - y1) % p)

def ec_mul(P, k, p):
    R = None
    while k:
        if k & 1: R = ec_add(R, P, p)
        P = ec_add(P, P, p); k >>= 1
    return R

def rand_point(p, rng):
    while True:
        x = rng.randrange(p)
        s = (x*x*x + x) % p
        y = pow(s, (p+1)//4, p)          # p = 3 mod 4
        if y*y % p == s: return (x, y)

def main():
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 2**384 - 2**128 - 2**96 + 2**32 - 1
    if not is_prime(p): sys.exit("p is not prime")
    if p % 4 == 1:
        # Not merely unimplemented: impossible. The one-shot format requires a
        # Montgomery curve, and every Montgomery curve has 4 | N; but the
        # supersingular order is p+1 = 2 mod 4 when p = 1 mod 4. So the
        # supersingular gate is [p = 3 mod 4] AND [smooth(p+1) > L].
        sys.exit("supersingular route impossible in the one-shot format: "
                 "p = 1 mod 4, so the supersingular order p+1 = 2 mod 4 "
                 "cannot be the order of a Montgomery curve (4 | N required)")
    n = p.bit_length(); y = n**4
    sp = math.isqrt(p); L = sp + 1 + math.isqrt(4*sp)
    fac, _ = smooth_factor(p + 1, y)
    S = 1
    for q, e in fac.items(): S *= q**e
    margin = S.bit_length() - L.bit_length()
    print(f"gate: p = 3 mod 4 ok; smooth(p+1) = {S.bit_length()} bits vs "
          f"L = {L.bit_length()} bits (margin {margin:+d})", file=sys.stderr)
    if S <= L: sys.exit("supersingular gate fails: smooth part does not exceed L")
    # Reserve one factor of 2 up front: with v_2(m) <= v_2(p+1) - 1, m divides
    # the group exponent for either supersingular group structure, Z/(p+1) or
    # Z/2 x Z/((p+1)/2). Then m = a near-minimal divisor of S/2 above L:
    # strip primes ascending while possible, so m/q <= L for every prime q | m,
    # giving m < L*r for r the least prime of m.
    assert fac.get(2, 0) >= 2 and S // 2 > L, "margin too thin to reserve a 2"
    mf = dict(fac); mf[2] -= 1
    m = S // 2
    for q in sorted(mf):
        while mf[q] and m // q > L:
            m //= q; mf[q] -= 1
    r = min(q for q in mf if mf[q])
    assert L < m < L * r and (p + 1) % m == 0
    assert m <= p + 1 + math.isqrt(4 * p)
    qs = sorted(q for q in mf if mf[q] and n*n < q < y)
    # point of exact order m, prime power by prime power
    rng = random.Random(384)
    N = p + 1
    Q = None
    for q in sorted(q for q in mf if mf[q]):
        e = mf[q]; vN = 0; t = N
        while t % q == 0: vN += 1; t //= q
        for _ in range(200):
            R = ec_mul(rand_point(p, rng), N // q**vN, p)
            if R is None: continue
            k, T = 0, R
            while T is not None: T = ec_mul(T, q, p); k += 1
            if k >= e: break
        else:
            sys.exit(f'no point with full {q}-valuation found')
        Q = ec_add(Q, ec_mul(R, q**(k - e), p), p)
    assert ec_mul(Q, m, p) is None
    for q in (q for q in mf if mf[q]):
        assert ec_mul(Q, m // q, p) is not None, f"order deficient at {q}"
    print(p, 0, Q[0], m, *qs)

if __name__ == "__main__":
    main()
