### Hush Hush - 150 points (22 solves)

>  Can I get a hash collision?
>
> nc 89.38.210.129 6665

For this challenge, we are given a service to connect to and the code for the respective service. When we established connection, we were asked two inputs and if the inputs were different but with equal md5 hashes, we would get the flag. Meaning that we would need to generate a hash collision. However, the problem was pretty simple as it had a big flaw in the following function:

```python
# can't break it
def my_hash(x):
    global n
    x += "piper"
    x = int(x.encode('hex'), 16)
    for i in range(32):
        x = pow(x, x, n)
        x +=1
    m = md5.new()
    m.update(hex(x))
    return m.hexdigest()
```

When we pass our input string, the word ```piper``` is concatenated. The input is converted into decimal and then a sequencial exponentiation is computed finishing with the calculation of the digest. Because the above word is concatenated, we can send nothing as input and that word will be hashed. On the other hand, if we send a null byte ```\x00```, we get the same result. And since ```''``` and ```\x00``` are different, we get the flag.

```python
from pwn import *

HOST = "89.38.210.129"
PORT = 6665

r = remote(HOST, PORT)

input1 = b'\x00'
input2 = ''

r.recvuntil("First input:")
r.sendline(input1)

r.recvuntil("Second input:")
r.sendline(input2)

r.interactive()
```

The flag is:
```
timctf{d0UbT_3verYTH1nG}
```