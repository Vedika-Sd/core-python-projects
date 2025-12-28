"""
Write a program that:
Prints numbers from 1 to 20
But:

Skip multiples of 3 
Stop completely if number is 17 
"""
for i in range (1,20):
    if i==17:
        break
    elif i%3==0:
        continue
    else:
        print(i, end=" ")
