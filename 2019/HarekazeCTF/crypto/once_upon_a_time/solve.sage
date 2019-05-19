import binascii
enc = "ea5929e97ef77806bb43ec303f304673de19f7e68eddc347f3373ee4c0b662bc37764f74cbb8bb9219e7b5dbc59ca4a42018"

c = binascii.unhexlify(enc)

K = [[1,3,2,9,4], [0,2,7,8,4], [3,4,1,9,4], [6,5,3,-1,4], [1,4,5,3,5]]

mattrix_lines = [c[i:i+5] for i in range(0, len(c), 5)]

W1 = mattrix_lines[0:5]
W2 = mattrix_lines[5:10]

W_1 = []
W_2 = []

for line in W1:
	t = []
	for j in range(len(line)):
		t.append(ord(line[j]))
	W_1.append(t)

for line in W2:
	t = []
	for j in range(len(line)):
		t.append(ord(line[j]))
	W_2.append(t)

W1 = matrix(GF(251), W_1)
W2 = matrix(GF(251), W_2)
K = matrix(GF(251), K)

first_half = K.solve_left(W1)
second_half = K.solve_left(W2)

flag1 = ""
flag2 = ""
for i in range(5):
	for j in range(5):
		flag1 += chr(first_half[i][j])
		flag2 += chr(second_half[i][j])

print "HarekazeCTF{" + (flag1+flag2).replace("%", "") + "}"