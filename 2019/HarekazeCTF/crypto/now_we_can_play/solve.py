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