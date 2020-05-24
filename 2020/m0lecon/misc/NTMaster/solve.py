from pwn import *

HOST = "challs.m0lecon.it"
PORT = 10000

r = remote(HOST, PORT)

r.recvuntil("You have 1 second for each of the 10 tests.")

for _ in range(10):
	r.recvline()
	line = r.recvline()
	N = int(line.split(b"N = ")[1])

	send = str(N-1) + " 1"
	r.sendline(send)
r.interactive()

# ptm{as_dumb_as_a_sanity_check}
