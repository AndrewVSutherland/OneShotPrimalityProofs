p = 10^80+129;
Dmax = 8000000;
Dstart = eval(readstr("scan.ckpt")[1]);
{forstep(d=Dstart, Dmax, 1,
  if((d%4==0 || d%4==3) && kronecker(-d,p)==1,
    v = qfbcornacchia(d, 4*p);
    if(#v && v[1]%4==2,
      write("cands.txt", d," ",v[1]," ",v[2])));
  if(d%100000==0, write("scan.ckpt2", d); system("mv scan.ckpt2 scan.ckpt")));}
write("scan.done","done");
print("scan complete");
