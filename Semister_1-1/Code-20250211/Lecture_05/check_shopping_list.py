# Define the shopping list
shopping_list = ["milk", "eggs", "bread", "butter"]

# Get the item from the user
item = input("Enter an item to check in the shopping list: ")

# Check if the item is in the shopping list
if item not in shopping_list:
    print(f"{item} is not in your shopping list.")
else:
    print(f"{item} is already in your shopping list.")
