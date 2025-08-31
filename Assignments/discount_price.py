normal_price = float(input('Enter normal price: '))
discount_percent = float(input('Enter percent discount: '))

discount_price = normal_price*(discount_percent/100)
print(f'Normal price: {normal_price:,.2f}')
print(f'Percent discount: {discount_percent:,.2f}%')
print(f'Discounted price: {normal_price-discount_price:,.2f}')