### Puzzlingly Accountable - 100 points

> We need to find a password. It's likely that the updated passwords were sent over the network. Let's see if that's true: data.pcap. Update 16:26 EST 1 Apr If you feel that you are close, make a private piazza post with what you have, and an admin will help out. The ones and sevens unfortunately look like each other.

Hint:
> How does an image end up on your computer? What type of packets are involved?

We get a pcap once again. Let's open it!
We can observe a few HTTP packets with GET requests. Let's filter them.

If we look carefully, we can find two GET requests from a secret folder.
If we follow TCP stream of each one of these packets (libAFo31.png and SoV1xW80.png), we get the PNG content. Let's save their raw data into files.

Since we saved it from wireshark, the data still has useless information:
```
GET /secret/libAFo31.png HTTP/1.1
User-Agent: Wget/1.16 (linux-gnu)
Accept: */*
Host: 10.0.0.1:8080
Connection: Keep-Alive

HTTP/1.0 200 OK
Server: BaseHTTP/0.3 Python/2.7.9
Date: Thu, 07 Apr 2016 21:44:40 GMT
Content-type: image/png
```
If we open each of these files in an hex editor (https://hexed.it/), we can delete that part, until we get only the PNG part, which starts with:
```
89 50 4E 47 0D 0A 1A 0A
```
Correcting the data gives us two pngs with the following letters:
```
libAFo31 - e7fc89c05d1b57c
SoV1xW80 - c50c8e859f6e06a63
```

Flag:
```
c50c8e859f6e06a63e7fc89c05d1b57c
```