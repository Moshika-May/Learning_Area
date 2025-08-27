# Initial inventory list of products in the store
inventory = ["Apple", "Banana", "Orange", "Grape", "Mango"]

# Display items to customers (referencing the same inventory list)
display_items_list = inventory

print("Items available:")
for item in display_items_list:
    print(f"- {item}")
print()

# Simulating a customer buying an item
purchased_item = input("Enter the name of the item the customer wants to buy: ")
if purchased_item in inventory:
    inventory.remove(purchased_item)
    print(f"\nCustomer purchased: {purchased_item}")
else:
    print(f"\n{purchased_item} is not available in the inventory.")

# Display items to customers after the purchase
print("Items available after purchase:")
for item in display_items_list:
    print(f"- {item}")
print()
