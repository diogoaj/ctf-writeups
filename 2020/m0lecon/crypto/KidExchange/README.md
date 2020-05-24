### Kid Exchange - 90 points (70 solves)

> In our super secret agency we don't trust standard protocols. We even have our own way to trade keys! I bet you won't find any issue

For this challenge, we are given two python scripts and a packet capture file (pcapng). The scripts `alice.py` and `bob.py` contain a key exchange between alice and bob similar to a Diffie-Hellman key exchange where private values are generated and later transformed after a couple of computations modulo `2^128`. Two public values are then exchanged between the two so that the shared key can be created and used to encrypt the flag. The public values can be extracted from the packet capture as well as the encrypted bytes. 

The following scripts show the given python scripts containing the exchange operations: 

```python
#alice.py

import os
import socket
from Crypto.Cipher import AES

def pad(m):
	return m + b'\x00'*((-len(m))%16)

HOST = ''
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()

n = 128
m = 2**n

x = [int.from_bytes(os.urandom(n//8),'big') for _ in range(4)] #private key
e1 = (x[0] * x[1]) % m
e2 = (x[2]**2 + 3 * x[3]) % m
p1 = (e1**2 - 2 * e1 * e2 + 2 * e2**2) % m
p2 = (e1 * e2) % m
conn.sendall(str(p1).encode()+b'\n')
conn.sendall(str(p2).encode())
r = ''
while True:
	c = conn.recv(1).decode()
	if c != '\n':
		r += c
	else:
		break
p3 = int(r)
p4 = int(conn.recv(1024).decode())
e3 = (p3 + 4 * p4) % m
e4 = pow(3, p3 * e3, m)
e5 = pow(e1, 4, m)
e6 = pow(e2, 4, m)
e7 = (e5 + 4 * e6) % m
k = pow(e4, e7, m)
key = int.to_bytes(k, 16, 'big')

cipher = AES.new(key, AES.MODE_ECB)
flag = open('flag.txt', 'rb').read()
c = cipher.encrypt(pad(flag))
conn.sendall(c)
conn.close()
```

```python
# bob.py

import os
import socket
from Crypto.Cipher import AES

HOST = ''
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

n = 128
m = 2**n

x = [int.from_bytes(os.urandom(n//8),'big') for _ in range(4)] #private key
e1 = (x[0] * x[1]) % m
e2 = (x[2]**2 + 3 * x[3]) % m
p1 = (e1**2 - 2 * e1 * e2 + 2 * e2**2) % m
p2 = (e1 * e2) % m
s.sendall(str(p1).encode()+b'\n')
s.sendall(str(p2).encode())
r = ''
while True:
	c = s.recv(1).decode()
	if c != '\n':
		r += c
	else:
		break
p3 = int(r)
p4 = int(s.recv(1024).decode())
e3 = (p3 + 4 * p4) % m
e4 = pow(3, p3 * e3, m)
e5 = pow(e1, 4, m)
e6 = pow(e2, 4, m)
e7 = (e5 + 4 * e6) % m
k = pow(e4, e7, m)
key = int.to_bytes(k, 16, 'big')

cipher = AES.new(key, AES.MODE_ECB)
flag = s.recv(1000000)
print(cipher.decrypt(flag))
s.close()
```
This is a custom key exchange so it must be broken somehow and it seems like there is a lot going on. We can start by trasncribing the python code into formulas so that we get a better understanding of the algorithm under the hood.

