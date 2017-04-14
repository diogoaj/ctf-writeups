### ECC2 - 200 points

> More elliptic curve cryptography fun for everyone!
(Yes, the flag will just be the number n.)

Hint:
> Using SageMath (or something similar which supports working with elliptic curves) will be very helpful.

Ok this problem was actually very hard for me since I haven't solved anything like this and didn't know nothing about elliptic curves. For this one, I used [SageMath](http://www.sagemath.org/index.html) to work with the curves, as hinted. First off, we have a file named "handout.txt" which contains the following content:
```
Elliptic Curve: y^2 = x^3 + A*x + B mod M
M = 93556643250795678718734474880013829509320385402690660619699653921022012489089
A = 66001598144012865876674115570268990806314506711104521036747533612798434904785
B = *You can figure this out with the point below :)*

P = (56027910981442853390816693056740903416379421186644480759538594137486160388926, 65533262933617146434438829354623658858649726233622196512439589744498050226926)
n = *SECRET*
n*P = (61124499720410964164289905006830679547191538609778446060514645905829507254103, 2595146854028317060979753545310334521407008629091560515441729386088057610440)

n < 400000000000000000000000000000

Find n.
```
I'm not going to explain what elliptic curves are and what the relation of them with cryptography, but, you can start by checking the wikipedia page on [ECC](https://en.wikipedia.org/wiki/Elliptic_curve_cryptography).

The first thing I did when I looked at the problem was to compute the B value of the equation we are given above. To do that, we simply plug in the values of the point P in the elliptic curve equation:
```
B = y^2 - x^3 - A*x mod M
```
Which is equal to: ```25255205054024371783896605039267101837972419055969636393425590261926131199030```

Then what I did was research what type of problem we have in hands here. I found out that this is a [Discrete Log](https://en.wikipedia.org/wiki/Discrete_logarithm) problem because we want to find the integer n that satisfies: ``` Q = nP ```. We have both points Q and P so now we just need to find n. That are a lot of algorithms to do this but, for this specific problem, none of them will actually work since the values we have are really large. 

Another thing I found out in my research is that there are possible attacks on elliptic curves but it involves that certain conditions are met. For example, if the prime M from the elliptic curve equation is equal to the [order of the curve](https://en.wikipedia.org/wiki/Counting_points_on_elliptic_curves), the curve is said to be anomalous and, the discrete log is very easy to compute. So what I did was check if ```E.order() == M``` which, unfortunately, returned ```False```.

After a couple of days banging my head on this problem, I came across a [paper](https://link.springer.com/chapter/10.1007/BFb0052240) that talked about **PohIig-Hellman Decomposition and Pollard's Methods** and how that can be used to calculate the discrete logarithm, and that's what I did.

So the idea is to calculate the discrete logarithm by factoring the order of the point P and, computing the "partial" discrete logs modulo each factor of the order of the point and then, join them with the Chinese Remainder Theorem to get the solution to the original problem. First we calculate the order of the point P and factorize this value:
```
P.order() = 93556643250795678718734474880013829509196181230338248789325711173791286325820
```
Now let's factorize the order. I used [factordb](http://www.factordb.com/) for this: 
```
Factors:
2^2 · 3 · 5 · 7 · 137 · 593 · 24337 · 25589 · 3637793 · 5733569 · 106831998530025000830453 · 1975901744727669147699767
```
Now the next step, is to calculate each partial logarithm. For example, the first logarithm is modulo 2^2 since it is the first factor. To do this, we multiply the co-factors (i.e all the other factors excluding 2^2) with the point P and Q. Then, calculate the logarithm. I used SageMath discrete_log_rho for this:
```python
co_factors = 3 * 5 * 7 * 137 * 593 * 24337 * 25589 * 3637793 * 5733569 * 106831998530025000830453 * 1975901744727669147699767

P = co_factors*P
Q = co_factors*Q

discrete_log_rho(Q,P,ord = 2, operation='+') = 2
```
Applying this logic to all factors we get the following partial solutions:
```
Partial solutions for each factor:
2 -> 2
3 -> 1
5 -> 4
7 -> 1
137 -> 129
593 -> 224
24337 -> 5729
25589 -> 13993
3637793 -> 1730599
5733569 -> 4590572
106831998530025000830453 -> ??
1975901744727669147699767 -> ??
```
The last two factors were too long to be calculated with the method I used and I couldn't get a solution for them. Luckily, the problem gives us a bound for the value of n:  ```n < 400000000000000000000000000000```.

Hmm, maybe with the solutions I have, I can get the solution within this bound. 
The final step is to join the partial solutions with CRT (using sage again) :
```python
CRT_list([2,1,4,1,129,224,5729,13993,1730599,4590572], [4,3,5,7,137,593,24337,25589,3637793,5733569])
```
Which returned:
```
152977126447386808276536247114
```
Ok let's try and check if this is the solution to the equation initially given:
```python
P*152977126447386808276536247114 == Q
True
```
Nice! So we indeed got the final solution without the last two partial solutions, neat!

The flag of this problem will be just the value of n so:
```
152977126447386808276536247114
```
