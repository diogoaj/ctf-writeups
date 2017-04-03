### weirderRSA - 175 points
> Another message encrypted with RSA. It looks like some parameters are missing. Can you still decrypt it?

Hints:
> 	- Is there some way to create a multiple of p given the values you have?
> 	- Fermat's Little Theorem may be helpful.

This was a tough one. The message we are given comes with incomplete RSA parameters and we still have to decrypt the ciphertext provided. The parameters are:
```
e = 65537
n = 352758655756163603130656475864162239004344663459120398951306959672239055329877644796995008368282924624780849432051543118959312685532106237568240835778731486989439626252834661294225426875963944816709371554839452465119058016363040631618359944564550348310851045841670935254841385590882490443247265126417117450357
dp = 13530055667815347122266109008252377134325151556131892235929064596659462917644020624855537451062167377041847601387880412738836767351591511886432133011921729
c = 23428056833770750219439218340180501853506449797628734848807388355447212714387039203998085387476974936419607861041793755542930286287098871510394661091846780839592290953853536571372997807697657464569729651718518301857979495046280018444198435962234642736892075369840282923945267377104440625478468507147243879631
```
So we have the modulus 'n', the public exponent 'e', a CRT exponent 'dp' ( Chinese Remainder Theorem exponent) which is used for fast decryption and encryption by some algorithms and is equal to d mod (p - 1). Finally the c number corresponds to the ciphertext we want to decipher.

Looking at the hints, we may have to, somehow, obtain a multiple of p so that we can factorize n. It seemed not an easy task, but looking at the dp value, I figured i could , at least, get a multiple of p - 1.
```
dp = d mod (p - 1)
dp = e^-1 mod (p - 1)
dp*e = 1 mod (p - 1)
dp*e - 1 = 0 mod (p - 1) = kp*(p-1) mod (p - 1)
```
Which means that dp*e - 1 is a multiple of p - 1. Now here comes the tricky part, how do we find a way to factorize n without having p? 

According to the paper ["A new attack on RSA and CRT-RSA"
](http://www.math.unicaen.fr/~nitaj/rsa21.pdf) by Abderrahmane Nitaj, I found out that there is a way to retrieve p having access to dp. In a simple way, the expression is:
```
p = gcd(edp + kp − 1, N)
```
The only unknown parameter here is kp. To find kp I wrote a script that would brute force the values of kp, by checking if p calculated is a prime number:
```python
for k in range(2, 100000000):
    print("kp =", k)
    p = gcd(dp*e - 1 + k, n)
    if fermat_test(p) == True:
        print("Found p prime!")
        print(p)
        break
```
Indeed the prime p was found! After a couple of iterations (34032 to be exact) the script returned: 
```python
p = 26055455403785096507756052717261284680661361587159609234428864200495745804937593432391788843742984937388092567353006541186681512162707243608988678338102797
``` 
After discovering p, the decryption is trivial RSA:
```python
q = n // p

phi = (q - 1) * (p - 1)

d = modinv(e, phi)

m = pow(c, d, n)

print(codecs.decode((hex(m).replace("0x", "")), "hex"))
```
Which returns the flag:
```
b'flag{wow_leaking_dp_breaks_rsa?_47413771836}'
```