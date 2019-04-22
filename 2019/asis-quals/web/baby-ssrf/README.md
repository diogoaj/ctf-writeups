### Baby SSRF - 70 points (73 solves)

> The goats thought they were safe behind the walls from the threat of the wolf!
> But they were not aware of the wolf's plan to bypass the wall!


We are given a really simple website with the text:

`Hi, I'm a baby ssrf :)`

Not a lot of information really. First thing I did was to try endpoints searching for something more relevant. 

```
$ python3 dirsearch.py -u 82.196.12.132:12999

 _|. _ _  _  _  _ _|_    v0.3.8
(_||| _) (/_(_|| (_| )

Extensions: php | Threads: 10 | Wordlist size: 6009

Target: 82.196.12.132:12999

Starting:
[21:20:24] 400 -   11B  - /%ff/
[21:20:52] 200 -    2KB - /source
[21:20:52] 200 -    2KB - /source/

Task Completed
```

I got a hit with the endpoint `/soruce`. Accessing the endpoint displays the source code of the site:

```javascript
const express = require("express");
const config = require("./configs");
const body_parser = require('body-parser');
const http = require('http')
const public_s = express();
const private_s = express();
const normalizeUrl = require('normalize-url');

public_s.use(body_parser.urlencoded({
    extended: true
}));

public_s.get('/', function (request, result) {
    result.setHeader('GET', 'source')
    result.send("Hi, I'm a baby ssrf :)")
    result.end()
})

public_s.get('/source', function(req, res) {
    res.sendFile(__filename)
  })

public_s.use(function (req, res, next) {
    var err = null;
    try {
        decodeURIComponent(req.path)
    } catch (e) {
        err = e;
    }
    if (err) {
        res.sendStatus(400).end()
    }
    next();
});

public_s.post('/open/', (request, result) => {
    document_name = request.body.document_name

    if (document_name === undefined) {
        result.end('bad')
    }
    console.log('http://localhost:9000/documents/' + document_name)
    if (document_name.indexOf('.') >= 0 ||
        document_name.indexOf("2e") >= 0 ||
        document_name.indexOf("┮") >= 0 ||
        document_name.indexOf("Ｅ") >= 0 ||
        document_name.indexOf("Ｎ") >= 0) {
        result.end('Please get your banana and leave!')
    } else {
        try {
            var go_url = normalizeUrl('http://localhost:9000/documents/' + document_name)
        } catch {
            var go_url = 'http://localhost:9000/documents/banana'
        }
        http.get(go_url, function (res) {
            res.setEncoding('utf8');

            if (res.statusCode == 200) {
                res.on('data', function (chunk) {
                    result.send(chunk)
                    result.end()
                });
            } else {
                result.end('Oops')
            }
        }).on('error', function (e) {
            console.log("Got error: " + e.message);
        });
    }
})

public_s.listen(8000)
private_s.listen(9000)

private_s.get('/documents/banana', function (request, result) {
    result.send("Here is your banana :D")
    result.end()
})

private_s.get('/flag', function (request, result) {
    result.send(config.flag)
    result.end()
})
```

The code is easy to understand. There is an internal service running behind the `/open` endpoint where the flag can be read. All we have to do is call the open service with the document that we want to read with the `document_name` argument. The only problem is the filter being done on our input:

```
if (document_name.indexOf('.') >= 0 ||
        document_name.indexOf("2e") >= 0 ||
        document_name.indexOf("┮") >= 0 ||
        document_name.indexOf("Ｅ") >= 0 ||
        document_name.indexOf("Ｎ") >= 0) {
        result.end('Please get your banana and leave!')
```

This prevents us from simply input `../flag` or bypass the filter with `%2e%2e/flag`. After some thinking, I figured I could URL encode the string `%2e` and bypass the filter. 

```
The input %2e%2e/flag becomes %25%32%45%25%32%45/flag
```

![burp_ssrf](https://github.com/diogoaj/ctf-writeups/blob/master/2019/asis-quals/web/baby-ssrf/resources/baby_ssrf.png)


Flag:

`
ASIS{68aaf2e4dd0e7ba28622aaed383bef4f}
`



