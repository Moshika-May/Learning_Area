def remove_number(string):
    result = ""

    for ch in string:
        if not ch.isdigit():
            result += ch

    return result

def main():
    sample = "a1b2c3"
    print(f'From {sample} to {remove_number(sample)}')

if __name__ == "__main__":
    main()
