### ONCE UPON A TIME - 100 points (71 solves)

> Now!! Let the games begin!!

The following code shows the cipher being used on the flag that we have to break:

```python
#!/usr/bin/python3
import random
import binascii
import re
from keys import flag

flag = re.findall(r'HarekazeCTF{(.+)}', flag)[0]
flag = flag.encode()
#print(flag)

def pad25(s):
    if len(s) % 25 == 0:
        return b''
    return b'\x25'*(25 - len(s) % 25)

def kinoko(text):
    text = text + pad25(text)
    mat = []
    for i in range(0, len(text), 25):
        mat.append([
            [text[i], text[i+1], text[i+2], text[i+3], text[i+4]],
            [text[i+5], text[i+6], text[i+7], text[i+8], text[i+9]],
            [text[i+10], text[i+11], text[i+12], text[i+13], text[i+14]],
            [text[i+15], text[i+16], text[i+17], text[i+18], text[i+19]],
            [text[i+20], text[i+21], text[i+22], text[i+23], text[i+24]],
            ])
    return mat

def takenoko(X, Y):
    W = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    for i in range(5):
        for j in range(5):
            for k in range(5):
                W[i][j] = (W[i][j] + X[i][k] * Y[k][j]) % 251
    return W

def encrypt(m1, m2):
    c = b""
    for mat in m1:
        g = random.randint(0,1)
        if g == 0:
            mk = takenoko(m2, mat)
        else:
            mk = takenoko(mat, m2)
        for k in mk:
            c += bytes(k)

    return c


if __name__ == '__main__':
    m1 = kinoko(flag)
    m2 = [[1,3,2,9,4], [0,2,7,8,4], [3,4,1,9,4], [6,5,3,-1,4], [1,4,5,3,5]]
    
    
    print("Encrypted Flag:")
    enc_flag = binascii.hexlify(encrypt(m1, m2)).decode()
    print(enc_flag)

```

And the result of ciphering is given by:
```
Encrypted Flag:
ea5929e97ef77806bb43ec303f304673de19f7e68eddc347f3373ee4c0b662bc37764f74cbb8bb9219e7b5dbc59ca4a42018
```


#### 1. Understanding the algorithm

If we look at the first line of the main function, we see that the flag is passed to the `kinoko` function which pads the flag with the `%` character and constructs two 5x5 matrices where each cell contains a letter of the flag.

Then, on the second line of main, another 5x5 matrix is initialized with what seems to be the key. At the end, the encrypt function is called using the plaintext and key matrices as argument.

When encrypting, the `takenoko` function is called twice to encrypt the two matrices initialized in the beginning. The encryption is quite simple and it is given by the following line:

```python
W[i][j] = (W[i][j] + X[i][k] * Y[k][j]) % 251
```

This right here is just matrix multiplication modulo 251. The only unknown here is either `X` and `Y` depending on the result of ```g = random.randint(0,1)```. Because of that, we have two equations to try:

![equation 1](https://github.com/diogoaj/ctf-writeups/blob/master/2019/HarekazeCTF/crypto/once_upon_a_time/resources/equation1.png)

![equation 2](https://github.com/diogoaj/ctf-writeups/blob/master/2019/HarekazeCTF/crypto/once_upon_a_time/resources/equation2.png)

#### 2. Solution

To solve this problem, we just need to solve the equations and obtain the matrices that each contain half the flag. Turns out, the algorithm used the first equation for the two iterations of the cipher. 

I wrote a script leveraging SageMath functions to easily solve this. The code is as follows:

```python
import binascii
enc = "ea5929e97ef77806bb43ec303f304673de19f7e68eddc347f3373ee4c0b662bc37764f74cbb8bb9219e7b5dbc59ca4a42018"

c = binascii.unhexlify(enc)

K = [[1,3,2,9,4], [0,2,7,8,4], [3,4,1,9,4], [6,5,3,-1,4], [1,4,5,3,5]]

mattrix_lines = [c[i:i+5] for i in range(0, len(c), 5)]

W1 = mattrix_lines[0:5]
W2 = mattrix_lines[5:10]

W_1 = []
W_2 = []

for line in W1:
	t = []
	for j in range(len(line)):
		t.append(ord(line[j]))
	W_1.append(t)

for line in W2:
	t = []
	for j in range(len(line)):
		t.append(ord(line[j]))
	W_2.append(t)

W1 = matrix(GF(251), W_1)
W2 = matrix(GF(251), W_2)
K = matrix(GF(251), K)

first_half = K.solve_left(W1)
second_half = K.solve_left(W2)

flag1 = ""
flag2 = ""
for i in range(5):
	for j in range(5):
		flag1 += chr(first_half[i][j])
		flag2 += chr(second_half[i][j])

print "HarekazeCTF{" + (flag1+flag2).replace("%", "") + "}"
```

Running the script gives us the flag:

```
HarekazeCTF{Op3n_y0ur_3y3s_1ook_up_t0_th3_ski3s_4nd_s33}
```