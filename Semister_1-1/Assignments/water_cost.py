# Kasidej Mahanin 6810742293

# Input section
liter_recieve = int(input('Enter the number of liters consumed: '))
rate_per_liter = float(input('Enter the rate per liter: '))

# Calculation section
if liter_recieve < 500:
    water_cost = liter_recieve * rate_per_liter
else:
    water_cost = (500 * rate_per_liter) + ((liter_recieve - 500) * rate_per_liter * 1.2)

# Print section
print(f'The total water cost is ${water_cost:,.2f}')