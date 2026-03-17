def three_consecutive(num1, num2, num3):
    if num1 > num2 > num3:
        consecutive_check_set_A = num1 - num2
        consecutive_check_set_B = num2 - num3

        if consecutive_check_set_A == 1 and consecutive_check_set_B == 1:
            return True
        return False
    
    if num1 > num3 > num2:
        consecutive_check_set_A = num1 - num3
        consecutive_check_set_B = num3 - num2

        if consecutive_check_set_A == 1 and consecutive_check_set_B == 1:
            return True
        return False

    if num2 > num3 > num1:
        consecutive_check_set_A = num2 - num3
        consecutive_check_set_B = num3 - num1

        if consecutive_check_set_A == 1 and consecutive_check_set_B == 1:
            return True
        return False

    if num2 > num1 > num3:
        consecutive_check_set_A = num2 - num1
        consecutive_check_set_B = num1 - num3

        if consecutive_check_set_A == 1 and consecutive_check_set_B == 1:
            return True
        return False

    if num3 > num1 > num2:
        consecutive_check_set_A = num3 - num1
        consecutive_check_set_B = num1 - num2

        if consecutive_check_set_A == 1 and consecutive_check_set_B == 1:
            return True
        return False

    if num3 > num2 > num1:
        consecutive_check_set_A = num3 - num2
        consecutive_check_set_B = num2 - num1

        if consecutive_check_set_A == 1 and consecutive_check_set_B == 1:
            return True
        return False
    return False


def main():
    print(f"Three consecutive numbers {three_consecutive(3, 4, 2)}")

if __name__ == "__main__":
    main()