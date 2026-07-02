# OneShotPrimalityProofs
For the purpose of this repository, a **one-shot ECPP** is a tuple of integers $(p,A,x_0,m,q_1,\ldots,q_k)$ in which
- $p$ is a positive odd integer,
- $A$ is a nonnegative integer less than $p$ with $A\ne \pm 2\bmod p$,
- $x_0$ is a nonnegative integer less than $p$,
- $m$ is an $n^4$-smooth integer, where $n=\lceil \log_2 p\rceil$, satisfying $L < m < L\cdot r$, where $L=q+1+\lfloor 2\sqrt{q}\rfloor$ with $q=\lfloor\sqrt{p}\rfloor$ and $r$ is the least prime divisor of $m$,
- $q_1<\cdots<q_k$ are the prime divisors of $m$ in the interval $(n^2,n^4)$,

such that there exist integers $B,y_0\in [0,p-1]$ for which $(x_0,y_0)$ is a point of order $m$ on the [Montgomery curve](https://en.wikipedia.org/wiki/Montgomery_curve) $By^2 = x^3 + Ax^2 +x$.

Each [Pomerance triple](https://github.com/AndrewVSutherland/DANGER3/blob/main/README.md) corresponds to a one-shot ECPP with $k=0$ in which $m$ is the least power of $2$ exceeding $q+1+2\sqrt{q}$, where $q=\lfloor\sqrt{p}\rfloor$.  It follows that one-shot ECPPs exist for every prime $p>3$.  The key property that one-shot ECPPs share with [Pomerance proofs of primality](https://math.dartmouth.edu/~carlp/PDF/paper62.pdf) is that they can be verified in quasi-quadratic time $O((\log p)^{2+o(1)})$, versus the quasi-cubic time to verify a traditional elliptic curve primality proof (ECPP).

This repository contains the following resources:
- voneshot.py is a Python program that verifies a one-shot ECPP in quasi-quadratic time.
- oneshot8all.txt contains the 202,260 one-shot ECPPs $(p,A,x_0,m,q_1,\ldots,q_k)$ with $p\le 2^8$.
- oneshot12prefixes.txt lists the 1,068,923 unique prefixes $(p,A)$ among all one-shot ECPPs with $p\le 2^{12}$
- oneshot.gp is a GP script that uses a brute-force random search to find one-shot ECPPs.
- certs.csv is a list of one-shot ECPPs for the larger primes listed in the table below.

This project is part of the DARPA expMath program.

**Challenge**
Below is a list of one-shot ECPPs for the least prime $p > 10^n$ for various $n$, as well as some cryptographically relevant $p$.  Can you extend this list?

<details>
<summary>$p=10^{20}+39$,&nbsp; Pomerance proof by <a href="https://www.wits.ac.za/people/academic-a-z-listing/j/vjejjalawitsacza/">Vishnu Jejjala</a> and GPT 5.4 Pro.</summary>
```
100000000000000000039 80635707401894747894 31614069099331127513 17179869184
```
</details>
<details>
<summary>$p=10^{21}+117$,&nbsp Pomerance proof by <a href="https://cos.northeastern.edu/people/fabian-ruehle/">Fabian Ruehle</a> and Claude Code Opus 4.6.</summary>
```
1000000000000000000117 51546435219887079991 144666470127730980460 34359738368
```
</details>
<details>
<summary>$p=10^{22}+9$,&nbsp Pomerance proof found by <a href="https://alexamclain.com/">Alexa McLain</a> and GPT 5.5 Codex.</summary>
```
10000000000000000000009 9992566338662824267458 3694769590833803032125 137438953472
```
</details>
<details>
<summary>$p=10^{23}+117$,&nbsp Pomerance proof found by <a href="https://alexamclain.com/">Alexa McLain</a> and GPT 5.5 Codex.</summary>
```
100000000000000000000117 24163028207499560363686 64911014007772963770218 549755813888
```
</details>
<details>
<summary>$p=10^{24}+7$,&nbsp; Pomerance proof found by <a href="https://janeshi99.github.io/">Jane Shi</a> and Claude Fable 5.</summary>
```
1000000000000000000000007 38923582678463553756710 843367907077058108520461 1099511627776
```
</details>
<details>
<summary>$p=10^{25}+13$,&nbsp Pomerance proof found by <a href="https://alexamclain.com/">Alexa McLain</a> and GPT 5.5 Codex.</summary>
```
10000000000000000000000013 5863342488035851054212447 9636258147581954669181726 4398046511104
```
</details>
<details>
<summary>$p=10^{26}+67$,&nbsp Pomerance proof found by <a href="https://alexamclain.com/">Alexa McLain</a> and GPT 5.5 Codex.</summary>
```
100000000000000000000000067 78462973492772865017160395 27732450411057582323409556 17592186044416
```
</details>
<details>
<summary>$p=10^{27}+103$,&nbsp; via <a href="https://github.com/AndrewVSutherland/OneShotPrimalityProofs/blob/main/oneshot.gp">oneshot.gp</a> (~2 CPU seconds).</summary>
```
1000000000000000000000000103 632259414096052310182774760 241933189256530284790900257 51496302105884 1310041
```
</details>
<details>
<summary>$p=10^{28}+331$,&nbsp; via <a href="https://github.com/AndrewVSutherland/OneShotPrimalityProofs/blob/main/oneshot.gp">oneshot.gp</a> (~2 CPU seconds).</summary>
```
10000000000000000000000000331 3819358685794209339778268422 305961141031129319858787556 102836022984716 26237 858787
```
</details>
<details>
<summary>$p=10^{29}+319$,&nbsp; via <a href="https://github.com/AndrewVSutherland/OneShotPrimalityProofs/blob/main/oneshot.gp">oneshot.gp</a> (~4 CPU seconds).</summary>
```
100000000000000000000000000319 47963730417932095477544369183 33344234680510331383928482742 631463703703722 86981 1606859
```
</details>
<details>
<summary>$p=10^{30}+57$,&nbsp; via <a href="https://github.com/AndrewVSutherland/OneShotPrimalityProofs/blob/main/oneshot.gp">oneshot.gp</a> (~3 CPU seconds).</summary>
```
1000000000000000000000000000057 687867969791064835508699233167 938392059726327280925731259947 2018066682255505 523427 15736687
```
</details>
<details>
<summary>$p=10^{35}+69$,&nbsp; via <a href="https://github.com/AndrewVSutherland/OneShotPrimalityProofs/blob/main/oneshot.gp">oneshot.gp</a> (~26 CPU seconds).</summary>
```
100000000000000000000000000000000069 43571634169656825484488799600262955 73324636112609490847888802702893858 14888340044140359809 734737 4341461 4667437
```
</details>
<details>
<summary>$p=10^{40}+121$,&nbsp; via <a href="https://github.com/AndrewVSutherland/OneShotPrimalityProofs/blob/main/oneshot.gp">oneshot.gp</a> (~11 CPU seconds).</summary>
```
10000000000000000000000000000000000000121 2555590210029791760837835235116824050712 7803267868978634318147510268900254553126 140275114734315966012 5729183 300008747
```
</details>
<details>
<summary>$p=10^{45}+9$,&nbsp; via <a href="https://github.com/AndrewVSutherland/OneShotPrimalityProofs/blob/main/oneshot.gp">oneshot.gp</a> (~169 CPU seconds).</summary>
```
1000000000000000000000000000000000000000000009 445135896715836861872058430558119402113657317 580092437731663015231074250204120036653708361 35083798402964252071240 234187 536561 7129877
```
</details>
<details>
<summary>$p=10^{50}+151$,&nbsp; via <a href="https://github.com/AndrewVSutherland/OneShotPrimalityProofs/blob/main/oneshot.gp">oneshot.gp</a> (~27 CPU seconds).</summary>
```
100000000000000000000000000000000000000000000000151 6437009016641369174910085274409395465870501856011 10538254878888005413405709303009388193264578918912 10329133743438851861485056 325151243
```
</details>
<details>
<summary>$p=10^{55}+21$,&nbsp; <a href="https://math.mit.edu/~drew/">Andrew V. Sutherland</a> and Claude Code Fable 5 via <a href="https://github.com/AndrewVSutherland2/OneShotFastECPP">OneShotFastECPP</a> (~1s on 16 cores).</summary>

```
10000000000000000000000000000000000000000000000000000021 7301475031374361535080075522771336209097048066987481974 6173834153687324988208255789263225553338976807106677666 22629477840921218317005780151 44383 1292429 4420139
```
</details>
<details>
<summary>$p=10^{60}+7$,&nbsp; <a href="https://math.mit.edu/~drew/">Andrew V. Sutherland</a> and Claude Code Fable 5 via <a href="https://github.com/AndrewVSutherland2/OneShotFastECPP">OneShotFastECPP</a> (~1s on 16 cores).</summary>

```
1000000000000000000000000000000000000000000000000000000000007 830110399961048501370209439146800545964774653303052106987822 298268227842950624646418770009243547891462938774568077449549 1870368881745889756085305770583 766813 1132639 1253249 2184151
```
</details>
<details>
<summary>$p=10^{65}+49$,&nbsp; <a href="https://math.mit.edu/~drew/">Andrew V. Sutherland</a> and Claude Code Fable 5 via <a href="https://github.com/AndrewVSutherland2/OneShotFastECPP">OneShotFastECPP</a> (~1s on 16 cores).</summary>

```
100000000000000000000000000000000000000000000000000000000000000049 69397864529375216513776535999986337394361058826206258935356508202 42263807855316775074995609583220755202348362869744021201467981989 382850234159733064321329488683694 93529 211319 1330223
```
</details>
<details>
<summary>$p=10^{70}+33$,&nbsp; <a href="https://math.mit.edu/~drew/">Andrew V. Sutherland</a> and Claude Code Fable 5 via <a href="https://github.com/AndrewVSutherland2/OneShotFastECPP">OneShotFastECPP</a> (~3s on 16 cores).</summary>

```
10000000000000000000000000000000000000000000000000000000000000000000033 4657918240794864663600468107142859528211157973012865214924916589954619 5842016358727341377590423667195843762086503605063812770939330326355949 149978862226141734763959283675972147 74507 2189183 33481957
```
</details>
<details>
<summary>$p=10^{75}+129$,&nbsp; <a href="https://math.mit.edu/~drew/">Andrew V. Sutherland</a> and Claude Code Fable 5 via <a href="https://github.com/AndrewVSutherland2/OneShotFastECPP">OneShotFastECPP</a> (~7s on 16 cores).</summary>

```
1000000000000000000000000000000000000000000000000000000000000000000000000129 275735573977776584341578365958662134102037737178052921570335739437008030239 90540804583116368247599614486383286453433172086081515460373141526347564870 132391591357272908574072744188508209119 360071 530653 756043 3273527 79091209
```
</details>
<details>
<summary>$p=10^{80}+129$,&nbsp; <a href="https://alexamclain.com/">Alexa McLain</a> and Claude Fable 5 via <a href="https://github.com/IslayResearch/OneShotPrimalityProofs/tree/main/p80">reverse-CM order generation</a> (~25m CPU).</summary>

```
100000000000000000000000000000000000000000000000000000000000000000000000000000129 82470437210932481586158718269394203973271304647559303607660206394909667116535460 48330764879392081599985511197395890918115647268502135887092185090492618867106471 17567358025082018213004584112556849530556 983502257 3814594499 4341669811
```
</details>

<details>
<summary>$p=10^{85}+103$,&nbsp; <a href="https://math.mit.edu/~drew/">Andrew V. Sutherland</a> and Claude Code Fable 5 via <a href="https://github.com/AndrewVSutherland2/OneShotFastECPP">OneShotFastECPP</a> (~90s on 16 cores).</summary>

```
10000000000000000000000000000000000000000000000000000000000000000000000000000000000103 4843939831684294311089478529180818054321968623911860910157433414781193453412787410114 4139062708140937362931046438452287416173687175134250719056459402720937076329363517804 5494293751895023693949731379675000029022421 131779 12846697 640037653 655537633 982995407
```
</details>
<details>
<summary>$p=10^{90}+289$,&nbsp; <a href="https://math.mit.edu/~drew/">Andrew V. Sutherland</a> and Claude Code Fable 5 via <a href="https://github.com/AndrewVSutherland2/OneShotFastECPP">OneShotFastECPP</a> (~24s on 16 cores).</summary>

```
1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000289 832901495234922943607064388115504600655650514310140681760977250138145905147480907225146062 94543528871990441267483137130131791599405532578388216635158312261736604103088033458257817 6338439815640971356836635757304716067267075333 887059 2168737 17585329 30478321 54463819 215810047
```
</details>
<details>
<summary>$p=10^{95}+151$,&nbsp; <a href="https://math.mit.edu/~drew/">Andrew V. Sutherland</a> and Claude Code Fable 5 via <a href="https://github.com/AndrewVSutherland2/OneShotFastECPP">OneShotFastECPP</a> (~30s on 16 cores).</summary>

```
100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000151 9352182245283662093217379409142108593986998501318200549989016367079064503090525414310332511507 96825277534417718587592935702553637699461025901236927041422820534984227992483753530285152610404 1458689670355191586076367098280346729129390524517 168029 2956999 4844809 5770879 6996713 15960491 940304579
```
</details>
<details>
<summary>$p=10^{100}+267$,&nbsp; <a href="https://math.mit.edu/~drew/">Andrew V. Sutherland</a> and Claude Code Fable 5 via <a href="https://github.com/AndrewVSutherland2/OneShotFastECPP">OneShotFastECPP</a> (~500s on 16 cores).</summary>

```
10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000267 1303605568953056679656519835890069231945056261099719079493144462625217066199094354664141180279406084 9297425805966447661709167147652926492522227990805155436263744355427229775148644776893432564525571420 133109540315876972450582869368293824379514903297199 118127 21489233 42051091 123206053 333120377
```
</details>
<details>
<summary>$p=10^{105}+3$,&nbsp; <a href="https://math.mit.edu/~drew/">Andrew V. Sutherland</a> and Claude Code Fable 5 via <a href="https://github.com/AndrewVSutherland2/OneShotFastECPP">OneShotFastECPP</a> (~300s on 16 cores).</summary>

```
1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003 107229584141991222635023530101245415439487680807002774607403367434756681948405983251223121135394736274754 283924384697557011640104124842719071234366581195969849149581150658890000276780146102159939761936685422393 46353451196469045982744310397963313944409977341120693 742253 34274521 128224441 249484523 1576468469 4304689031
```
</details>

Contributors (both human and AI) are welcome to submit pull requests to this repo, provided they follow the guidelines below:
- new entries should be the least prime greater than a power of 10 larger than any currently listed;
- include the name of a human and a link to their web page (if available);
- specify the model (and effort level) of any LLM used;
- give a rough estimate of the computational resources used (e.g. CPU/GPUm/hours);
- provide a link to a GitHub repo with code that can be used to reproduce the example.

