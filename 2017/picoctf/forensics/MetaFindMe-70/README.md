### Meta Find Me - 70 points

> Find the location of the flag in the image: image.jpg. Note: Latitude and longitude values are in degrees with no degree symbols,/direction letters, minutes, seconds, or periods. They should only be digits. The flag is not just a set of coordinates - if you think that, keep looking!

Hint:
> How can images store location data? Perhaps search for GPS info on photos.

For this problem, an image is given and we are asked to find the information about the image's location. If we open up the image properties, we can easily find tha latitude and the longitude values. 
```
Latitude: 77
Longitude: 172
```

Obviously, this is not the flag so we got to keep looking at the metadata of this image to see what we can find. To do this I used a program called [ExifTool](http://www.sno.phy.queensu.ca/~phil/exiftool/) to check all the metadata contained in the file. After executing it we got a bunch of information but the most important thing was a comment that had the "partial" flag:
```
...
Comment                         : "Your flag is flag_2_meta_4_me_<lat>_<lon>_736c. Now find the GPS coordinates of this image! (Degrees only please)"
Image Width                     : 500
Image Height                    : 500
Encoding Process                : Progressive DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:4:4 (1 1)
Image Size                      : 500x500
Megapixels                      : 0.250
Thumbnail Image                 : (Binary data 6989 bytes, use -b option to extract)
GPS Position                    : 77 deg 0' 0.00", 172 deg 0' 0.00"
```
Combining the comment with the latitude and longitude we get the full flag:
```
flag_2_meta_4_me_77_172_736c
```