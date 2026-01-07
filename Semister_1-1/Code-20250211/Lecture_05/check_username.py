# Define the registered users
registered_users = ["alice", "bob", "charlie", "david"]

# Get the username from the user
username = input("Enter a username to check: ")

# Check if the username is in the registered users
if username in registered_users:
    print(f"Welcome back, {username}!")
else:
    print(f"{username} is not a registered user.")
