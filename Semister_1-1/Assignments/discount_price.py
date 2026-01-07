# 6810742293 กษิดิ์เดช มหานิล 760001

# Input section
normal_price = float(input('Enter normal price: '))
discount_percent = float(input('Enter percent discount: '))

# Calculation section
discount_price = normal_price * (discount_percent / 100)

# print section
print(f'Normal price: {normal_price:,.2f}')
print(f'Percent discount: {discount_percent:,.2f}%')
print(f'Discounted price: {normal_price - discount_price:,.2f}')