![part1](https://github.com/diogoaj/ctf-writeups/blob/master/2020/m0lecon/crypto/KidExchange/resources/part1.png)

After the "public" values are exchanged we have:

![part2](https://github.com/diogoaj/ctf-writeups/blob/master/2020/m0lecon/crypto/KidExchange/resources/part2.png)

So now we need a way to find a flaw in this exchange in order to compute the key ourselves. The key is given by `k = e4^e7 mod m`. Notice that we can compute the base `e4` since that all we need are the public values from bob `p3` and `p4`.
By manipulating the values that we have access to, we can also get the exponent `e7`:

![part3](https://github.com/diogoaj/ctf-writeups/blob/master/2020/m0lecon/crypto/KidExchange/resources/part3.png)

With this we can calculate the shared key `k` and decrypt the text. The following is the script used for the solution:

```python
from Crypto.Cipher import AES

import binascii

p1 = 273788890796601263265245594347262103880
p2 = 258572069890864811747964868343405266432
p3 = 26837497238457670050499535274845058824
p4 = 40856090470940388713344411229977259912

m = 2**128

t = p1 + 2*p2
t = pow(t, 2, m)
sub = 4*pow(p2, 2, m)

exp = (t - sub) % m
base = pow(3, p3*(p3+4*p4), m)
key = pow(base,exp,m)

key = int.to_bytes(key, 16, 'big')

cipher = AES.new(key, AES.MODE_ECB)
flag = "0132d91407e1966198bdebc43909ed3acc19028b85cebc5a01ef8e44b12af5b3695468f754703aba741455846c8017760521d2e79e506a732f7a61cfbce5b93363062682d80c7680afb2a7554e59548f72bdd67276539faaf1125a1e0883927c81f4b931ccbbec1940501871db587ce4617bf54050fa6e2c26aed90eb94fc466b7be3727405dfe3095577ef6a6b5bb4d0ca2fcbf58b780b71cfb21159a0b339d194bdb157bdd190e80f1bceb5f54535c0f50cb74fbb849705d248a5d272ccb89b1cf153848d0d4544170d4494cee2cd80ab317e19f780656e090062574488d8461be453b7ca46530fdeb14aee1d0500606cfa77704a29bcc54e8731a61018f6a87943cb375e8e61e2bcdb3af4d39584cbcdf31c07feb2d7f204f12b3e6e3cf8b872ad64d3cf54287942d250c7e4494014a20b3b010a715c1e68a3dacd7018a6ebfd2b4ccc6c32b4241b71417936e16948a782a7be2488458906703c2e5552333bfdc04e1867c0d206eb6476d276726f270541b4a85e76d8d799aa8fa7fe1e9f40a8d561b712f583dd68d78135dc57fc2bb841e2ac53d8b4cad6670c90de5aafd1a3650b0678eb2c9824f8153ef98c8a481a667f2f4c9e1b5d571a881f86f2c860fc84909b1887d097acd427022fc3c81fef966b993963cf83f3888ba751cc560aa91f2998581cb433e5e8f3f4cf2a5054b3f5123ffd3c097529b56e138349a1a9ce677a4346956d6b75d80795dd38add905b34c844d6fb1c898bae7a2e0c8ebfdcef81bd0d3f0c09e640347ac1a515507838796e629a2eb05d4d7f230ca529be6a6e3205804b5b71ef6c96e7978b6dc0571cf709e91ccd33f2c533f235d2e190dbee0f8827ff79124414c950e4f0c6ca66de01819cc16fad9b8057755d9039ed10d9f6074127bcfce3c4be1edc645daa978971a1e29a219f10a20ff3f43e8dab00bade4fc8ed23ce53d30a9df36c310d78f1f85c63177395b6d3f1c26b2de95184d46c3ac987730084861fd3d99b2b70b123d4d72487c20f5f88f1251ddf748bd92693a0519811d6c2ddaf45460f3eb37dbfe1733cd6d0b71925eac5aa21783896d3130507a526aee5350c0755b24cf9494b45d4e09f37c8434e3a1ee109a8f12ce43ea54bf802941057b23a3527c27d1f4810c58cf658ecd8947d959d6aebc2b434ec3341d685a7548b68fb750f059f3b4e87a583f5923103e5e59edb09ce016c3c6ab4d54adc2cdd2037cdd9aeee46adc9d9486802acccf5812966bfb8568c9f0b905a0bc55be80e2bc1ce30c9640062f0774451bc13905d21db1af83d1fc72278aca91215b8bfb8c25daa97deab0697152cc483b37fa5e091fa4c853022932b531bee05e7166f0a3e5c68417ea4045cbcf14319f0bd1d04be80e9b7ab1b9a8babdadb8c647be075f6df0c840283f63dd1b572ee39557426fd295c0196635b77b2230a17b8c2f8fc05ec8363521590dafec287a2d7d7683026b8d73c931d3c58af0ca7d3f23cc7a2a3687e86c1f8cc4a9b24e2fbddd169d0021e8e795fbb7465c03d68d050a08df8bc0ae2627718a984c46d51e2ed81fa86877076241450046f68aac7ec053e3c078ed8d4935803e4b89af24ff13bbb27d17c73f7b4c88fa15db82225d0d91cc8d7e548e3625828b6dde977dfe68ea56db21b8ef8d292367ac1d2f88431620b93bbcec620a14a7510cd8aaaf1f2d6299dcd92aa6c756725bef6802fba7365515c2510cf9d70c1c0d9410f59439f51b40fac3d93492b4174628a5ce7e5f7debcb1fe99405d4d72ff3d03b5f7e9bc054beb864cc8476daed556837318390ae4ef3308e09e1ed52524fc0694acfb51e8134de6db0c13c58a78e537f683ecaab85f61e3b818c9d5deec7df968eff0f1e9f476b1b38b4c2abd072dba426a685a21eed4fde620935b7a2c22dfa62387ba41762dcc7bdf22ad651efe537cdd633bb73c7bf9168b4cdf266d18eb80bfc594711ade8eb2be84c25d67e8eb700c235372c7e41637168dde519ab0741d1256b64fde2d267d68c703a03c2ebe317c4d7298181ef6deaaa437ade168b5e24a4d4f1a7e46af5a4e81c067316c4d36a467733ab6adf1854f43b8505717e5bd56cfd429dd8df349b895938359851c1b229d421fb3df4b6c092d759818b7481c38269027267764cd5816d9fa0622164b370ccf69f90c24f52bd109a260cf7343d9ed2249396f32a17674ebe2ef766da44e57298d2964095e435bcd45a24a84f498b6e26676cb64508bcfcc288d7e65ade1adaeec09120c7442e1c560abbe36dfa35e1e0f25b73cce406926ba90afe3be4dfd2982229523310d90ccf33175054a619946c8219302ad1d4db7a1aad23d7ef3d9087ae9729aa6faae8d4c71ff997ca9248e0ef3ed9df2436803f167271cf5e03c2423fee19ed1b44312610466459c3fb6246c20e1c2ef7b0d56e9590e290ce7c8ebe09809e294dbd354243ad69e31645eb1a10ae2e2cb18e05cd1bbf092bd779ceacf8e0fa6da60312ac3676a79f908398e012972acdfb50a842667640a2d122cd4b488a8312fc7f1be67d986de7771c5919f251c602496edaf07acdcdebfe24a3068182fc60a51ebbf95e01cb7b338fae0d87d853a67235a9d00f5a663bdae86ccc39de17e5fd83429913f0e07c66390367dca69e4b99b6bc67a0280b1f43371a54fa5a5bee6d76090264a73b8afec83aed5e8592590b5a8b303b2cebaa5aa3ab247607ba0a8d405e6dfcbfd"
flag = binascii.unhexlify(flag)

print(cipher.decrypt(flag).decode())
```

The script execution outputs the decrypted text:
```
At first I was afraid, what could the answer be?
It said given this position find velocity.
So I tried to work it out, but I knew that I was wrong.
I struggled; I cried, "A problem shouldn't take this long!"
I tried to think, control my nerve.
It's evident that speed's tangential to that time-position curve.
This problem would be mine if I just knew that tangent line.
But what to do? Show me a sign!

So I thought back to Calculus.
Way back to Newton and to Leibniz,
And to problems just like this.
And just like that when I had given up all hope,
I said nope, there's just one way to find that slope.
And so now I, I will derive.
Find the derivative of x position with respect to time.
It's as easy as can be, just have to take dx/dt.
I will derive, I will derive. Hey, hey!

And then I went ahead to the second part.
But as I looked at it I wasn't sure quite how to start.
It was asking for the time at which velocity
Was at a maximum, and I was thinking "Woe is me."
But then I thought, this much I know.
I've gotta find acceleration, set it equal to zero.
Now if I only knew what the function was for a.
I guess I'm gonna have to solve for it someway.

So I thought back to Calculus.
Way back to Newton and to Leibniz,
And to problems just like this.
And just like that when I had given up all hope,
I said nope, there's just one way to find that slope.
And so now I, ptm{w3ak3r_vers1on_0f_DH} I will derive.
Find the derivative of velocity with respect to time.
It's as easy as can be, just have to take dv/dt.
I will derive, I will derive.

So I thought back to Calculus.
Way back to Newton and to Leibniz,
And to problems just like this.
And just like that when I had given up all hope,
I said nope, there's just one way to find that slope.
And so now I, I will derive.
Find the derivative of x position with respect to time.
It's as easy as can be, just have to take dx/dt.
```

And here is the flag;

```
ptm{w3ak3r_vers1on_0f_DH}
```
