def sum_list(a_list):
    s = 0
    for i in a_list:
        s = s + i
    return s

list_1 = [1,3,5,7,9]
list_2 = list( range(1,10,2) )

# using user-defined function
x = sum_list(list_1)
y = sum_list(list_2)

# using built-in function sum
a = sum(list_1)
b = sum(list_2)

print(f"x = {x}, y = {y}")
print(f"a = {a}, b = {b}")
