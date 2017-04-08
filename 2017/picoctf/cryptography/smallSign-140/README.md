### smallSign - 140 points

> This service outputs a flag if you can forge an RSA signature!
nc shell2017.picoctf.com 7541

Hint:
> 	RSA encryption (and decryption) is multiplicative.

This challenge involves forging a RSA signature. We are given the following code running at port 7541 on the server:

```python
#!/usr/bin/python -u

from Crypto.PublicKey import RSA
import random
import signal

key = RSA.generate(2048)

print ("You have 60 seconds to forge a signature! Go!")
# In 60 seconds, deliver a SIGALRM and terminate
signal.alarm(60)

print ("N:", key.n)
print ("e:", key.e)

while True:
    m = int(input("Enter a number to sign (-1 to stop): "))
    if m == -1:
        break
    sig = key.sign(m, None)
    print ("Signature:", str(sig[0]))

challenge = random.randint(0, 2**32)
print ("Challenge:", challenge)
s = int(input("Enter the signature of the challenge: "))
if key.verify(challenge, (s, None)):
    print ("Congrats! Here is the flag:", flag)
else:
    print ("Nope, that's wrong!")
```
When we connect to the server we are given the modulus "N" and the public exponent "e". After that, we can ask the server to sign any number we want and the signature of that number is returned. Here is an example of an interaction:

```
You have 60 seconds to forge a signature! Go!                                          
N: 25681272343974341804956006126786420486348491060984957175234630606694634071486214446485762384538445370093843703087489201667383915253135861048191942025323531249439409148246393294936871034311024518439434220286298947308297993489690387179290032063686758124730441859024735614036256091121152957366927440296590852883940872380884354458736325330494572678772103897295046136591822105407765735471780103163025244067321267043022765832731289976065354472996942271616794473965371626172544468146210013451571410980389838662683380361886188403352537189060227164082350896255967277883171412563790145370025146592439856778150255780254400191767                                                                            
e: 65537                                                                               
Enter a number to sign (-1 to stop): 123                                               
Signature: 1633417085612390524139783221307238496022071408139460246195558522398829916969
9320203727417845838792736224000300897388929525218093245892383807835311158740672402275704857294291627634097503929509366790281770494496100374778363968540442311938125836768462473757697404404872505827789119228883493163698302482908231834203530761707563595402631506568221217257851284652543987987924808360184498801376058068054202162258631976213720084835758121241133845548316677689486648291677304056075305657331399327977019917246286854788659548762570857071187105462281454770156658386858785413311097508971170750551576443363614919043145097949312884924                                                                    
Enter a number to sign (-1 to stop):     
```
After we press "-1", the server issues a challenge, that is, a randomized number that we have to sign. If the signature is correct we are given the flag. The only problem is, we only have 60 seconds to do so.

The hint gives us a pretty good idea of how we should approach this problem. Imagine if the challenge we have to sign is 20 but we don't have the private exponent to sign it. So, the idea is to get the signatures of each factor of 20 (in this case, it would be: 5,2,2 because 5 * 2 * 2 = 20), because each factor signature multiplied gives us the value we want signed, since RSA is multiplicative.
```
The RSA signature signature is given by:
S = m^d mod N

So, given two messages m1 and m2, the signature of the multiplication between the two is given by:
S = (m1*m2)^d mod n
```
With this in mind, I wrote a script that would connect to the server and get the signatures for the first 130 prime numbers. With a little bit of luck, with those 130 primes, we can multipliy some of them to give us the integer we have to sign. And with that, the target signature!

After running the script on some terminals, and a couple of minutes later, the flag is returned !

```
ad4b118a7296792be34a29ee5180daba
```
___
**Thanks to:**
- [@RicardoPereiraIST](https://github.com/RicardoPereiraIST) for helping solving the problem and correcting the script.

