### smallRSA - 120 points
> You intercepted a single message. However, it appears to be encrypted. Can you decrypt it?

Hints:
> 	Normally, you pick e and generate d from that. What appears to have happened in this case? What is likely about the size of d?

This challenge gives us two RSA parameters, the modulus 'n', the public exponent 'e'.
```
e = 165528674684553774754161107952508373110624366523537426971950721796143115780129435315899759675151336726943047090419484833345443949104434072639959175019000332954933802344468968633829926100061874628202284567388558408274913523076548466524630414081156553457145524778651651092522168245814433643807177041677885126141
n = 380654536359671023755976891498668045392440824270475526144618987828344270045182740160077144588766610702530210398859909208327353118643014342338185873507801667054475298636689473117890228196755174002229463306397132008619636921625801645435089242900101841738546712222819150058222758938346094596787521134065656721069
c = 299332969197175711189362475973176110018924953676765834206557170936449056044940463424192591024333960287834765144663838107275612534099922176841029550103731130301225827761650271435325506311287472459681420052612378517579125881519989567977576917642556419749968152894536307775054555830688673518208539947146038594927
```

Notice how long the public exponent is. When we are in a situation like this, the private expontent must be really small. Having this in mind, we can perform the [Wiener Attack](https://en.wikipedia.org/wiki/Wiener%27s_attack).
```
Wiener's Theorem:
Let n = p*q with q < p < 2*q. Let d < (1/4)*n^(1/4).
Given <N,e> with ed = 1 mod (phi(n)), the attacker can efficiently recover d.
```
The attack is done using the [continued fraction](https://en.wikipedia.org/wiki/Continued_fraction) method to discover the exponent. I found a really good [library](https://github.com/orisano/owiener) that does exactly what we need, so the code is really straightforward:
```python
d = owiener.attack(e, n)

if d is None:
    print("Failed")
else:
    print("Hacked d={}".format(d))

print(codecs.decode(hex(pow(c,d,n)).replace("0x",""), "hex"))
```
The private exponent d is:
```python
d=3223594586826657550897063711914171740995144768727978698812620148084071525621
```
Which give us the flag:
```
b'flag{Are_any_RSA_vals_good_91797351217}'
```
