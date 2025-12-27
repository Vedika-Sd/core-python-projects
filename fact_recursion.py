def fact(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * fact(n - 1)

def main():
    n = int(input("Enter a number to calculate its factorial: "))
    result = fact(n)
    print(f"The factorial of {n} is {result}")

if __name__ == "__main__":
    main()