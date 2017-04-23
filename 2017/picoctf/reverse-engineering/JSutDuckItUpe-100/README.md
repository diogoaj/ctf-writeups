### JSut Duck It Up - 100 points

> What in the world could this be?!?! file

Hint:
> Maybe start searching for uses of these chunks of characers? Is there anything on the Internet with them?

In this problem we get a file full with these characters:
```
[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]][([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]]+[])[!+[]+!+[]+!+[]]+(!![]+[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+
...
```
This looks like some esoteric language. But which one?
After a little bit of googling we find this on Wikipedia  (https://en.wikipedia.org/wiki/Esoteric_programming_language):
```
JSFuck
JSFuck is an esoteric and educational programming language whose alphabet and syntax are subsets of JavaScript's. It uses only six different characters to write and execute code (()+[]!). Since it is a subset of JavaScript, it can run on a JavaScript engine. Despite being an esoteric language, JSFuck became famous by allowing a cross-site scripting attack on eBay.
```
So that's what the name of the problem means!
Now that we know the language, we "jsut" need to run it.

Luckily, there's a website that allows running the code easily (http://www.jsfuck.com/).
Let's write the code in the box and run it. That gives out the flag.

Flag:
```
aw_yiss_ducking_breadcrumbs_b703db4e
```
