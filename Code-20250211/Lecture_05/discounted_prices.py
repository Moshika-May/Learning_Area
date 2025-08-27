# Initial list of product prices
prices = [10.0, 20.5, 40.9, 50.0, 100.0]

# Display the original prices
print("Original Prices:")
for index, price in enumerate(prices, 1):
    print(f"Product {index}: ${price:,.2f}")
print()

# Copy prices list into two discounted prices lists for comparison
discounted_prices_1 = [] + prices
discounted_prices_2 = [] + prices

# Get the first discount rate from the user
prompt = "Enter first discount rate (as a percentage, e.g., 10 for 10%): "
discount_rate_1 = float(input(prompt)) / 100

# Get the second discount rate from the user
prompt = "Enter second discount rate (as a percentage, e.g., 15 for 15%): "
discount_rate_2 = float(input(prompt)) / 100

# Apply the first discount to each price in the discounted_prices_1 list
for index in range(len(discounted_prices_1)):
    discounted_prices_1[index] = discounted_prices_1[index] * \
                                 (1 - discount_rate_1)

# Apply the second discount to each price in the discounted_prices_2 list
for index in range(len(discounted_prices_2)):
    discounted_prices_2[index] = discounted_prices_2[index] * \
                                 (1 - discount_rate_2)

# Display the discounted prices for the first discount rate
print("Discounted Prices (First Discount Rate):")
for index, price in enumerate(discounted_prices_1, 1):
    print(f"Product {index}: ${price:,.2f}")
print()

# Display the discounted prices for the second discount rate
print("Discounted Prices (Second Discount Rate):")
for index, price in enumerate(discounted_prices_2, 1):
    print(f"Product {index}: ${price:,.2f}")
print()

# Display the original prices again to show they are unchanged
print("Original Prices After Discount Applied:")
for index, price in enumerate(prices, 1):
    print(f"Product {index}: ${price:,.2f}")
print()
