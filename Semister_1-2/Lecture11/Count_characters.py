def count_char_frequency(text):
    frequency = {}
    for char in text:

        if char == ' ':
            continue

        if char in frequency:
            frequency[char] += 1

        else:
            frequency[char] = 1
            
    return frequency

def main():
    print(count_char_frequency("banana"))

if __name__ == "__main__":
    main()