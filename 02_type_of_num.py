# Check if number is positive, negative or zero Also check if number is even or odd
def check_integer(num):
    if num > 0:
        print("This is postive number")
    elif num<0:
        print("This is negative number")
    else:
        print("This is zero")

def check_even_odd(num):
    if num%2==0:
        print("Number is even")
    else:
        print("Number is odd")

def main():
    num = int(input("Enter number: "))
    check_integer(num)
    check_even_odd(num)

if __name__ == "__main__":
    main() 