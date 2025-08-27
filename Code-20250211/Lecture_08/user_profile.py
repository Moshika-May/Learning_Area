def update_user_profile(user_profile, new_info):
    """
    Updates the user profile dictionary with new information.
    """
    user_profile.update(new_info)
    return user_profile

def get_user_input():
    """
    Collects updated user profile information from user input.
    """
    print("Enter updated profile information (leave blank to skip):")
    
    new_info = {}
    
    email = input("Email: ").strip()
    if email:
        new_info['email'] = email
    
    location = input("Location: ").strip()
    if location:
        new_info['location'] = location
    
    bio = input("Bio: ").strip()
    if bio:
        new_info['bio'] = bio
    
    return new_info

def main():
    # Initial user profile
    user_profile = {
        'username': 'johndoe',
        'email': 'johndoe@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'location': 'New York'
    }

    # Get new information from user input
    new_info = get_user_input()

    # Update user profile with the new information
    updated_profile = update_user_profile(user_profile, new_info)

    # Print the updated user profile
    print("\nUpdated user profile:")
    print(updated_profile)

main()
