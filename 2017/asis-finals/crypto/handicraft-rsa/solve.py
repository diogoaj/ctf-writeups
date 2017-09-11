from Crypto.Util.number import *
from Crypto.PublicKey import RSA
import time

with open("output.txt", "r") as f:
    output = f.read()

key_content = output.split("----------------------------------------------------------------------------")[0][:-1]
key = RSA.importKey(key_content)

enc = output.split("----------------------------------------------------------------------------")[1].replace("\n", "")

n = key.n

p = 139457081371053313087662621808811891689477698775602541222732432884929677435971504758581219546068100871560676389156360422970589688848020499752936702307974617390996217688749392344211044595211963580524376876607487048719085184308509979502505202804812382023512342185380439620200563119485952705668730322944000000001

q = n/p

e = 65537
d = inverse(e, (p-1)*(q-1))


fullKey = RSA.construct((long(n), long(e), long(d), long(p), long(q)))

msg = enc.decode("base64")

for i in xrange(10000):
	dec = fullKey.decrypt(msg)
	msg = dec
	try:
		print msg.decode()
		break
	except:
		pass
