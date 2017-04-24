### Digital Camouflage - 50 points

> We need to gain access to some routers. Let's try and see if we can find the password in the captured network data: data.pcap.

Hint:
> * It looks like someone logged in with their password earlier. Where would log in data be located in a network capture?
> * If you think you found the flag, but it doesn't work, consider that the data may be encrypted.

In this challenge, we get a pcap. Let's open it using Wireshark.

The hint says there was some kind of login, so we are most likely looking for a HTTP packet.
After filtering for HTTP, we can see there is a POST request.

In that request, we can see this:
```
userid=hardawayn&pswrd=UEFwZHNqUlRhZQ%3D%3D
```
So we have the userid, but the password seems encoded somehow.

The %3D is just '=' url encoded, therefore we have this:
```
UEFwZHNqUlRhZQ==
```
This is the format of base64 encoding. Decoding it (https://www.base64decode.org/), gives us the flag:

Flag
```
PApdsjRTae
```
