def count_duplicates(list_int):
    seen = set()
    duplicates = 0
    
    for num in list_int:
        if num in seen:
            duplicates += 1
        else:
            seen.add(num)
            
    return duplicates

def main():
    a = [2, 4, 6, 8, 10, 12, -2, -4]
    print(count_duplicates(a))

if __name__ == "__main__":
    main()