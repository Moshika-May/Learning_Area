# 6810742293 กษิดิ์เดช มหานิล 760001

# Input section
first_num = int(input('Enter first number: '))
second_num = int(input('Enter secnod number: '))

# Calculation section
calculation_a = first_num + second_num
calculation_b = first_num - second_num
calculation_c = first_num * second_num
calculation_d = first_num / second_num
calculation_e = first_num // second_num
calculation_f = first_num % second_num
calculation_g = first_num ** second_num

# print section
print(f'{first_num} + {second_num} = {calculation_a}',
      f'{first_num} - {second_num} = {calculation_b}',
      f'{first_num} * {second_num} = {calculation_c}',
      f'{first_num} / {second_num} = {calculation_d}',
      f'{first_num} // {second_num} = {calculation_e}',
      f'{first_num} % {second_num} = {calculation_f}',
      f'{first_num} ** {second_num} = {calculation_g}', sep=('\n'))