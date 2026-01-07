# input email address
email = input("Enter your email address: ")

# Use the find() method to locate the position of the '@' symbol
at_position = email.find('@')

# Check if the '@' symbol was found
if at_position != -1:
    # Extract the domain part by slicing the string from the position after '@'
    domain = email[at_position + 1:]
    print(f"The domain of the email address is: {domain}")
else:
    print("Invalid email address. No '@' symbol found.")
