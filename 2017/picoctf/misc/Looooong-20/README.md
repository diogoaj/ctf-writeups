### looooong - 20 points

> I heard you have some "delusions of grandeur" about your typing speed. How fast can you go at shell2017.picoctf.com:59858?

Hint:
> * Use the nc command to connect!
> * I hear python is a good means (among many) to generate the needed input.
> * It might help to have multiple windows open

Let's connect and see that the program does:
```
To prove your skills, you must pass this test.                                                     
Please give me the 'e' character '658' times, followed by a single '3'.                            
To make things interesting, you have 30 seconds.                                                   
Input: 
```
The program changes everytime so we need to do what they ask in 30 seconds.
Let's run what they ask in python and copy+paste it into the program.
```
$python -c "print('e' * 658 + '3')"

Or run in python:
print('e' * 658 + '3')
```
After copying the result into the program, we get:
```
You got it! You're super quick!                                                                    
Flag: with_some_recognition_and_training_delusions_become_glimpses_ee260d1c785fd08f5d78753feae3c553
```

Flag
```
with_some_recognition_and_training_delusions_become_glimpses_ee260d1c785fd08f5d78753feae3c553
```
