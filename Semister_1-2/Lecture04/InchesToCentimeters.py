def main():
    print("This program converts feet and inches to centimeters.")
    feet = int(input("Enter number of feet: "))
    inch = int(input("Enter number of inches: "))
    centimeter = (feet * 30.48) + (inch * 2.54)
    print(f'{feet} ft {inch} in = {centimeter} cm')
    
if __name__ == "__main__":
    main()