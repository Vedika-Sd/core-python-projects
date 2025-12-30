"""
Task — Digit Operations
Write three functions:

1️⃣ count_digits(n)
Returns number of digits
Handle negative numbers correctly

2️⃣ sum_of_digits(n)
Returns sum of digits
Ignore sign (-123 → 6)

3️⃣ reverse_number(n)
Returns reversed number
No string conversion

Rules:
Use while loop
Use return, not print

No strings (str() forbidden)
"""

def count_digits(n):
    count = 0
    while n>0:
        count+=1
        n = n//10
    return count

def sum_of_digits(n):
    sum = 0
    while n>0:
        sum = sum + n%10
        n//=10
    return sum

def reverse_number(n):
    rev = 0
    while n>0:
        rev = rev * 10 + n%10
        n//=10
    return rev

def main():
    n = int(input("Enter any number: "))
    total_count = count_digits(n)
    print(f"Digit count in number {n} is {total_count}")
    total_sum = sum_of_digits(abs(n))
    print(f"Sum of digits in number {n} is {total_sum}")
    reversed_num = reverse_number(abs(n))
    print(f"Reversed number of {n} is {reversed_num}")

if __name__ == "__main__":
    main()
        
