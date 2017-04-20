import math
import random
from Crypto.Cipher import AES
from hashlib import sha256
from Crypto import Random
from Crypto.Random import random
import string

p = 174807157365465092731323561678522236549173502913317875393564963123330281052524687450754910240009920154525635325209526987433833785499384204819179549544106498491589834195860008906875039418684191252537604123129659746721614402346449135195832955793815709136053198207712511838753919608894095907732099313139446299843  

g = 41899070570517490692126143234857256603477072005476801644745865627893958675820606802876173648371028044404957307185876963051595214534530501331532626624926034521316281025445575243636197258111995884364277423716373007329751928366973332463469104730271236078593527144954324116802080620822212777139186990364810367977 

A = 60599224471338675280892530751916349778515159413752423808328059701102187627870714718035966693602191072973114841123646111608872779841184094624255525186079109811898831481367089940015561846391171130215542875940992971840860585330764274682844976540740482087538338803018712681621346835893113300860496747212230173641

B = 41577936475113646062415839313533664222336390873095585592257233546410748309845182921273101711259044469844745154398797450729717767422505327649336923087518273833440859523881791932947163012973287757609314935398468435619627316484481259644562078527117416504710807415325721826304371028711933641605633408713301811494

# Calculated with bsgs
a = 33657892424673

iv_and_data =      "ffed2b87861bd6feab7b995c8bbc7c9af4a0e37e7ae8e861a3fc5fcd32aa10233f2195150f863349315a3fac7a56c54051c3714a38dc7c1014c6929c2027ecb9" #pw

command =          "452d11ce48746b405ede2b3d460e508aae237618503cb6e524ba0cbc3d133753b96a07466d96cb02a08add58ba313c14" #echo 

command_output =   "b46607855c1ce5189a95dd2131208fc2777083baa40f488aa6f3056b9426ae569e71aaa91768ee0abff5556ee1d7d6f4" #echo

command_2 =        "698647ce3244f5a450bf7a80b6c7096bdf8320ee41e71d414da9cf7b7a37fde4" # exit 

command_output_2 = "62216d83b780e7d86a02333e68e09a93104725fa60e829a37b456b04749e883e" # exit

BLOCK_SIZE = 16
R = Random.new()

pw = "ThisIsMySecurePasswordPleaseGiveMeAShell\n"

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

def read_encrypted(KEY,data):
    data = data.decode("hex")
    IV, data = data[:BLOCK_SIZE], data[BLOCK_SIZE:]
    aes = AES.new(KEY, AES.MODE_CBC, IV)
    m = unpad(aes.decrypt(data))
    return m


flag ="4f0746b0fc22da83a3f75c5f53fb741f60d14fd660ecf26ce6dce0706d1f3d4c7fc1b742f0f047b3753141a6b7ae9e90443199f84de3ddcddc2710d1d64022f7"
flag_decrypted ="ac72f7354114b5b0909ab78812eb58ca"
KEY = sha256(str(1)).digest()

print(read_encrypted(KEY))

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

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

#bsgs(g,A,p)