### Not Your Average RSA - 100 points (65 solves)

>  Somebody told me this RSA factoring is MP complete... or was it NP?

For this RSA problem, we are only given the modulus and the ciphertext as follows:

```
c: 9074407119435549226216306717104313210750146895081726439798095976354600576814818348656600684713830051655944443364224597709641982342039946659987121376590618828822446965847273448794324003758131816407702456966504389655568712152599077538994030379567217702587542326383955580601916478060973206347266442527564009737910
n: 18086135173395641986123054725350673124644081001065528104355398467069161310728333370888782472390469310073117314933010148415971838393130403883412870626619053053672200815153337045022984003065791405742151350233540671714100052962945261324862393058079670757430356345222006961306738393548705354069502196752913415352527
```

First thing I did was to insert the modulus into factordb to see if it could be easily factored but, the database didn't have all the factors. So, next thing I did was to run yafu on the modulus and voilá:

```
# Factored with yafu
p1 = 27289543
p2 = 27409927
p3 = 33322589
p4 = 17730961
p5 = 27138691
p6 = 22576643
p7 = 27606707
p8 = 21647243
p9 = 18313601
p10 = 23554169
p11 = 24525821
p12 = 31703933
p13 = 25671797
p14 = 24996157
p15 = 27739163
p16 = 20013121
p17 = 17673199
p18 = 29488469
p19 = 30580789
p20 = 21321539
p21 = 31881917
p22 = 25808239
p23 = 22685197
p24 = 30342329
p25 = 24946057
p26 = 16904777
p27 = 18646361
p28 = 19459483
p29 = 31696261
p30 = 22050221
p31 = 20010041
p32 = 25963459
p33 = 20197313
p34 = 21891889
p35 = 33098557
p36 = 31737131
p37 = 29511773
p38 = 28863719
p39 = 20390129
p40 = 17901463
p41 = 18145913
p42 = 33381329
```

What I didn't expect was to see so many primes. Multiple prime RSA can decrypt messsages using the Chinese Remainder Theorem as explained in this StackOverflow [question](https://crypto.stackexchange.com/questions/31109/rsa-enc-decryption-with-multiple-prime-modulus-using-crt). To solve this problem, I simple implemented the solution given by the top answer:

```python
# From https://crypto.stackexchange.com/questions/31109/rsa-enc-decryption-with-multiple-prime-modulus-using-crt
ts = []
xs = []
ds = []

for i in range(len(primes)):
	ds.append(modinv(e, primes[i]-1))

m = primes[0]

for i in range(1, len(primes)):
	ts.append(modinv(m, primes[i]))
	m = m * primes[i]

for i in range(len(primes)):
	xs.append(pow((c%primes[i]), ds[i], primes[i]))

x = xs[0]
m = primes[0]

for i in range(1, len(primes)):
	x = x + m * ((xs[i] - x % primes[i]) * (ts[i-1] % primes[i]))
	m = m * primes[i]


print hex(x%n)[2:-1].decode("hex")
```

Running the above script we get the flag:

```
timctf{mUlt1_PriM3_rS4_c0ULD_B3_DAngEr0us}
```
