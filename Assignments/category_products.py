# 6810742293 Kasidej Mahanin

def main():

    # Initialize main dictionary
    products = {}

    # Input number of categories
    num_categories = int(input("Input number of categories: "))

    # Loop based on number of categories
    for _ in range(num_categories):
        
        # Add newline for formatting match
        print() 
        category_name = input("Input category name: ")

        # List to store products for this category
        item_list = []

        # Loop to get products until 'q'
        while True:
            product = input("Enter product (or 'q' to stop): ")
            if product == 'q':
                break
            item_list.append(product)

        # Sort list alphabetically
        item_list.sort()

        # Add to dictionary (Key=Category, Value=List)
        products[category_name] = item_list

    # Output section
    print("\n--- Result ---")

    # Iterate through dictionary to print results
    for category, items in products.items():
        print("Category:", category)
        print("Products:", items)
        print("Total =", len(items))
        print() # Empty line between categories

# Call function
main()
