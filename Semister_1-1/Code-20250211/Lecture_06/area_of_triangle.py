import math

def area_of_triangle(a, b, c):
    s = 0.5 * (a + b + c)
    area = math.sqrt(s*(s-a)*(s-b)*(s-c))
    return area

def main():
    a, b, c = input("Enter lengths of 3 sides: ").split()
    a = float(a); b = float(b); c = float(c)
    area = area_of_triangle(a, b, c)
    print(f"Area = {area}")

main()
