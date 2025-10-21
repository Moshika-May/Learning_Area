def print_info(name, surname, age):
    print(f'Hello {surname} {name}!, this is your {age} years!')

def main():
    name = input('Input your name: ')
    surname = input('Input your surname: ')
    age = int(input('Input age: '))
#     name = "Mochi"
#     surname = "Cestiana"
    print_info(name, surname, age)

main()