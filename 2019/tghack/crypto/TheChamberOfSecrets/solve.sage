## ElGamal Elliptic Curve decryption

a = -3
b = 313205882961673
q = 1125899906842597

E = EllipticCurve(Zmod(q), [a, b])

g = E(1115545019992514, 78178829836422)
h = E(829999038570486, 549144410878897)
c1 = E(700253548714057, 421820716153583)
c2 = E(470712751668926, 131989609316847)

x = g.discrete_log(h)

print "[+] x:", x

C_ = c1*x
P = c2 - C_

print "[+] key:", P[0]