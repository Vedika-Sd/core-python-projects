# check armstrong number
"""
A number is Armstrong if
sum of each digit raised to power of number of digits equals the number
Ex. 
153 -> 3 digits
153 → 1³ + 5³ + 3³ = 153 → True

9474 → 4 digits
4⁴ + 7⁴ + 4⁴ + 9⁴ = 9474


"""
def check_armstrong(n):
    original_n = n
    cube_sum = 0
    num_digits = len(str(n))  # converting to string to count digits
    
    while n>0:
        digit = n%10
        cube_sum = cube_sum + digit**num_digits
        n//=10

    if original_n == cube_sum:
        return True
    else:
        return False

def main():
    n = int(input("Enter any number: "))
    print(f"Is {n} Armstrong Number : {check_armstrong(n)}")    
if __name__ == "__main__":
    main()
        

