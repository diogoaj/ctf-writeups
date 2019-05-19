### Twenty-five - 100 points 56 solves)

> With "ppencode", you can write Perl code using only Perl reserved words.

These three files are given: `crypto.txt`, `reserved.txt` and `twenty-five.pl`. 

The `crypto.txt` file contains an encrypted file which reminded me of substitution cipher. After digging into what "ppencode" meant, I discovered that "ppencode" is a way of writing a string with a script containing only Perl reserved words. A demo for that can be found [here](http://www.namazu.org/~takesako/ppencode/demo.html).

#### Solution

So the solution for the problem is basically to discover the key used in the substitution cipher and then, run the resulting script to retrieve the flag.

In order to get the key, I used this [site](https://www.quipqiup.com/) and tried to guess words based on frequency analysis. And little by little I discovered the mapping between the plaintext and the ciphertext. I then wrote a script to decrypt the words:

```python
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
```

Finally, the resulting Perl script outputs the flag:

```bash
$ python decrypt.py > script.pl
$ perl script.pl
```

And the flag is:

```
HarekazeCTF{en.wikipedia.org/wiki/Frequency_analysis}
```
