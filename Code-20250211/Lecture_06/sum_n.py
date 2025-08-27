def sum_n(n):
    s = 0
    for i in range(1, n+1):
        s = s + i
    return s

x = sum_n(5)
y = sum_n(10)

print(f"x = {x}")
print(f"y = {y}")
