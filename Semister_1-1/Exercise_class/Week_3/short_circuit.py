a = int(input("Enter a number: "))
b = int(input("Enter another number: "))
if b != 0 and a / b > 1: # if a / b > 1 and b != 0: # This would raise an error if b is 0
    print(f'{a}/{b} is greater than 1')
print('bye')