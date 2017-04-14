### Missing Identity - 100 points

> Turns out, some of the files back from Master Challenge 1 were corrupted. Restore this one file and find the flag. 

Hints:
> What file is this?
> What do you expect to find in the file structure?
> All characters in the file are lower case or numberical. There will not be any zeros.

For this challenge we are given a file named "file". The first thing to do is to check what type of file we have with the file command:
```
$ file file
file: data
```
Hm, not very helpful. Next thing we tried was to unzip the file:
```
$ unzip file
Archive:  file
file #1:  bad zipfile offset (local header sig):  0
  inflating: nottheflag1.png
  inflating: nottheflag2.png
  inflating: nottheflag3.png
  inflating: nottheflag4.png
  inflating: nottheflag5.png
```

Now we're in the right track. After unziping the file we got 5 .png images with the name "nottheflag", but we got an error extracting the first file that said ```bad zipfile offset (local header sig): 0 ```. To solve this error, I edited the header of the file in [Hexedit](https://hexed.it/) and changed it to the correct [zip header](https://en.wikipedia.org/wiki/List_of_file_signatures):
```
The header of the file was: 
5858 5858
I changed it to:
504B 0304
```
After the fix, we just run the command ```unzip``` with the corrected file and we can extract all the images with success, giving us the flag in an image:
```
zippidydooda49559523
```