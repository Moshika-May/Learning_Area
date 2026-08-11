def main():
    x = input("enter number: ")
    number_input_1, sign, number_input_2 = x.split()
    if sign == "+":
        i = int(number_input_1) + int(number_input_2)
    elif sign == "-":
        i = int(number_input_1) - int(number_input_2)
    elif sign == "*":
        i = int(number_input_1) * int(number_input_2)
    elif sign == "/":
        i = int(number_input_1) / int(number_input_2)
    else:
        print("Invalid input")
    print(f"Result: {i}")

if __name__ == "__main__":
    main()
