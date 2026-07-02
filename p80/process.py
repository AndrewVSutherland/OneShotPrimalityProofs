import sys, time, math, random, json, os
from gmpy2 import mpz, gcd, isqrt, is_prime

P  = mpz(10)**80 + 129
N2 = 266*266
N4 = mpz(N2)*N2
SP = isqrt(P)
L  = SP + 1 + isqrt(4*SP)
LOG2L = math.log2(int(L))
BUDGET = 250000

def sieve(limit):
    bs = bytearray([1])*(limit+1); bs[0]=bs[1]=0
    for i in range(2, int(limit**0.5)+1):
        if bs[i]: bs[i*i::i] = bytearray(len(bs[i*i::i]))
    return [i for i in range(2,limit+1) if bs[i]]

SMALL = sieve(100000)
CHUNKS = []
prod = mpz(1); plist = []
for q in SMALL:
    prod *= q; plist.append(q)
    if prod.bit_length() > 8192:
        CHUNKS.append((prod, plist)); prod = mpz(1); plist = []
if plist: CHUNKS.append((prod, plist))

def strip_small(N):
    fac = {}; C = mpz(N)
    for chunk, pl in CHUNKS:
        g = gcd(C, chunk)
        if g > 1:
            for q in pl:
                if g % q == 0:
                    e = 0
                    while C % q == 0: C //= q; e += 1
                    fac[q] = e
    return fac, C

def brent(N, budget, c, x0):
    N = mpz(N)
    y = mpz(x0); r = 1; q = mpz(1); G = mpz(1); it = 0
    m = 256
    while True:
        x = y
        for _ in range(r):
            y = (y*y + c) % N
        k = 0
        while k < r and G == 1:
            ys = y
            lim = min(m, r-k)
            for _ in range(lim):
                y = (y*y + c) % N
                q = q * (x-y) % N
            G = gcd(q, N)
            k += lim; it += lim
            if it > budget: return None
        r <<= 1
        if G != 1: break
    if G == N:
        G = mpz(1)
        while G == 1:
            ys = (ys*ys + c) % N
            G = gcd(x-ys, N)
        if G == N: return None
    return G

def split_all_below(C, budget, rng):
    fac = {}; rough = mpz(1)
    stack = [mpz(C)]
    while stack:
        M = stack.pop()
        if M == 1: continue
        if is_prime(M):
            if M <= N4:
                fac[int(M)] = fac.get(int(M),0)+1
            else:
                rough *= M
            continue
        f = None
        for _ in range(3):
            f = brent(M, budget, rng.randrange(1,10**6), rng.randrange(2,10**6))
            if f and f != M: break
            f = None
        if f is None:
            rough *= M; continue
        stack.append(f); stack.append(M//f)
    return fac, rough

def process_order(N, rng):
    fac, C = strip_small(N)
    med, rough = split_all_below(C, BUDGET, rng)
    for f,e in med.items(): fac[f] = fac.get(f,0)+e
    lg = sum(math.log2(f)*e for f,e in fac.items())
    return fac, lg, rough

def main():
    rng = random.Random(2026)
    seen_t = set()
    pos = 0
    done = 0
    t_start = time.time()
    hits = 0
    out = open("hits.txt", "a")
    stat = open("progress.txt", "a")
    while True:
        # incremental read of cands.txt
        try:
            with open("cands.txt") as f:
                f.seek(pos)
                lines = f.readlines()
                # avoid partial last line
                if lines and not lines[-1].endswith("\n"):
                    lines = lines[:-1]
                pos += sum(len(l) for l in lines)
        except FileNotFoundError:
            lines = []
        if not lines:
            if os.path.exists("scan.done"):
                break
            time.sleep(5); continue
        for line in lines:
            d_, t_, s_ = line.split()
            D = int(d_); t = mpz(t_)
            if int(t) in seen_t:
                continue
            seen_t.add(int(t))
            for sign in (+1, -1):
                N = P + 1 - sign*t
                assert N % 4 == 0
                if N % 8 != 0:
                    continue   # need 8 | N to guarantee a Montgomery model
                fac, lg, rough = process_order(N, rng)
                done += 1
                if lg >= LOG2L - 1e-9:
                    hits += 1
                    rec = {"D": D, "t": str(t), "sign": sign, "N": str(N),
                           "lg": lg, "fac": {str(k): v for k,v in fac.items()}}
                    out.write(json.dumps(rec)+"\n"); out.flush()
                if done % 200 == 0:
                    el = time.time()-t_start
                    stat.write("done=%d hits=%d rate=%.2f/s elapsed=%.0fs\n" % (done, hits, done/el, el))
                    stat.flush()
    stat.write("FINISHED done=%d hits=%d\n" % (done, hits)); stat.flush()

if __name__ == "__main__":
    main()
