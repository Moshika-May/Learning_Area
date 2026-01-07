users = {
    'alice': {
        'age': 25,
        'email': 'alice@example.com'
    }
}

def print_users_table(users):
    """Prints the user data in a table format."""
    print(f"{'Name':<10} {'Age':<5} {'Email':<20}")
    for name, details in users.items():
        age = details['age']
        email = details['email']
        print(f"{name:<10} {age:<5} {email:<20}")

def create_user(users, name, age, email):
    """Create a new user to the dictionary."""
    if name in users:
        return False
    users[name] = {'age': age, 'email': email}
    return True

def update_user(users, name, age=None, email=None):
    """Updates an existing user in the dictionary."""
    if name in users:
        if age is not None:
            users[name]['age'] = age
        if email is not None:
            users[name]['email'] = email
        return True
    else:
        return False

def delete_user(users, name):
    """Deletes a user from the dictionary."""
    if name in users:
        del users[name]
        return True
    else:
        return False

def main():
    while True:
        print("\nUser Management Menu")
        print("1. Display users")
        print("2. Create user")
        print("3. Update user")
        print("4. Delete user")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            print("\nUsers table:")
            print_users_table(users)
        elif choice == '2':
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            email = input("Enter email: ")
            if create_user(users, name, age, email):
                print(f"User {name} added.")
            else:
                print(f"User {name} already exists.")
        elif choice == '3':
            name = input("Enter name: ")
            age = input("Enter age (leave blank to skip): ")
            email = input("Enter email (leave blank to skip): ")
            age = int(age) if age else None
            email = email if email else None
            if update_user(users, name, age, email):
                print(f"User {name} updated.")
            else:
                print(f"User {name} not found.")
        elif choice == '4':
            name = input("Enter name: ")
            if delete_user(users, name):
                print(f"User {name} deleted.")
            else:
                print(f"User {name} not found.")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

main()
