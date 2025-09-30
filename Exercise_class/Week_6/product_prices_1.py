# List of products and their prices
products = ["Laptop", "Smartphone", "Tablet", "Headphones", "Smartwatch"]
prices = [1200.00, 800.00, 400.00, 100.00, 200.00]

# Original products and prices
print("\nOriginal products and prices:")
for index in range(len(products)):
    print(f"{products[index]}: ${prices[index]:.2f}")

# User input for the product to modify and the new price
product_to_modify = input("\nEnter the name of the product to modify the price: ")
product_to_modify in products

# Searching for the product and updating its price using list slicing
found = False
for i in range(len(products)):
    new_price = float(input(f"Enter the new price for {product_to_modify}: "))
    if products[i] == product_to_modify:
        prices = prices[:i] + [new_price] + prices[i+1:]
        found = True
        break

if not found:
    print(f"Product named {product_to_modify} not found in the list.")

# Updated products and prices
else:
    print("\nUpdated products and prices:")
    for index in range(len(products)):
        print(f"{products[index]}: ${prices[index]:.2f}")
