### HashChain - 90 points

> We found a service hiding a flag! It seems to be using some kind of MD5 Hash Chain authentication to identify who is allowed to see the flag. Maybe there is a flaw you can exploit? hcexample.py has some example code on how to calculate iterations of the MD5 hash chain. Connect to it at shell2017.picoctf.com:50102!

Hint:
> Connect from the shell with nc. Read up on how Hash Chains work and try to identify what could make this cryptosystem weak.


This problem involves knowledge of [Hash functions](https://en.wikipedia.org/wiki/Hash_function) and [Hash Chains](https://en.wikipedia.org/wiki/Hash_chain). A hash function is, in simple terms, a function that takes a string as an input and returns a hash value, that is, a value with a fixed size (depending on the algorithm) containing hexadecimal characters and, given the same input, the output will always be the same. One thing important about hashes is that if we have access to an hash value, we can't determine what is the original input given to the algorithm. A hash chain, on the other hand, is the application of a hash function multiple times.

First thing to do here is look at the code given:

```python
import md5 #Must be run in python 2.7.x

#code used to calculate successive hashes in a hashchain. 
seed = "seedhash"

#this will find the 5th hash in the hashchain. This would be the correct response if prompted with the 6th hash in the hashchain
hashc = seed
for _ in xrange(5):
  hashc = md5.new(hashc).hexdigest()
 
print hashc
```

Basically what this code does is calculate the Hash of the ```seed``` five times. Let's check what the server is up to. When we connect to the server this is what we get:
```
*******************************************                                            
***            FlagKeeper 1.1           ***                                            
*  now with HASHCHAIN AUTHENTICATION! XD  *                                            
*******************************************                                            
                                                                                       
Would you like to register(r) or get flag(f)?                                          
                                                                                       
r/f?
```
So we have two options, register and get flag. The first option registers our user and presents us with the following message:
```
Hello new user! Your ID is now 3263 and your assigned hashchain seed is f8037f94e53f17a2cc301033ca86d278                                                                      
Please validate your new ID by sending the hash before this one in your hashchain (it will hash to the one I give you):                                                       
d40d3b66694a0b5bb852e6e24d1fa60b
```
It is saying that our user id is 3263 and our initial hashseed is ```f8037f94e53f17a2cc301033ca86d278```, and then is telling us to validate our user by sending the hash before this one: ```d40d3b66694a0b5bb852e6e24d1fa60b```. Interesting, so all we have to do to validate a user is to calculate multiple iterations of the hash function given in the initial code and stop when we reach the final hash. 

To do this I wrote a quick script in Python:
```python
import md5 

seed = "f8037f94e53f17a2cc301033ca86d278"
hash_final = "d40d3b66694a0b5bb852e6e24d1fa60b"

hashc = seed
last_hash = ""

for i in range(50):
  hashc = md5.new(hashc).hexdigest()
  if hashc == hash_final:
        print(last_hash)
        break
  last_hash = hashc
```
Validating the user gives us the message: ```Yep! That's it! You're validated```

Ok, now that we understand how the system works let's check the second option, the get flag option:
```
This flag only for user 808
Please authenticate as user 808
c4e4767be33fac9eaf99d070bf22218b
Next token?
```
It is simply asking the token before the hash of the user 808. Here I got a little bit confused because we didn't have the initial seed for the given user. Luckily I decided to check if the user's id was the initial hash. If this was true, we would simply execute the above script and calculate the hash we wanted, just like we did with the register option!

After running the script with my assumption, the flag is returned! The message displayed:
```
Hello user 808! Here's the flag: 96630f954dd403c7882666b5443e4678
```
And we get the flag:
```
96630f954dd403c7882666b5443e4678
```