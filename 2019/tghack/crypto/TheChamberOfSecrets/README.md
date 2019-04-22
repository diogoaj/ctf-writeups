### The Chamber of Secrets - 300 points (6 solves)

> I was walking down a dark corridor one evening when I suddenly heard some whispering from the walls around me. I couldn't quite hear what it said, so when the thing whispering started moving, I obviously followed. What could go wrong, right? After a while, I turned a corner and looked right into some red text on a wall. It said:

```
public(h, a, b, q, g)  
h = (829999038570486 : 549144410878897 : 1)   
a = -3    
b = 313205882961673   
q = 1125899906842597   
g = (1115545019992514 : 78178829836422 : 1)  
c = ((700253548714057 : 421820716153583 : 1), (470712751668926 : 131989609316847 : 1))  

sTokhflo9WHPQB8JHEm0OVG2SwUA/sHaP0yFv9T2kmoZjC5g46eeRM8M8CGRj8bV/NxY4VJ8Ls0=
```

> When standing there pondering who in their right minds would write something like that on a wall, the whispers grew louder and I finally heard what it said:

```python
key =  SHA256.new()  
key.update(secret)  

def bf_encrypt(key, message):  
    bs = Blowfish.block_size  
    iv = Random.new().read(bs)  
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)  
    pad_len = bs - divmod(len(message), bs)[1]  
    padding = [pad_len]*pad_len  
    padding = pack('b'*pad_len, *padding)  
    return base64.b64encode(iv + cipher.encrypt(message + > padding))  
```
> All of this sounds like gibberish to me, but maybe someone capable of speaking old, mythical languages can decipher the whispers and recover the secrets of old...


The first part of the challenge was a bit guessy. We had a couple of public parameters `h`, `a`, `b`, `q` and `g`. By the looks of the values, I assumed it had to be an Elliptic Curve cryptosystem. Also, the `c` value reminded me of the [Elgamal](https://en.wikipedia.org/wiki/ElGamal_encryption) cryptosystem since it had two values for the ciphertext.

So this is what I did, I tried to map all values to Elliptic Curve parameters. For example, `a` and `b` had to be parameters of the curve's equation, `q` is a prime number so it must be the parameter that defines the field. Later, I found out a [StackExchange](https://crypto.stackexchange.com/questions/9987/elgamal-with-elliptic-curves#9990) post that discussed this type of encryption scheme. 

The rest of the values were points of the curve. `h` being the public key as in Elgamal cryptosystem, `g` is a point of order N (generator in the Elgamal system). Finally, `c` was the ciphertext as expected and the random base64 string that appears at the bottom, is yet another ciphertext that we need to decipher with the Blowfish cipher as suggested by the Python function.

Given the values that we just mapped I figured I could recover the private key `x` by calculating the Discrete Logarithm between `h` and `g`. This is because, the public key `h` is given by:

```
h = x*g
```

Since the values are small, it is quite easy to calculate the key. Having the private key, we can now decrypt the `c` value:

```
C' = c1*x
P = c2 - C', where P is the plaintext
```

Finally, after a bit more guessing, I discovered that the Blowfish key was the X value of the plaintext, leading to the decryption of the base64 and flag retrieval.

For the Elliptic Curve part, I created a Sage script as follows:

```python
## ElGamal Elliptic Curve decryption

a = -3
b = 313205882961673
q = 1125899906842597

E = EllipticCurve(Zmod(q), [a, b])

g = E(1115545019992514, 78178829836422)
h = E(829999038570486, 549144410878897)
c1 = E(700253548714057, 421820716153583)
c2 = E(470712751668926, 131989609316847)

x = g.discrete_log(h)

print "[+] x:", x

C_ = c1*x
P = c2 - C_

print "[+] key:", P[0]
```

The output:

```
$ sage solve.sage
[+] x: 29131765433887
[+] key: 934013602642177
```

And here is the Python code I used to get the flag:

```python
from Crypto.Cipher import Blowfish
from Crypto.Hash import SHA256
import base64

b = "sTokhflo9WHPQB8JHEm0OVG2SwUA/sHaP0yFv9T2kmoZjC5g46eeRM8M8CGRj8bV/NxY4VJ8Ls0="

key =  SHA256.new()

# Insert key here
key.update(b"934013602642177")

def decrypt(key, message):
	enc = base64.b64decode(message)
	iv = enc[:Blowfish.block_size]
	cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
	return cipher.decrypt(enc[Blowfish.block_size:])

print(decrypt(key.digest(), b))
```

And so, the flag is:

```
TG19{please_be_more_discreet_when_hacking}
```