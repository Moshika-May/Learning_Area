def remove_duplicates(str_a):
    char = []
    last_char = None
    
    for i in str_a:
        if i != last_char:
            char.append(i)
        last_char = i
    return "".join(char)

def main():
    print(remove_duplicates("bookkeeeeeper"))

if __name__ == "__main__":
    main()