### Raw2Hex - 20 points

>This program just prints a flag in raw form. All we need to do is convert the output to hex and we have it! CLI yourself to /problems/608e5f8b55c005ae6bc4ff13393c9c23 and turn that Raw2Hex!

Hint:
>Google is always very helpful in these circumstances. In this case, you should be looking for an easy solution.

Lets head to /problems/608e5f8b55c005ae6bc4ff13393c9c23
```
$ls
flag  raw2hex
$cat flag
cat: flag: Permission denied
$./raw2hex
The flag is:=��C]Y��+��=|D�2
```

So we need to convert this string to hex
```
$./raw2hex > ~/level1/raw2hexDump
```
After this we edit raw2hexDump file in order for the file to contain only
```
=��C]Y��+��=|D�2
```

Last step is to convert this string to hex.

```
$ STR=$(cat ~/level1/raw2hexDump)
$ HEXVAL=$(xxd -pu <<< "$STR")
$ echo "$HEXVAL"
3dacd3435d59a4862b9ff83d7c44cd320a
```

The flag is : 3dacd3435d59a4862b9ff83d7c44cd320a
