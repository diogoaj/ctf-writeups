### Ψ-Ф genre - 202 points (?? solves)

I was solving previous ctf crypto problems when I found a quite 
challenging one that I couldn't solve at the time of the competition (ASIS 2019 Quals). I took the code from the author's [repository](https://github.com/fact0real/asisctf/tree/master/quals-2019/crypto/Ψ-Ф%20genre) and ran the server on my machine.

Also, while I struggled with this one, I did not find any writeup online so, here is my solution.


#### Understanding the problem

The challenge presents us a server which gives 4 options:

```
| Options:
|   [E]ncryption oracle!
|   [F]lag oracle!
|   [P]hirypt oracle!
|   [Q]uit oracle!
```

Let's start from the top, the encryption oracle (E option) asks the user for a number and the server responds with the operation `pow(m, e, n)`, where `m` is the user's input, `e` is the RSA public exponent and `n` is the RSA modulus. We can see, by now, that we are dealing with the RSA cryptosystem. 

The flag oracle (F option) returns a value corresponding to the following computation: `pow(e*flag, e, n)`, which contains the `flag` value that we seek.

The third option (P) is another oracle that computes: `m % phi(n)` where `phi(n)` is Euler's totient function value for `n` which is equivalent to `(p-1)*(q-1)`, `p` and `q` being the private primes that compose the RSA modulus. 

Finally, the quit option exits the application and closes the connection to the server.


#### Computing RSA modulus N

If we want to solve this challenge we need more info. We can start by calculating the modulus `n` using the first oracle (E) that the server offers. We can do this if we use modular arithmetic concepts:

```
enc(m) = m^e mod n
enc(m) - m^e = 0 mod n 
enc(m) - m^e = in mod n -> multiple of n

enc(25) = 25^e mod n
enc(5)^2 = 5^2e = 25^e

With this, we can get a multiple of n:

(5^e)^2 - 25^e mod n = i*n mod n

We can get another multiple of n using the same idea:

(6^e)^2 - 36^e mod n = j*n mod n

Therefore, we can get the value of n times a constant k, which should be very small, if we use the GCD function:

gcd(enc(5)^2 - enc(25), enc(6)^2 - enc(36)) = k*n, where k is small
```

With this we have `n` but we still need more to work with. Let's get `phi(n)`.


#### Computing phi(n)

We will use the second oracle here. The idea in this step is similar to the one we did before. Calculate multiples of phi and use the GCD function. The following calculation worked for me:

```
Compute 2*n and 3*n and send them to the phi oracle.

gcd(2*n - 2*n mod phi, 3*n - 3*n mod phi) = phi(n)
```

And that gives us `phi(n)` which we will use to factor `n`.


#### Factoring modulus N

It is now possible to factor the modulus with access to phi(n):

```
We know that 

phi(n) = (p - 1)*(q - 1)

Expanding the equation we get:

phi = p*q - q - p + 1, p*q = n
phi = n - q - p + 1
phi - n + q + p - 1 = 0 ( multiply both sides by p )
p*phi - p*n + n + p^2 - p = 0 
p^2 + p*(phi - n - 1) + n = 0

We simply have to solve the quadratic equation to get prime number p. 
In Sagemath this is something like:

eq = p^2 + p*(phi - n - 1) + n
eq.roots()
```

We now know almost everything. We still cannot decrypt the flag's ciphertex because we don't know the public exponent e. We will do that in the next step.


#### Discovering public exponent e

This part is tricky. We do not have access to `e` and the common exponents won't work. Brute-force does not work either. However, we could try and factor either `p-1` or `q-1`. If any of these numbers are smooth, there is a pretty good chance that we can reduce the Discrete Logarithm modulo `p` or `q`, and solve the equation a lot faster.

```
An example of a possible factorization:
sage: q = 251098056194756395484481669175849167413526916127364056264269438343751622680221403475328153544217244464840550268103890323703560028678327138948165837221100166
sage: factor(q)
2 * 17 * 19^2 * 31 * 37^3 * 41 * 43 * 47 * 53 * 59 * 61^2 * 71 * 79^2 * 101 * 103 * 131 * 163 * 191 * 197 * 211 * 233 * 241 * 251^2 * 293 * 443 * 577 * 701 * 709 * 727 * 733 * 1187 * 1423 * 2237 * 2591 * 3389 * 3727 * 3989 * 4049 * 4507 * 4513 * 4547^2 * 6619 * 7477 * 7727 * 7993 * 13001 * 13093 * 16139 * 18059 * 32713 * 59141
```

This particular example was factored instantly by Sage. We can now proceed and solve the Discrete Logarithm:

```
DLP: g^a = b mod p

We want to find a (in the case of the challenge we want to find e). 

If the prime number p is strong, this calculation is computationally hard. 

However, if p-1 is smooth, we can use Pohllig-Hellman's algorithm, which makes the problem a lot easier.
```

With this in mind, we'll get `e`:

```
Ask the encryption oracle to cipher 2 for example:
c1 = 2^e mod n

We can reduce this problem modulo q:
c2 = c mod q

This is now a solvable problem. In Sagemath:
e = discrete_log(c2, Mod(2, q))
```

#### Recovering the flag

We now have everything that we need to recover the flag. Some last computations:

```python
flag_value = pow(e*flag, e, n) # From oracle F

d = inverse_mod(e, phi)
m = pow(flag_value, d, n)

# m now contains e*flag, we need the inverse of e mod n to get the flag

e_inv = inverse_mod(e, n)

flag = m*e_inv % n

print long_to_bytes(flag)
```

Finally, the flag:
```
ASIS{___RSA___DLP___Wh47S_tH3_Pr0Bl3M?!!!}
```