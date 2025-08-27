def get_name():
    # Get the user’s first name and last name.
    full_name = input('Enter your full name: ')
    # Return the name.
    return full_name

def main():
    fisrt_name, last_name = get_name().split()
    print(f"Hello: {fisrt_name} {last_name}")

main()