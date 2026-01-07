import math
def factorial(n):
    fact = 1
    for i in range(1, n+1):
        fact = fact * i
    return fact

x = factorial(5)      # using user-defined function
y = math.factorial(5) # using function factorial in math module

print(f"x = {x}, y = {y}")
