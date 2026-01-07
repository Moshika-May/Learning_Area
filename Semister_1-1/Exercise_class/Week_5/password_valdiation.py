while True:
    password = input('Input password (>= 6 Characters): ')
    if len(password) < 6:
        print('Error: Password must be at least 6 characters long.')
        continue
    confirm_password = input('Confirm password: ')
    if password != confirm_password:
        print('Error: Passwords do not match. Please try again.')
        continue
    print
    break
