'''
PI * R ^ 2
cal_circle_area และ cal_circumference และ main
input "radius"
PI = 3.14159
'''

def cal_circle_area(radius):
    PI = 3.14159
    circle_area = PI * (radius ** 2)
    print(f'Circle Area: {circle_area:,.2f}')

def cal_circumference(radius):
    PI = 3.14159
    circumference = 2 * PI * radius
    print(f'Circunference: {circumference:,.2f}')

def main():
    radius = float(input('Input radius: '))
    cal_circle_area(radius)
    cal_circumference(radius)

main()