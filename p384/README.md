# One-shot ECPP for NIST P-384 via the supersingular shortcut

p = 2^384 − 2^128 − 2^96 + 2^32 − 1 (the secp384r1 field prime, p ≡ 3 mod 4).

Since p ≡ 3 mod 4, the curve y² = x³ + x over F_p is supersingular: trace 0,
order exactly p+1, and already in Montgomery form with A = 0. A one-shot
certificate therefore exists — with **no discriminant search and no class
polynomial** — whenever the n⁴-smooth part of p+1 exceeds L = (p^{1/4}+1)².

Generalized-Mersenne primes make this unusually likely because p+1 factors
algebraically. Here

    p + 1 = 2^32 · (2^64 − 1) · (2^288 + 2^224 + 2^160 + 2^96 − 1)

and its n⁴-smooth part is 197 bits against the 193-bit bound L. The
certificate takes under a second to produce:

```
39402006196394479212279040100143613805079739270465446667948293404245721771496870329047266088258938001861606973112319 0 4175274830798286041899756280709154499563919256408856884352101796557004789991571158742257957651858293808361679587253 11536780045728150470386993180886018923731057780327784120320 1075237 6700417 22253377
```

Reproduce with `python3 supersingular.py` (pure Python, deterministic, prints
the certificate above; verify with `python3 ../voneshot.py $(python3 supersingular.py)`).
The script works for any prime p ≡ 3 mod 4 that passes the smooth-part gate —
notably p = 2^521 − 1 (NIST P-521), where p+1 = 2^521 is entirely smooth and the
certificate is a power-of-2 Pomerance triple.
