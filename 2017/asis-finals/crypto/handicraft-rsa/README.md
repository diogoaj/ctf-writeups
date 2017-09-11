### Handicraft RSA - 138 points (30 solves)

> Someone is developing his own RSA system in his very old home's basement. Prove him that this RSA system is only valid on his basement!

We are given the following code:

```python
#!/usr/bin/python

from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from secret import s, FLAG

def gen_prime(s):
    while True:
        r = getPrime(s)
        R = [r]
        t = int(5 * s / 2) + 1
        for i in range(0, t):
            R.append(r + getRandomRange(0, 4 * s ** 2))
        p = reduce(lambda a, b: a * b, R, 2) + 1
        if isPrime(p):
            if len(bin(p)[2:]) == 1024:
                return p

while True:
    p = gen_prime(s)
    q = gen_prime(s)
    n = p * q
    e = 65537
    d = inverse(e, (p-1)*(q-1))
    if len(bin(n)[2:]) == 2048:
        break

msg = FLAG
key = RSA.construct((long(n), long(e), long(d), long(p), long(p)))
for _ in xrange(s):
    enc = key.encrypt(msg, 0)[0]
    msg = enc

print key.publickey().exportKey()
print '-' * 76
print enc.encode('base64')
print '-' * 76

```

We clearly have here a RSA cryptosystem problem. The code above generates the prime numbers and calculates the private key. At the end, it ciphers the flag a couple of times. One thing that statnds out in the code is the gen_prime function. It is generating prime numbers but in an odd way. It takes random numbers and multiplies them by 2 and then sums them. At the end it sums 1 and checks if it's prime. Primes generated like this are not safe at all since p-1 has a lot of small factors. In fact, there is a known algorithm capable of factoring the RSA modulus in these sort of cases called Pollard p-1. And that's what I used to factorize N:

```python
from Crypto.Util.number import *
from Crypto.PublicKey import RSA

with open("output.txt", "r") as f:
    output = f.read()

key_content = output.split("----------------------------------------------------------------------------")[0][:-1]
key = RSA.importKey(key_content)

n = key.n

# Taken from: https://www.uam.es/personal_pdi/ciencias/fchamizo/programming/p_sage.html
def pollard_p_auto2(n):
    aa = 2
    a = aa
    i = 0
    d = n
    if is_prime(n):
        return d
    while (d==1) or (d==n):
        i += 1
        a = Mod(a,n)^i
        d = gcd (a-1,n)
        if a == 1:
            aa += 1
            a = aa
            i = 0
    return d

print pollard_p_auto2(n)


```
The above sage script returns the desired prime number p in a couple of seconds:
```
139457081371053313087662621808811891689477698775602541222732432884929677435971504758581219546068100871560676389156360422970589688848020499752936702307974617390996217688749392344211044595211963580524376876607487048719085184308509979502505202804812382023512342185380439620200563119485952705668730322944000000001
```

And thats's pretty much it. The following code shows the private exponent computation and respective cleartext recovery:

```python
from Crypto.Util.number import *
from Crypto.PublicKey import RSA

with open("output.txt", "r") as f:
    output = f.read()

key_content = output.split("----------------------------------------------------------------------------")[0][:-1]
key = RSA.importKey(key_content)

enc = output.split("----------------------------------------------------------------------------")[1].replace("\n", "")

n = key.n

p = 139457081371053313087662621808811891689477698775602541222732432884929677435971504758581219546068100871560676389156360422970589688848020499752936702307974617390996217688749392344211044595211963580524376876607487048719085184308509979502505202804812382023512342185380439620200563119485952705668730322944000000001

q = n/p

e = 65537
d = inverse(e, (p-1)*(q-1))


fullKey = RSA.construct((long(n), long(e), long(d), long(p), long(q)))

msg = enc.decode("base64")

while True:
	dec = fullKey.decrypt(msg)
	msg = dec
	try:
		print msg.decode()
		break
	except:
		pass

```
And finally, the flag:
```
ASIS{n0t_5O_e4sy___RSA___in_ASIS!!!}
```
