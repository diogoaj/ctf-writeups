from Crypto.Cipher import Blowfish
from Crypto.Hash import SHA256
import base64

b = "sTokhflo9WHPQB8JHEm0OVG2SwUA/sHaP0yFv9T2kmoZjC5g46eeRM8M8CGRj8bV/NxY4VJ8Ls0="

key =  SHA256.new()

# Insert key here
key.update(b"934013602642177")

def decrypt(key, message):
	enc = base64.b64decode(message)
	iv = enc[:Blowfish.block_size]
	cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
	return cipher.decrypt(enc[Blowfish.block_size:])

print(decrypt(key.digest(), b))