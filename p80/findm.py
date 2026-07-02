import math, json, sys
from gmpy2 import mpz, isqrt

def find_m(P, fac):
    """fac: {prime: mult}. Find m = subset product with L < m < L*r, r = min prime used.
    Multiplicities are capped so that m is guaranteed to divide the exponent of
    E(F_p) = Z/A x Z/B for ANY valid split (A | gcd(B, p-1), AB = N):
        v_q(m) <= v_q(N) - min(floor(v_q(N)/2), v_q(p-1)).
    Returns (m, sorted distinct primes of m) or None."""
    fac2 = {}
    for q, v in fac.items():
        vq_pm1 = 0
        t = P - 1
        while t % q == 0:
            vq_pm1 += 1; t //= q
        e = v - min(v // 2, vq_pm1)
        if e > 0:
            fac2[q] = e
    fac = fac2
    SP = isqrt(P); L = SP + 1 + isqrt(4*SP)
    n = P.bit_length(); n2 = n*n; n4 = mpz(n2)*n2
    hasse = P + 1 + isqrt(4*P)
    primes = sorted(fac.keys())
    # atoms list (prime repeated by multiplicity), descending for DFS
    # try each possible least prime r0 (ascending: tightest window first is harder;
    # go ascending anyway, windows (L, r0*L))
    for r0 in primes:
        avail = []
        for q in primes:
            if q >= r0:
                avail += [q]*fac[q]
        if r0 not in avail: continue
        # must include r0 at least once; remaining atoms sorted descending
        rest = sorted(avail, reverse=True)
        rest.remove(r0)
        lo = L // r0 + 1          # need m > L with m = r0 * (partial)
        hi_total = (L * r0 - 1)   # m < L*r0  => m <= L*r0 - 1
        # DFS over rest to find product Q with  L < r0*Q*? ... we build m directly:
        target_lo = L + 1         # m >= L+1
        target_hi = min(L * r0 - 1, hasse)
        # suffix products for pruning
        suf = [mpz(1)]*(len(rest)+1)
        for i in range(len(rest)-1, -1, -1):
            suf[i] = suf[i+1]*rest[i]
        found = None
        import sys
        sys.setrecursionlimit(10000)
        def dfs(i, cur):
            nonlocal found
            if found is not None: return
            if target_lo <= cur <= target_hi:
                found = cur; return
            if i >= len(rest): return
            if cur > target_hi: return
            if cur * suf[i] < target_lo: return   # even taking everything is too small
            # branch: include rest[i]
            dfs(i+1, cur*rest[i])
            if found is not None: return
            # skip all remaining copies of the same prime? no—skip just this atom
            # (to reduce duplicate work, skip over equal atoms when excluding)
            j = i
            while j < len(rest) and rest[j] == rest[i]:
                j += 1
            dfs(j, cur)
        dfs(0, mpz(r0))
        if found is not None:
            m = found
            # recompute prime set of m
            mm = m; used = []
            for q in primes:
                if mm % q == 0:
                    used.append(q)
                    while mm % q == 0: mm //= q
            assert mm == 1
            assert used[0] == r0 or min(used) == r0
            r = min(used)
            assert L < m < L*r and m <= hasse
            qs = [q for q in used if n2 < q < n4]
            return int(m), qs
    return None

if __name__ == "__main__":
    # read hits.txt lines, emit best subsets
    Pstr = sys.argv[1]; hitsfile = sys.argv[2]
    P = mpz(Pstr)
    for line in open(hitsfile):
        rec = json.loads(line)
        fac = {int(k): v for k,v in rec["fac"].items()}
        res = find_m(P, fac)
        if res:
            m, qs = res
            print(json.dumps({"D": rec["D"], "sign": rec["sign"], "t": rec["t"],
                              "N": rec["N"], "m": str(m), "qs": qs, "lg": rec["lg"]}))
