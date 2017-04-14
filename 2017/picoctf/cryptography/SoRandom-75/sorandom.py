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