import math

def length_of_triangle(a, b, x):
    # x is angle in radians, between two sides a and b
    radian = math.radians(x)
    c = math.sqrt(a * a + b * b - a * b * math.cos(radian))
    return c

def main():
    a, b = input("Enter lengths of 2 sides: ").split()
    x = input("Enter angle between the 2 sides (degree): ")
    a, b = float(a), float(b)
    x = float(x)
    c = length_of_triangle(a, b, x)
    print(f"Length of remaining side = {c}")

main()
