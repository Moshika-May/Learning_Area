# 6810742293 Kasidej Mahanin

# Define function
def check_password(a_string):

    # Lenght >= 8
    if len(a_string) < 8:
        return False

    # Prams for each case
    has_upper = False
    has_lower = False
    has_digit = False

    # Loop each string
    for char in a_string:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
            
    # "TRUE" if prams was right
    return has_upper and has_lower and has_digit

def main():

    # Input
    password_input = input("Input password: ")

    # Call func and print output
    if check_password(password_input):
        print("Strong password.")
    else:
        print("Weak password.")

# Call function main
main()