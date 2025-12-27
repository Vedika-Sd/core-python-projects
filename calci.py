while True:
    try:
        num1, num2 = map(int, input("Enter two numbers with space-separated: ").split())
        op = input("Enter operation (add, sub, div, mult, power): ").lower()

        if op == "add":
            print("Addition =", num1 + num2)

        elif op == "sub":
            print("Subtraction =", num1 - num2)

        elif op == "mult":
            print("Multiplication =", num1 * num2)

        elif op == "div":
            if num2 == 0:
                print("Error: Division by zero not allowed")
            else:
                print("Division =", num1 / num2)
                print("Floor Division =", num1 // num2)
                print("Remainder =", num1 % num2)

        elif op == "power":
            print(f"{num1} ^ {num2} =", num1 ** num2)

        else:
            print("Invalid operation")

    except ValueError:
        print("Please enter valid integers")

    choice = input("Do you want to continue? (y/n): ").lower()
    if choice == "n":
        break
