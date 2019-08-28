# for local testing:
# socat TCP-LISTEN:1337,fork,reuseaddr EXEC:"python2 challenge.py",pty,echo=0,stderr

from random import SystemRandom
from fractions import gcd
import sys


def test(a, d, n, s):
    x = pow(a,d, n) 
    if x == 1 or x == n-1:
        return False

    for i in range(s):
        x = x*x % n
        if x == 1:
            return True
        if x == n-1:
            return False
    return True


def is_prime(n, rounds):
    if n % 2 == 0:
        return False
    d, s = n - 1, 0
    while not d % 2:
        d, s = d >> 1, s + 1
    return not any(test(a, d, n, s) for a in R.sample(range(1,314), rounds))


def detectCheat(p, q, n):
    return not (p > 1 and q > 1 and p*q == n and p.bit_length() >= 512 and q.bit_length() >= 512 and is_prime(p, 20) and is_prime(q, 20))


R = SystemRandom()
seen_p = set()
wins = 0
games = 42
winthreshold = 0.9


print "I found new uber crypto that allows us to securely generate random numbers!"
print "Lets use this to play a very fair game of random chance!"
print "If you manage to win 90% of games, I'll give you a flag!"
print "Tell you what, I'll even give you one if you manage to lose 90%!"

for i in range(games):
    while True:
        n = int(raw_input("Give me a fresh composite n=p*q\n> "))
        for p in seen_p:
            if n % p == 0:
                print "I already know a prime factor! Use a different n: ", p
                break
        else:
            break

    r = R.randint(0, n)
    s = r*r % n
    print "Alrighty, now please give me the root of\n%d" % s
    ans = int(raw_input("> "))
    if (ans * ans) % n != s:
        print "This is wrong. I wont play with cheaters. Bye!"
        sys.exit()

    p = gcd(n, (r-ans) % n)
    q = n / p

    if p>1 and q>1:
        print "RESULT: I won! Here are your factors: ", p, q
    else:
        print "RESULT: Hrmpf you win."
        wins += 1

    print "Prove that you are not cheating!"
    p = int(raw_input("p: "))
    q = int(raw_input("q: "))
    seen_p.add(p)
    seen_p.add(q)

    if detectCheat(p, q, n):
        print "Hey! You used invalid primes! Don't try to trick me, I'll notice! Bye!"
        sys.exit()

    print "Another Round!"


if wins > winthreshold*games:
    print "Well done! You won! (%.2f)" % (wins*1.0/games)
    print "Take your flag: ALLES{FLAG-easy-winner}"
elif games-wins > winthreshold*games:
    print "Well done! You lost! (%.2f)" % (wins*1.0/games)
    print "Take your flag: ALLES{FLAG-hard-loser}"
else:
    print "Output looks random enough! (%.2f)" % (wins*1.0/games)