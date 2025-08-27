# examples of value-returning functions
def get_xxx():
    a, b = 10, 20
    return a + b

def get_yyy():
    x, y = 10, 20
    return x + y

print(f"{get_xxx()}")
print(f"{get_yyy()}")

# Both get_xxx and get_yyy are essentially the same functions
# since they both
# - are void functions
# - same parameters (no parameters)
# - have the same body that give the same result
