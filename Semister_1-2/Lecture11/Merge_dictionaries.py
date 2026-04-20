def merge_dictionaries(dict1, dict2):
    dict3 = {}

    for key, value in dict1.items():
        dict3[key] = value
    
    for key, value in dict2.items():
        if key in dict3:
            dict3[key] += value

        else:
            dict3[key] = value
            
    return dict3

def main():
    dict_a = {'a': 10, 'b': 20}
    dict_b = {'b': 5, 'c': 15}
    print(merge_dictionaries(dict_a, dict_b))

if __name__ == "__main__":
    main()