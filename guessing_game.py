print("Lets play a guessing game!")
secret_no = 37

while True:
    user_no = int(input("Enter your gueesing number that match with this computers secret number: "))

    if user_no == secret_no:
        print("Congatulations you win! you correctly guessed secret no. ", secret_no)
    else:
        print("Wrong guessing, Try again")

    choice = input("want to continue? y/n").lower()
    if choice == 'n':
        break