# Kasidej Mahanin 6810742293
PACKAGE_PRICE = 99.00

number_of_packages = int(input('Number of packages purchased: '))
normal_price = number_of_packages * PACKAGE_PRICE
if number_of_packages >= 0:
    if number_of_packages >= 10 and number_of_packages <= 19:
        discount = 0.10
    elif number_of_packages >= 20 and number_of_packages <= 49:
        discount = 0.20
    elif number_of_packages >= 50 and number_of_packages <= 99:
        discount = 0.30
    elif number_of_packages >= 100:
        discount = 0.40
    total_price = number_of_packages * PACKAGE_PRICE * (1 - discount)
    print(f'Total amount due: {total_price:.2f} Baht')
