# Kasidej Mahanin 6810742293

# Constants
PACKAGE_PRICE = 99.00

# Input number of packages
number_of_packages = int(input('Number of packages purchased: '))
discount = 0.00

# Calculate total price with discount
if number_of_packages >= 10 and number_of_packages <= 19:
        discount = 0.10
elif number_of_packages >= 20 and number_of_packages <= 49:
        discount = 0.20
elif number_of_packages >= 50 and number_of_packages <= 99:
        discount = 0.30
elif number_of_packages >= 100:
        discount = 0.40
total_price = number_of_packages * PACKAGE_PRICE * (1 - discount)
normal_price = number_of_packages * PACKAGE_PRICE
discount_price = normal_price * discount

# Print the result
print(f'Normal amount: {normal_price:,.2f} Baht',
      f'Discount amount: {discount_price:,.2f} Baht',
      f'Total amount: {total_price:,.2f} Baht', sep='\n')