### SSS Part 1 - 75 points (91 solves)

>  3 math teachers agreed to a common secret password to access the exam answers. Luckily, one of them lost a note that seems related. They also talk all the time about some guy named Lagrange.
>  
> NOTE: the coordinates are:
> 4612c90f5d8cd5d616193257336d92af1f66df92443b4ee69f5c885f0173ad80113844e393d194e3
> 8c25921e46b03e48b7cbe94c3267f41adf618abd16422f660b59df6fae81e8aff2242852be33db49
> d2385b2d2fd3a6bb597ea041316255869f5c35e7e8490fe5775736805b9023dfd3100bc1e89621af


From the problem description and the problem title SSS, we know that we are dealing with [Shamir Secret Sharing](https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing) algorithm that allows one to share a secret by splitting it into multiple shares. Each share is given to a unique person and the secret, can only be constructed if every person gives his/her share. 

Since we have the three shares (three coordinates of the polynomial used to split the secret) we can easily reconstruct the secret. To do this, I used a [library](https://github.com/blockstack/secret-sharing) to do that for me:

```python
>>> from secretsharing import SecretSharer
>>> SecretSharer.recover_secret(['1-4612c90f5d8cd5d616193257336d92af1f66df92443b4ee69f5c885f0173ad80113844e393d194e3', '2-8c25921e46b03e48b7cbe94c3267f41adf618abd16422f660b59df6fae81e8aff2242852be33db49', '3-d2385b2d2fd3a6bb597ea041316255869f5c35e7e8490fe5775736805b9023dfd3100bc1e89621af'])
'74696d6374667b62347331435f6c346772346e67335f314e54657250304c6174696f4e7d'
>>> '74696d6374667b62347331435f6c346772346e67335f314e54657250304c6174696f4e7d'.decode("hex")
'timctf{b4s1C_l4gr4ng3_1NTerP0LatioN}'
```

And so the flag is:

```
timctf{b4s1C_l4gr4ng3_1NTerP0LatioN}
```
