
key = {'s': 'a',
	   'b': 'b',
	   'w': 'c',
	   'i': 'd',
	   'y': 'e',
	   'u': 'f',
	   'x': 'g',
	   'h': 'h',
	   'd': 'i',
	   'v': 'j',
	   'q': 'k',
	   'p': 'l',
	   'r': 'm',
	   'j': 'n',
	   'g': 'o',
	   'f': 'p',
	   'o': 'q',
	   'l': 'r',
	   'm': 's',
	   'a': 't',
	   'e': 'u',
	   'k': 'v',
	   'c': 'w',
	   't': 'x',
	   'n': 'y',
	   'z': 'z',
	   ' ': ' ',
	   '\n': ' '}


with open("crypto.txt", "r") as f:
	content = f.read()
	f.close()

script = "#!/usr/bin/perl -w\n"
for c in content:
	script += key[c]

print script