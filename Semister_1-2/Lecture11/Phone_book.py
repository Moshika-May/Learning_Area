"""
File: phonebook.py
------------------
This file implements a fun phonebook program, 
where we can store people's phone numbers
and tell the user which numbers are available.
"""

def print_all_phone_numbers(phonebook):
    for name in phonebook:
        print(f"{name} -> {phonebook[name]}")

def lookup_phone_number(phonebook):
    name = input("Name to look up within our phonebook: ")
    if name in phonebook:
        phone_number = phonebook[name]
        print(f"{name}'s phone number is {phone_number}")
    else:
        print(f"{name} does not exist within our phonebook")

def add_new_number(phonebook):
    # Add the phone number key/value pair to our phone book
    name = input("Enter the name: ")
    phone_number = input("Enter the phone number: ")

    if name in phonebook:
        print(f"Updating {name}'s phone number")

    phonebook[name] = phone_number

def main():

    phonebook = {}

    print("Welcome to SF210 Phonebook!")
    print("Options include: ")
    print("(A)dd a phone number to our phone book")
    print("(L)ookup a phone number in our phone book")
    print("(P)rint all the values in our phone book")
    print("Hit the return key to close the phone book")

    while True:

        user_input = input("Enter an option: ")

        if user_input == "A":
            add_new_number(phonebook)

        elif user_input == "L":
            lookup_phone_number(phonebook)

        elif user_input == "P":
            print_all_phone_numbers(phonebook)

        elif user_input == "":
            break

        else:
            print("Invalid input!")



if __name__ == "__main__":
    main()