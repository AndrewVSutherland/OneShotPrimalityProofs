# One-shot ECPP for p = 10^80 + 129 via reverse-CM order generation

Finding a one-shot ECPP at 266 bits by the brute-force route (random Montgomery A,
count points with SEA, hope the order is n^4-smooth in the window) is infeasible:
each SEA call costs minutes and the expected number of curves is in the thousands.

This pipeline inverts the search: instead of picking curves and computing orders,
it *generates guaranteed curve orders directly* from CM discriminants, tests the
orders for smoothness, and only constructs a curve (once) for the winner.

## Pipeline

1. **scan2.gp** — for each discriminant D <= 8e6 with kronecker(-D,p) = 1, solve
   4p = t^2 + D s^2 with `qfbcornacchia` (microseconds per D). Every solution
   guarantees curves of order p+1±t. Keep t ≡ p+1 (mod 4) so 4 | N.
2. **process.py** — for each candidate order N with **8 | N** (this guarantees a
   point of order 4 and hence a Montgomery model; N ≡ 4 mod 8 candidates can fail
   Montgomery conversion across the whole isogeny class), extract the n^4-smooth
   part: strip primes < 1e5 by primorial gcds, then batched Brent-rho with a fixed
   iteration budget. Keep N whose smooth part exceeds L. (Rho misses only lose
   candidates, never soundness.)
3. **findm.py** — subset-product DFS with suffix-product pruning to find m | N with
   L < m < L*r (r = least prime of m). Prime multiplicities are capped by
   v_q(m) <= v_q(N) - min(floor(v_q(N)/2), v_q(p-1)) so that m divides the group
   exponent of E(F_p) = Z/A x Z/B for *any* valid structure (A | gcd(B, p-1)).
4. **construct.gp** — one `polclass(-D)` for the winner; root j mod p; select the
   twist of order N by a random-point test; Montgomery conversion via a 2-torsion
   root alpha of x^3+ax+b with c = 3 alpha^2 + a a QR (A = 3 alpha / sqrt(c),
   x0 = (x - alpha)/sqrt(c)); and a point of *exact* order m built prime-power by
   prime-power (R = [N/q^{v_q(N)}]P, measure its q-valuation k, S = [q^{k-e}]R,
   sum the S's) — plain cofactor multiplication [N/m]P provably never yields
   order m when some q-Sylow of the group is non-cyclic.

`e2e_test.py` runs the whole pipeline end to end for any prime (validated on the
repo's p = 10^50 + 151 entry before running the 10^80 case).

## Result

For p = 10^80 + 129 (least prime > 10^80): scan found 6623 usable (D,t,s) with
D <= 8e6; 2781 deduplicated orders processed; 5 smooth hits; winner D = -2406423
(class number 760), N = p + 1 + t with t = 9748811013986470950676005585652138849918,
m = 2^2*3*11*47*97*3761*67189*983502257*3814594499*4341669811 (134 bits).

```
100000000000000000000000000000000000000000000000000000000000000000000000000000129 82470437210932481586158718269394203973271304647559303607660206394909667116535460 48330764879392081599985511197395890918115647268502135887092185090492618867106471 17567358025082018213004584112556849530556 983502257 3814594499 4341669811
```

Passes `voneshot.py verify()`. Total cost ≈ 25 CPU minutes on a single core (scan ~2 min, smoothness sieve ~19 min, window search + construction ~2 min).
