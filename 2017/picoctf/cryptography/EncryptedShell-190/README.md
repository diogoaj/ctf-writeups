### Encrypted Shell - 190 points
> This service gives a shell, but it's password protected! We were able intercept this encrypted traffic which may contain a successful password authentication. Can you get shell access and read the contents of flag.txt?
The service is running at shell2017.picoctf.com:40209.

Hints:
> 	- Are any of the parameters used in the key exchange weaker than they should be?

As the title says, there is a server running a service that gives you a shell once you know the password. Let's take a good look at the code first:
```python
#!/usr/bin/python2 -u
from hashlib import sha256
from Crypto import Random
from Crypto.Random import random
from Crypto.Cipher import AES
from subprocess import check_output, STDOUT, CalledProcessError

BLOCK_SIZE = 16
R = Random.new()

with open("parameters.txt") as f:
    p = int(f.readline().strip())
    g = int(f.readline().strip())

password = open("password.txt").read()

def pad(m):
    o = BLOCK_SIZE - len(m) % BLOCK_SIZE
    return m + o * chr(o)

def unpad(p):
    return p[0:-ord(p[-1])]

def send_encrypted(KEY, m):
    IV = R.read(BLOCK_SIZE)
    aes = AES.new(KEY, AES.MODE_CBC, IV)
    c = aes.encrypt(pad(m))
    print (IV + c).encode('hex')

def read_encrypted(KEY):
    data = raw_input("").decode('hex')
    IV, data = data[:BLOCK_SIZE], data[BLOCK_SIZE:]
    aes = AES.new(KEY, AES.MODE_CBC, IV)
    m = unpad(aes.decrypt(data))
    return m

def serve_commands(KEY):
    while True:
        cmd = read_encrypted(KEY)
        try:
            output = check_output(cmd, shell=True, stderr=STDOUT)
        except CalledProcessError as e:
            output = str(e) + "\n"
        send_encrypted(KEY, output)

print """Welcome to the
______ _   _   _____ _          _ _ 
|  _  \ | | | /  ___| |        | | |
| | | | |_| | \ `--.| |__   ___| | |
| | | |  _  |  `--. \ '_ \ / _ \ | |
| |/ /| | | | /\__/ / | | |  __/ | |
|___/ \_| |_/ \____/|_| |_|\___|_|_|
"""

print "Parameters:"
print "p = {}".format(p)
print "g = {}".format(g)

a = random.randint(1, 2**46)
A = pow(g, a, p)
print "A = {}".format(A)

B = int(raw_input("Please supply B: "))
K = pow(B, a, p)

KEY = sha256(str(K)).digest()

pw = read_encrypted(KEY)
if pw == password:
    serve_commands(KEY)
else:
    send_encrypted("Invalid password!\n")

```

So, the services prints two parameters first: ```p``` and ```g``` then, generates a random number ```a``` and calculates a value ```A``` with the ```pow``` function and prints it's value. By just looking at this lines of code, we can deduce that a key exchange is happening, more specifically, a [Diffie-Hellman key exchange](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange). 

In a Diffie-Hellman key exchange, two parties agree on two initial values, ```p```, which is a prime number and ```g```. After that, each of the parties choose two private values ```a``` and ```b``` and calculate ```A``` and ```B``` as follows: ```A = g^a mod p``` and ```B = g^b mod p```.  Those values are then exchanged through the channel and the shared key can be computed as: ```K = A^b mod p``` and ```K = B^a mod p``` which is equal to ```g^ab mod p```. This exchange is relatively safe if the values used are strong. If an attacker is in the middle of the communication, he cannot compute the shared key ```K``` because he never saw the private values being exchanged, he only saw the public values ```A``` and ```B```. To calculate the private values, one would compute the discrete logarithm to get ```a``` or ```b```, and that problem is very hard to solve.

