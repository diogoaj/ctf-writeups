import md5 

seed = "808"
hash_final = "c4e4767be33fac9eaf99d070bf22218b"

hashc = seed
last_hash = ""

for i in range(50):
  hashc = md5.new(hashc).hexdigest()
  if hashc == hash_final:
        print(last_hash)
        break
  last_hash = hashc