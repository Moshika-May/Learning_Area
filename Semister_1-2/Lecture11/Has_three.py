def has_three(list_1):
    dic_word = {}
    for word in list_1:
        if word not in dic_word:
            dic_word[word] = 1

        elif word in dic_word:
            dic_word[word] += 1
    
    for word in dic_word:
        value = dic_word[word]
        # print(f'{word} ----> {value}')

        if value == 3:
            return True
    return False

def main():
    list_A = ["to", "be", "or", "be", "to", "be", "hamlet"]
    print(has_three(list_A))

if __name__ == "__main__":
    main()
    