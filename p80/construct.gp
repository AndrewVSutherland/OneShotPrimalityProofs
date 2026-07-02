default(parisizemax, 2000000000);
default(parisize, 200000000);
\\ construct.gp : args set via -D style read from construct.in
\\ input file: p D N m  (one line, decimal)
{
  v = readvec("construct.in")[1];
  p = v[1]; D = v[2]; N = v[3]; m = v[4];
  Np = 2*p + 2 - N;   \\ twist order
  n = #binary(p); n2 = n^2; n4 = n^2^2;
  fm = factor(m); fs = fm[,1];  \\ prime divisors of m (m is n^4-smooth so this is fast)
  print("class number h = ", qfbclassno(-D));
  H = polclass(-D);
  print("polclass degree ", poldegree(H), ", computing roots mod p...");
  rts = polrootsmod(H, p);
  print(#rts, " roots");
  done = 0;
  for(ri = 1, #rts,
    if(done, break);
    j = rts[ri];
    if(lift(j)==0 || lift(j)==1728%p, next);
    k = j/(1728 - j);
    a0 = 3*k; b0 = 2*k;
    \\ two twists: (a0,b0) and (a0*d^2, b0*d^3)
    d = 2; while(kronecker(d,p) != -1, d++);
    for(tw = 0, 1,
      if(done, break);
      a = if(tw, a0*d^2, a0); b = if(tw, b0*d^3, b0);
      E = ellinit([a,b], p);
      \\ decide the order of E among {N, Np}
      isN = -1;
      for(tries=1, 8,
        P = random(E);
        zN = (ellmul(E,P,N) == [0]);
        zNp = (ellmul(E,P,Np) == [0]);
        if(zN && !zNp, isN = 1; break);
        if(zNp && !zN, isN = 0; break));
      if(isN != 1, next);
      print("curve of order N found: root #",ri," twist ",tw);
      \\ Montgomery conversion: root alpha of x^3+ax+b with 3a^2+a QR
      rr = polrootsmod(x^3 + a*x + b, p);
      print("  2-torsion roots: ", #rr);
      for(ai = 1, #rr,
        if(done, break);
        al = rr[ai];
        c = 3*al^2 + a;
        if(c == 0, next);
        if(issquare(c),
          s = 1/sqrt(c);   \\ either sqrt is fine
          A = 3*al*s;
          if(lift(A)==2 || lift(A)==p-2, next);
          \\ build point of exact order m, prime power by prime power
          Q = [0]; okm = 1;
          for(fi = 1, #fs,
            q = fs[fi]; e = fm[fi,2];
            vN = valuation(N, q);
            fnd = 0;
            for(att = 1, 60,
              R = ellmul(E, random(E), N / q^vN);
              if(R == [0], next);
              kk = 0; T = R;
              while(T != [0] && kk <= vN, T = ellmul(E, T, q); kk++);
              if(kk > vN, next);   \\ safety: order not a q-power (shouldn't happen)
              if(kk >= e, S = ellmul(E, R, q^(kk - e)); fnd = 1; break));
            if(!fnd, okm = 0; break);
            Q = elladd(E, Q, S));
          if(okm && ellmul(E, Q, m) == [0],
            exact = 1;
            for(fi = 1, #fs, if(ellmul(E, Q, m/fs[fi]) == [0], exact = 0; break));
            if(exact,
              x0 = lift(s*(Q[1] - al));
              qs = select(q -> q > n2, fs);
              printf("CERT %d %d %d %d", p, lift(A), x0, m);
              for(i=1,#qs, printf(" %d", qs[i]));
              print("");
              done = 1));
          if(!done, print("  point-of-order-m construction failed on this curve"));
        );
      );
    );
  );
  if(!done, print("FAILED"));
}
quit
