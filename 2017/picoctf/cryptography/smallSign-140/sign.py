import socket
import time
import random
import itertools
import sys
from sympy.ntheory import factorint

signatures_map = {}

def erat2():
    D = {  }
    yield 2
    for q in itertools.islice(itertools.count(3), 0, None, 2):
        p = D.pop(q, None)
        if p is None:
            D[q*q] = q
            yield q
        else:
            x = p + q
            while x in D or not (x&1):
                x += p
            D[x] = p

def get_primes_erat(n):
  return list(itertools.takewhile(lambda p: p<n, erat2()))

def factors(n):    
    return factorint(n)

def connect(hostname, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.recv(1024) # discard this message
    data = str(s.recv(1024)).split(":") 

    # Get N 
    N = int(data[1].split("\\")[0].strip())

    # send values to sign 
    for i in range(130):
        r = prime_list[i]
        value = str(r) + '\n'
        s.send(value.encode())
        time.sleep(0.4)
        data = str(s.recv(1024)).split(":")[1]
        signature = data.split("\\")[0].strip()
        signatures_map[r] = signature

    s.send(b'-1\n')
    time.sleep(0.4)
    challenge = str(s.recv(1024)).split(":")[1]
    challenge = challenge.split("\\")[0].strip()

    fact = factors(int(challenge))

    result = 1
    for factor in fact:
        if factor not in signatures_map:
            print(factor)
            print(fact)
            print("Not the primes we needed...")
            return
        else:
            result = result * pow(int(signatures_map[factor]), fact[factor],N)

    print(fact)
    result = result % N
    result = str(result) + "\n"

    print("All found, lets goooooooOoooo!")
    s.send(result.encode())
    time.sleep(1)
    print(str(s.recv(1024)))
    s.close()

prime_list = get_primes_erat(10000)
while True:
    connect("shell2017.picoctf.com", 7541)
