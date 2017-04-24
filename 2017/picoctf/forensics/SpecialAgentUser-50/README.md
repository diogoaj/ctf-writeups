### Special Agent User - 50 points

> We can get into the Administrator's computer with a browser exploit. But first, we need to figure out what browser they're using. Perhaps this information is located in a network packet capture we took: data.pcap. Enter the browser and version as "BrowserName BrowserVersion". NOTE: We're just looking for up to 3 levels of subversions for the browser version (ie. Version 1.2.3 for Version 1.2.3.4) and ignore any 0th subversions (ie. 1.2 for 1.2.0)

Hint:
> Where can we find information on the browser in networking data? Maybe try reading up on user-agent strings.

In this challenge we get a pcap and they ask us to find what browser was used.

Once again, let's open it, filter for HTTP, and see what we can find in the User-Agent:

```
User-Agent: Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))
```
At first, it appears we are using Mozilla 5.0 but that isn't true.
```
MozillaProductSlice. Claims to be a Mozilla based user agent, which is only true for Gecko browsers like Firefox and Netscape. For all other user agents it means 'Mozilla-compatible'. In modern browsers, this is only used for historical reasons. It has no real meaning anymore
```
In fact, we are using Internet Explorer. In case we missed it from our user agent, we can easily see it by using the website they give us (http://www.useragentstring.com).

After analyzing our user agent, we get: http://imgur.com/a/33fUV

Therefore, our browser is MSIE 9.0.

Flag
```
MSIE 9.0
```
