### Zipper - 50 points

> Something doesn't seem quite right with this zip file. 
> 
> Can you fix it and get the flag?

For this problem we are given a zip file. First thing to do here is to try and unzip the file. It is obvious that this won't work but, at least, we can check what type of error we are going to receive:
```
$ unzip zipper_50d3dc76dcdfa047178f5a1c19a52118.zip
Archive:  zipper_50d3dc76dcdfa047178f5a1c19a52118.zip
warning:  filename too long--truncating.
:  bad extra field length (central)
```
Ok, we are given a warning, ```filename too long--truncating.``` and an error, ```bad extra field length (central)```. Something is wrong with this two fields in the zip structure. Next thing I did was to google the zip file structure and found [this](https://users.cs.jmu.edu/buchhofp/forensics/formats/pkzip.html) helpful website. 

After learning a bit about the structure, I opened the zip file with [hexed.it](https://hexed.it/) and started to check the file bytes and compared with the structure. The first wrong thing here is the file name size in the local file header. It has the hex value ```29 23```which is ```9001``` in decimal! After the extra field length value, we can find a couple of 0's before encountering a value that is not 0:

![image_1](http://i.imgur.com/AuQoFl2.png)

We can deduce that this is the file name. If we count, we have 8 bytes of data, which means, that the file name has 8 bytes. We can just change the file name length field now to ```08 00```. After this step, we can give the file a name, I chose to name it ```flag.txt``` and so, we insert the hex value for this string: ```66 6c 61 67 2e 74 78 74```

Still, we can't unzip the file just yet. In the central directory part of the zip, we have the same problem:

![image_2](http://i.imgur.com/tjeBUCG.png)

Highlighted in the aboce image is what we have to change. It is the same steps we did above with the local header. Change the file size to 8 bytes and change the file name to ```flag.txt```.

After the fix, we can finally unzip the file and retrieve the flag:
```
$ unzip z.zip && cat flag.txt
Archive:  z.zip
  inflating: flag.txt


Huzzah, you have captured the flag:
PCTF{f0rens1cs_yay}
```

Flag:
```
PCTF{f0rens1cs_yay}
```
