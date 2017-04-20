### Lazy Dev - 50 points

> I really need to login to this website, but the developer hasn't implemented login yet. Can you help?.

Hint:
> * Where does the password check actually occur?
> * Can you interact with the javascript directly?

We get this website (http://shell2017.picoctf.com:4370/), that has a submit button. Submitting doesn't seem to work, always returning:
```
Nah, that's not it
```
Let's open the console and see what we find.
Right in the html we have this:
```
<script type="text/javascript" src="/static/client.js"></script>
```
It seems to be a local script. Can we find it?
On Sources, there's the static folder with the script inside.

http://imgur.com/a/rEz3A

Looking at the code, there's a function (validate) always returning false.
```
function validate(pword){
  //TODO: Implement me
  return false;
}
```
But since, it's a local function, we can change it!
```
function validate(pword){
  return true;
}
```
Now we can submit again and it will give us the flag.

Flag:
```
client_side_is_the_dark_side0c97381c155aae62b9ce3c59845d6941
```