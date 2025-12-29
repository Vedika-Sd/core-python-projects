"""
Task:
write separate function to check if number is even, max, square of a number
call function for at least once, return values.
"""

def is_even(num):
    """Return True if number is even"""
    return num%2 == 0

def square(num):
    """Return Square of number"""
    return num*num   

def max_num(num,num1):
    """Return maximum of two numbers, wihtout using inbuilt functions"""
    return num1 if num1>num else num

def main():
    num = int(input("Enter one number: "))
    print(f"{num} number even : {is_even(num)}")
    print(f"Square of {num} = {square(num)}")

    num1 = int(input("Enter second number: "))
    print(f"Between {num} and {num1}, {max_num(num, num1)} is maximum")

if __name__ == "__main__":
    main()