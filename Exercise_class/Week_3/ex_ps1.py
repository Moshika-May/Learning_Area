# กษิดิ์เดช มหานิล 6810742293
first_int = int(input("Enter integer #1: "))
second_int = int(input("Enter integer #2: "))
third_int = int(input("Enter integer #3: "))
highest = 0

if first_int >= second_int and first_int >= third_int:
    highest = first_int
elif second_int >= first_int and second_int >= third_int:
    highest = second_int
else:
    highest = third_int
print(f'The maximum number is {highest}')