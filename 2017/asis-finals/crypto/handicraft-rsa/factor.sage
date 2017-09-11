from Crypto.Util.number import *
from Crypto.PublicKey import RSA

with open("output.txt", "r") as f:
    output = f.read()

key_content = output.split("----------------------------------------------------------------------------")[0][:-1]
key = RSA.importKey(key_content)

n = key.n

def pollard_p_auto2(n):
    aa =2
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