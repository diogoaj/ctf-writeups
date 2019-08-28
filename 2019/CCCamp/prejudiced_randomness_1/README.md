### Prejudiced Ratndomness 1 - 123 points (39 solves)

> I found new uber crypto that allows us to securely generate random numbers! Lets use this to play a very fair game of random chance. Win the game!

> nc hax.allesctf.net 7331

We are given the code of a server which generates random bits in a form of a game of chance. For each iteration of the game, the server asks us a number composed of two prime numbers, calculates a random number and computes its square modulo `N` (our input). The server then asks for a root of:

```
s = r^2 mod n, given s
```

The server takes the root we give and tries to factor `N` using the GCD function:

```
p = gcd(n, (r - ans) % n)
```

There is a 50% chance that `p` divides `N` as the value `s` can have four roots. Thus, the bit generator should be pretty random. The objective of this problem is to fool the number generator in order to win everytime, that is, give a solution to the equation that does not allow the server to factor `N`.

The solution is actually simple. The server does not check if the primes numbers we give are equal and so, we can input an `N = p^2`. Turns out, this equation has only two roots and none of them can factor `N`. 

The solution is: generate a prime in each iteration and compute its square, feeding it to the server. We then calculate the square root modulo `p^2`. This is easy if the modulo is a prime. In this case, the module is a square of a prime. We should be able to calculate the root modulo `p` and use [Hansel's lemma](https://en.wikipedia.org/wiki/Hensel%27s_lemma) to lift the solution modulo `p^2`. We then just need to insert one of the roots and we will always fool the server.

The main loop of my solution is as follows:

```python
for _ in range(42):
    r.recvuntil(">")
    p = getPrime(512)

    n = p**2

    r.sendline(str(n))

    r.recvuntil("Alrighty, now please give me the root of")

    r.recvline()
    chall = r.recvline()
    chall = chall.replace("\n", "").replace(">", "").replace(" ", "")

    roots = prime_mod_sqrt(int(chall), p)

    # Hansel's Lemma 
    z = inverse(2*roots[0], p)
    x = ((int(chall)-roots[0]**2) / p) % p 
    y = x*z % p 
    root = (roots[0] + y*p) % p**2

    r.sendline(str(root))
    line =  r.recvline()
    print line

    r.recvuntil("p:")
    r.sendline(str(p))

    r.recvuntil("q:")
    r.sendline(str(p))
```


The flag is:

```
 ALLES{m4ster_of_r4ndomn3zz_squ4red}
```

