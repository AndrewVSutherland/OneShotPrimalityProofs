import subprocess, json, sys, time, math, random
from gmpy2 import mpz, isqrt, is_prime
sys.path.insert(0, "/home/claude")

PSTR = sys.argv[1]
DMAX = int(sys.argv[2])
MAXHITS = int(sys.argv[3]) if len(sys.argv) > 3 else 1
P = mpz(PSTR)
assert is_prime(P)

# patch process module globals for this p
import process
process.P = P
n = P.bit_length()
process.N2 = n*n
process.N4 = mpz(n*n)*(n*n)
process.SP = isqrt(P)
process.L = process.SP + 1 + isqrt(4*process.SP)
process.LOG2L = math.log2(int(process.L))
process.BUDGET = 250000

tf = (P + 1) % 4
print("p bits:", n, "n4:", process.N4, "t filter: t=%d mod 4" % tf, "log2L=%.2f" % process.LOG2L)

# scan
scan_script = f"""
p = {PSTR};
{{forstep(d=3, {DMAX}, 1,
  if((d%4==0 || d%4==3) && kronecker(-d,p)==1,
    v = qfbcornacchia(d, 4*p);
    if(#v && v[1]%4=={tf},
      print(d," ",v[1]," ",v[2]))));}}
quit
"""
t0=time.time()
out = subprocess.run(["gp","-q"], input=scan_script, capture_output=True, text=True).stdout
cands = [l.split() for l in out.strip().splitlines() if l.strip()]
print(f"scan: {len(cands)} usable candidates in {time.time()-t0:.1f}s")

rng = random.Random(7)
from findm import find_m
hits = []
seen = set()
t0=time.time()
orders_done = 0
for d_, t_, s_ in cands:
    D = int(d_); t = mpz(t_)
    if int(t) in seen: continue
    seen.add(int(t))
    for sign in (+1,-1):
        N = P + 1 - sign*t
        assert N % 4 == 0, (N%4, t%4)
        if N % 8 != 0: continue   # Montgomery model guaranteed only when 8 | N
        fac, lg, rough = process.process_order(N, rng)
        orders_done += 1
        if lg >= process.LOG2L - 1e-9:
            res = find_m(P, fac)
            status = "windowed" if res else "no-window"
            print(f"HIT D={D} sign={sign} lg={lg:.1f} {status}  [{orders_done} orders, {time.time()-t0:.0f}s]")
            if res:
                m, qs = res
                hits.append((D, sign, int(N), m, qs))
    if len(hits) >= MAXHITS: break
print(f"processed {orders_done} orders in {time.time()-t0:.0f}s -> {len(hits)} windowed hits")

for (D, sign, N, m, qs) in hits:
    with open("construct.in","w") as f:
        f.write(f"[{P},{D},{N},{m}]\n")
    out = subprocess.run(["gp","-q","construct.gp"], capture_output=True, text=True, timeout=3000).stdout
    print(out)
    for line in out.splitlines():
        if line.startswith("CERT "):
            vals = [int(x) for x in line.split()[1:]]
            import voneshot
            ok = voneshot.verify(vals[0], vals[1], vals[2], vals[3], tuple(vals[4:]))
            print("voneshot.verify:", ok)
            if ok:
                print("CERTIFICATE:", " ".join(map(str, vals)))
                sys.exit(0)
print("no verified cert")
