### SoRandom - 75 points

> We found sorandom.py running at shell2017.picoctf.com:16768. It seems to be outputting the flag but randomizing all the characters first. Is there anyway to get back the original flag?

Hint:
> 	How random can computers be?


For this crypto challenge, we are given a Python script running on a server:
```python
#!/usr/bin/python -u
import random,string

flag = "FLAG:"+open("flag", "r").read()[:-1]
encflag = ""
random.seed("random")
for c in flag:
  if c.islower():
    #rotate number around alphabet a random amount
    encflag += chr((ord(c)-ord('a')+random.randrange(0,26))%26 + ord('a'))
  elif c.isupper():
    encflag += chr((ord(c)-ord('A')+random.randrange(0,26))%26 + ord('A'))
  elif c.isdigit():
    encflag += chr((ord(c)-ord('0')+random.randrange(0,10))%10 + ord('0'))
  else:
    encflag += c
print "Unguessably Randomized Flag: "+encflag
```
When we use ```nc``` and connect to the server, we receive this output:
```
Unguessably Randomized Flag: BNZQ:449xg472190mwx6869b8pt10rwo92624 
```

Now, looking at the code, we can see that the server is using some kind of cipher that, depending if the letter is upper case, lower case or a number, it rotates each letter in the alphabet accordingly. 

Another thing to note here is that a random seed is used to shuffle each letter in the plaintext, but, is it really random? The line ```random.seed("random")```sets the seed as the word "random" but that is not really random since it is initialized always the same way. With this in mind, the cipher is always deterministic and, if we run the script again we will get the same output.

Since I didn't want to think in a way to decrypt the ciphertext, I wrote a script in Python, using the cipher above, to brute force each letter. The idea is: 
* We cycle through all the letters in the ciphertext and check if the letter is upper case, lower case or a number. 
* Iterate through one of the possible groups (upper, lower or digit) and call the function above. If the cipher of this character coincides with the original ciphertext char, we correctly guessed a letter of the flag.
* Repeat until we find all the characters of the flag.

The script I wrote, it could be improved but it worked so:
```python
import random,string

lower = string.ascii_lowercase
upper = string.ascii_uppercase
digits = string.digits

ciphered = "BNZQ:449xg472190mwx6869b8pt10rwo92624"
flag = ""
encflag = ""

def cipher(str):
        encflag = ""
        random.seed("random")
        for c in flag:
          if c.islower():
            #rotate number around alphabet a random amount
            encflag += chr((ord(c)-ord('a')+random.randrange(0,26))%26 + ord('a'))
          elif c.isupper():
            encflag += chr((ord(c)-ord('A')+random.randrange(0,26))%26 + ord('A'))
          elif c.isdigit():
            encflag += chr((ord(c)-ord('0')+random.randrange(0,10))%10 + ord('0'))
          else:
            encflag += c
        return encflag

for char in ciphered:
        encflag += char
        if char in upper:
                for u in upper:
                        flag += u
                        if cipher(flag) == encflag:
                                break
                        else:
                                flag = flag[:-1]
        elif char in lower:
                for l in lower:
                        flag += l
                        if cipher(flag) == encflag:
                                break
                        else:
                                flag = flag[:-1]
        elif char in digits:
                for d in digits:
                        flag += d
                        if cipher(flag) == encflag:
                                break
                        else:
                                flag = flag[:-1]
        else:
                flag += char


print(flag)
```
Running the script we get the flag:
```
FLAG:107bd559693aef6692e1ed55ebe29514
```