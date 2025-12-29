# Check if number is prime or not
import math
def check_prime(num: int) -> bool:
    """Return True if num is prime, False otherwise."""
    if num <2:
         return False
    if num == 2:
         return True
    if num%2==0:
         return False
    
    limit = int(math.sqrt(num))
    for i in range(3,limit+1,2):
        if num%i==0:
             return False
        else:
             return True

def main():
        num = int(input("Enter one number: "))
        print(f"{num} is prime: {check_prime(num)}")

if __name__ == "__main__":
    main()