After the initial key exchange, the service asks for the ciphered password and, if the password is correct, a shell is executed for us and we can send all the commands we want:
```python
pw = read_encrypted(KEY)
if pw == password:
    serve_commands(KEY)
else:
    send_encrypted("Invalid password!\n")
```
The only thing left for us to do here is to check the traffic.pcap given. We open this file with [Wireshark](https://www.wireshark.org/) and click on any TCP packet to follow the TCP stream. The result is interesting:
```
Welcome to the
______ _   _   _____ _          _ _ 
|  _  \ | | | /  ___| |        | | |
| | | | |_| | \ `--.| |__   ___| | |
| | | |  _  |  `--. \ '_ \ / _ \ | |
| |/ /| | | | /\__/ / | | |  __/ | |
|___/ \_| |_/ \____/|_| |_|\___|_|_|

Parameters:
p = 174807157365465092731323561678522236549173502913317875393564963123330281052524687450754910240009920154525635325209526987433833785499384204819179549544106498491589834195860008906875039418684191252537604123129659746721614402346449135195832955793815709136053198207712511838753919608894095907732099313139446299843
g = 41899070570517490692126143234857256603477072005476801644745865627893958675820606802876173648371028044404957307185876963051595214534530501331532626624926034521316281025445575243636197258111995884364277423716373007329751928366973332463469104730271236078593527144954324116802080620822212777139186990364810367977
A = 60599224471338675280892530751916349778515159413752423808328059701102187627870714718035966693602191072973114841123646111608872779841184094624255525186079109811898831481367089940015561846391171130215542875940992971840860585330764274682844976540740482087538338803018712681621346835893113300860496747212230173641
Please supply B: 41577936475113646062415839313533664222336390873095585592257233546410748309845182921273101711259044469844745154398797450729717767422505327649336923087518273833440859523881791932947163012973287757609314935398468435619627316484481259644562078527117416504710807415325721826304371028711933641605633408713301811494
ffed2b87861bd6feab7b995c8bbc7c9af4a0e37e7ae8e861a3fc5fcd32aa10233f2195150f863349315a3fac7a56c54051c3714a38dc7c1014c6929c2027ecb9
452d11ce48746b405ede2b3d460e508aae237618503cb6e524ba0cbc3d133753b96a07466d96cb02a08add58ba313c14
b46607855c1ce5189a95dd2131208fc2777083baa40f488aa6f3056b9426ae569e71aaa91768ee0abff5556ee1d7d6f4
698647ce3244f5a450bf7a80b6c7096bdf8320ee41e71d414da9cf7b7a37fde4
62216d83b780e7d86a02333e68e09a93104725fa60e829a37b456b04749e883e
```
The stream shown above reveals an example of a successful interaction between the server and the client. The really interesting value is the one after B:
```
ffed2b87861bd6feab7b995c8bbc7c9af4a0e37e7ae8e861a3fc5fcd32aa10233f2195150f863349315a3fac7a56c54051c3714a38dc7c1014c6929c2027ecb9
```
This corresponds to the encrypted password that gives us access to the shell. The rest hexadecimal values are commands and the respective outputs. In this specific problem, the private value used in the key exchange is a weak random number that ranges from 1 to 2^46 which means, that we can use a relatively fast algorithm to solve the discrete logarithm. Once we have the shared key, we can decrypt all the traffic and discover the password!

To solve this problem, I used the [Baby-Step Giant-Step](https://en.wikipedia.org/wiki/Baby-step_giant-step) algorithm which has complexity ```O(sqrt(p))```. Seems really slow right? We can optimize the algorithm since we know the bounds on the private exponent. With this information, the complexity is greatly reduced to: ```O(sqrt(n))``` with ```n``` being the maximum bound on the exponent. The algorithm is as follows:
```python
# g^a mod p = A
def bsgs(g,A,p,bound=None):
    baby_steps = {}

    if bound == None:
        m = int(math.ceil(math.sqrt(p)))
    else:
        m = bound

    print "[-] Computing baby steps..."
    for i in range(m):
        print i
        baby_steps[pow(g,i,p)] = i

    print "[-] Computing giant steps..."
    inv = pow(modinv(g,p), m, p)
    Y = A
    for i in range(m):
        if Y in baby_steps:
            print "Exponent found:"
            print (str(g) + "^" + str(i*m + baby_steps[Y]) + " = " + str(A) + " mod " + str(p))
            return
        else:
            Y = (Y * inv) % p
```
Even with the optimization, the calculation will take a lot of time (approximately 90 minutes for me, cosuming 1.8Gb of memory), because of the pre-computation phase in the first cycle. In the end, the private exponent ```a``` is returned:
```
a = 33657892424673
```

Now comes the easy part, since we have the private exponent, we now are in control of the shared key used in this session and we can retrieve the password of the server:
```python
pw = "ffed2b87861bd6feab7b995c8bbc7c9af4a0e37e7ae8e861a3fc5fcd32aa10233f2195150f863349315a3fac7a56c54051c3714a38dc7c1014c6929c2027ecb9"

def unpad(p):
    return p[0:-ord(p[-1])]

def read_encrypted(KEY, data):
    data = data.decode("hex")
    IV, data = data[:BLOCK_SIZE], data[BLOCK_SIZE:]
    aes = AES.new(KEY, AES.MODE_CBC, IV)
    m = unpad(aes.decrypt(data))
    return m

# Shared key
K = pow(B,a,p)
KEY = sha256(str(K)).digest()

print(read_encrypted(KEY, pw))
```
Which returns:
```
ThisIsMySecurePasswordPleaseGiveMeAShell

```
Nice, so this is the password. Also, I decrypted the rest of the traffic but the result was not useful (the commands used were an ```echo``` and ```exit```). 

We can now access the server and use the shell, the initial ```g```, ```p```, and ```A``` values are given and we have to supply B. Here I just gave 1 as input since the shared key will be ```pow(B,a,p) = 1``` so it is more straightforward to calculate. After supplying B we input the password. For this we use again the encryption methods given:
```python
password = "ThisIsMySecurePasswordPleaseGiveMeAShell\n"

def pad(m):
    o = BLOCK_SIZE - len(m) % BLOCK_SIZE
    return m + o * chr(o)


def send_encrypted(KEY, m):
    IV = R.read(BLOCK_SIZE)
    aes = AES.new(KEY, AES.MODE_CBC, IV)
    c = aes.encrypt(pad(m))
    print (IV + c).encode('hex')


KEY = sha256(str(1)).digest()
password_enc = send_encrypted(KEY, password)

print(password)
```
After inserting the value returned by the print funcion in the shell, the service expects us to supply another value (a command), so we cipher "cat flag.txt" and supply the command, which in turn outputs:
```
4f0746b0fc22da83a3f75c5f53fb741f60d14fd660ecf26ce6dce0706d1f3d4c7fc1b742f0f047b3753141a6b7ae9e90443199f84de3ddcddc2710d1d64022f7
```

All we have to do now is decipher this string and the flag is ours:
```
ac72f7354114b5b0909ab78812eb58ca
```




