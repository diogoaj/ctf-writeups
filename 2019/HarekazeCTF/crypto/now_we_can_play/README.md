### Now We Can Play!! - 200 points (34 solves)

> It is just a simple cryptography game. When you get a flag, YOU WIN!!
> 
> nc problem.harekaze.com 30002

The challenge presents us the following code:

```python
#!/usr/bin/python3
from Crypto.Util.number import *
from Crypto.Random.random import randint
from keys import flag

def genKey(k):
    p = getStrongPrime(k)
    g = 2
    x = randint(2, p)
    h = pow(g, x, p)

    return (p, g, h), x

def encrypt(m, pk):
    p, g, h = pk
    r = randint(2, p)

    c1 = pow(g, r, p)
    c2 = m * pow(h, r, p) % p
    return c1, c2

def decrypt(c1, c2, pk, sk):
    p = pk[0]
    m = pow(3, randint(2**16, 2**17), p) * c2 * inverse(pow(c1, sk, p), p) % p
    return m


def challenge():
    pk, sk = genKey(1024)
    m = bytes_to_long(flag)
    c1, c2 = encrypt(m, pk)

    print("Public Key :", pk)
    print("Cipher text :", (c1, c2))

    while True:
        print("---"*10, "\n")
        in_c1 = int(input("Input your ciphertext c1 : "))
        in_c2 = int(input("Input your ciphertext c2 : "))

        dec = decrypt(in_c1, in_c2, pk, sk)
        print("Your Decrypted Message :", dec)

if __name__ == "__main__":
    challenge()
```

The `challenge` function is straightforward. Some keys are generated, the flag is encrypted and the `while` loop is just a decryption oracle. 

The cryptosystem used here is Elgamal and we are given the public key `(p,g,h)` and the ciphertext `(c1, c2)`. The decryption oracle has a twist and it does not decipher the flag completely as we would expect. 

In the Elgamal cryptosystem, the message is given by:

![equation 1](https://github.com/diogoaj/ctf-writeups/blob/master/2019/HarekazeCTF/crypto/now_we_can_play/resources/equation1.png)

Where c1 and c2 are given by:

![equation 2](https://github.com/diogoaj/ctf-writeups/blob/master/2019/HarekazeCTF/crypto/now_we_can_play/resources/equation2.png)

![equation 3](https://github.com/diogoaj/ctf-writeups/blob/master/2019/HarekazeCTF/crypto/now_we_can_play/resources/equation3.png)

Normally, the first equation should give us the plaintext but that is not the case here. Here is the line of code that matters:

```python
m = pow(3, randint(2**16, 2**17), p) * c2 * inverse(pow(c1, sk, p), p) % p
```

With this information, the decryption equation is something like:

![equation 4](https://github.com/diogoaj/ctf-writeups/blob/master/2019/HarekazeCTF/crypto/now_we_can_play/resources/equation4.png)

There is an extra factor here that prevents us to read the flag directly. To get the original message, we need the multiplicative inverse of `3^r` to cancel out that factor. If we look closely at how this number is generated, we see that the random number chosen `r` is very small and so, this allows us to brute-force this value and calculate all inverses between `3^(2^16)` and `3^(2^17)`. Then, multiply each one by `m'` until we see the flag.

Here is the code that solves the problem:

```python
from pwn import *
import gmpy2

r = remote("problem.harekaze.com", 30002)

pk = r.recvuntil("))")
c = r.recvuntil("))")

r.recvuntil(":")

p = long(pk.split(",")[1].replace(" (", ""))

c1 = c.split(",")[1].replace(" (", "")
c2 = c.split(",")[2].replace(" ", "").replace("))", "")


l = []

for i in range(2**16, 2**17):
	l.append(gmpy2.invert(pow(3,i,p), p))

r.sendline(c1)
r.sendline(c2)

dec = r.recvuntil(")")

dec = dec.split(",")[1].replace(" ", "").replace(")", "")

dec = long(dec)

for num in l:
	m = (dec * num) % p
	try:
		m = hex(m)[2:].decode("hex")
		if "Harekaze" in m:
			print m
			break
	except:
		pass
```

And here is the flag;

```
HarekazeCTF{im_caught_in_a_dr3am_and_m7_dr3ams_c0m3_tru3}
```

