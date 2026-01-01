"""Task: String Analyzer (Easy + Useful + Interview-safe)

What you must do
Take a string input from user
Write separate functions for:

count_vowels(s)
count_consonants(s)
count_digits(s)
count_spaces(s)

Call all functions from main()

Print a clean summary
"""
def count_vowels(s):
    vowels = "aeiou"
    count_vowel = 0
    for i in s:
        if i in vowels:
            count_vowel+=1
    return count_vowel

def count_consonants(s):
    vowels = "aeiou"
    count_consonant = 0
    for i in s:
        if i.isalpha() and i not in vowels:
            count_consonant+=1
    return count_consonant

def count_digits(s):
    count_digit = 0
    for i in s:
        if i.isdigit():
            count_digit+=1
        return count_digit

def count_spaces(s):
    count_space = 0
    for i in s:
        if i.isspace():
            count_space+=1
        return
    
def main():
    user_input = input("Enter a string: ").lower()
    vowels = count_vowels(user_input)
    consonants = count_consonants(user_input)
    digits = count_digits(user_input)
    spaces = count_spaces(user_input)

    print("\nString Analysis Summary:")
    print(f"Vowels: {vowels}")
    print(f"Consonants: {consonants}")
    print(f"Digits: {digits}")
    print(f"Spaces: {spaces}")

if __name__ == "__main__":
    main()