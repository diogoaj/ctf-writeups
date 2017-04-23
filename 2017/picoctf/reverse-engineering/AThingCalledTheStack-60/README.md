### A Thing Called the Stack - 60 points

> A friend was stacking dinner plates, and handed you this, saying something about a "stack". Can you find the difference between the value of esp at the end of the code, and the location of the saved return address? Assume a 32 bit system. Submit the answer as a hexidecimal number, with no extraneous 0s. For example, the decimal number 2015 would be submitted as 0x7df, not 0x000007df

Hint:
> * Where is the return address saved on the stack?
> * Which commands actually affect the stack?

We are asked to determine the difference between the value of %esp at the end of the code and the location of the saved return address.
We are given this code:

```
foo:
    pushl %ebp
    mov %esp, %ebp
    pushl %edi
    pushl %esi
    pushl %ebx
    sub $0xb4, %esp
    movl $0x1, (%esp)
    movl $0x2, 0x4(%esp)
    movl $0x3, 0x8(%esp)
    movl $0x4, 0xc(%esp)
```
All we have in the stack, when foo is called is:
```
	ret addr	<= %esp
```
After that, the first 2 lines are saving %ebp, therefore we will have:
```
	ret addr
    saved ebp	<= %esp
```
Then, we have 3 more push instructions. Both the save ebp and each push displace the stack pointer 4 bytes.
Because of that, we are now with a difference of 0x10.
```
4 push instructions * 4 bytes = 16 = 0x10 hex
```
Now we have:
```
	ret addr
    saved ebp
    %edi
    %esi
    %ebx	<= %esp
```
Finally, we are subtracting 0xb4 to the stack pointer (moving it even more):
```
	ret addr
    saved ebp
    %edi
    %esi
    %ebx
    ... (0xb4)
    			<= %esp
```
Having as a difference:
```
0x10 + 0xb4 = 0xc4
```
The final 4 instructions aren't actually changing the stack pointer, but changing the values of what it is pointing to.

Therefore, the difference between the return address and %esp is:

Flag
```
0xc4
```
