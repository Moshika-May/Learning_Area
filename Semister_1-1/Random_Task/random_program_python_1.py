# Ok I am stupid + Programer มือใหม่
from math import sqrt,pow


# Constant number
G_EARTH = 9.81 # m/s²
G_CONSTANT = 6.67430 * (10 ** -11) # m³⋅kg⁻¹⋅s⁻²
PI = 3.14159265359
SPACING_A = '==================================='
INPUT_SECTION = 'Input sections'
OUTPUT_SECTION = 'Output sections'
TYPE_CONVERSION_AND_CREATION = 'Type conversion and creation'
BOOLEAN_1 = bool(1)
BOOLEAN_0 = bool(0)

print(f'\n{SPACING_A}  {INPUT_SECTION:^4}  {SPACING_A}', end=('\n\n'))


# Input values
name = input('Input ur name: ')
radius = float(input('Radius: '))
num_a = float(input('Input Negative number: '))


# Calculation
Introducing = f'{name.title()}'
Circle_area = PI*(pow(radius,2))
Square_area = pow(radius,2)
if num_a > 1:
    num_a = num_a*(-1)    # num_a was always negative number
Rad_sq_x2 = round((pow(radius,2))*2,2)
Num_a_abs_div = divmod(abs(num_a),3)
Highest_num = max(radius,abs(num_a))
Lowest_num = min(radius,abs(num_a))
Sum_num = sum([radius,num_a])


# Headliner
print(f'\n{SPACING_A}  {OUTPUT_SECTION:^4}  {SPACING_A}', end=('\n\n'))


print(f'This is answer from {Introducing}.', 
      f'\nCircle area: {Circle_area:,.2f}m²', 
      f'radius: {radius}m', 
      f'Regtangle square area: {round(Square_area,2)}m²',
      f'If we used rad to calculate ((rad^2)*2): {Rad_sq_x2}m', sep=('\n'), end=('\n\n'))
print(f'Your number was: {abs(num_a):,.2f}'+
      f'\nYour negative number was: {num_a:,.2f}'+
      f'\nYour negative number with absolute and square root: {sqrt(abs(num_a)):,.3f}'+
      f'\nYour negative number after divided by 3: {Num_a_abs_div}'+
      f'\nYour highest input was: {Highest_num:,.2f}'+
      f'\nYour lowest input was: {Lowest_num:,.2f}'+
      f'\nSum of rad and negative number: {Sum_num:,.2f}', end=('\n\n'))
print('Here are matrix 3x3 easy table:\n|1\t|2\t|3\n|4\t|5\t|6\n|7\t|8\t|9', end=('\n\n'))


print(f'\n{SPACING_A}  {TYPE_CONVERSION_AND_CREATION:^4}  {SPACING_A}', end=('\n\n'))
print(f'Value of boolean_1 is: {BOOLEAN_1}',
      f'Value of boolean_0 is: {BOOLEAN_0}', sep=('\n'), end=('\n\n'))
print(f'{BOOLEAN_1} and {BOOLEAN_1} is: {BOOLEAN_1 and BOOLEAN_1}',
      f'{BOOLEAN_1} and {BOOLEAN_0} is: {BOOLEAN_1 and BOOLEAN_0}',
      f'{BOOLEAN_0} and {BOOLEAN_1} is: {BOOLEAN_0 and BOOLEAN_1}',
      f'{BOOLEAN_0} and {BOOLEAN_0} is: {BOOLEAN_0 and BOOLEAN_0}',
      f'\n{BOOLEAN_1} or {BOOLEAN_1} is: {BOOLEAN_1 or BOOLEAN_1}',
      f'{BOOLEAN_1} or {BOOLEAN_0} is: {BOOLEAN_1 or BOOLEAN_0}',
      f'{BOOLEAN_0} or {BOOLEAN_1} is: {BOOLEAN_0 or BOOLEAN_1}',
      f'{BOOLEAN_0} or {BOOLEAN_0} is: {BOOLEAN_0 or BOOLEAN_0}',
      f'\n{BOOLEAN_1} xor {BOOLEAN_1} is: {(BOOLEAN_1 ^ BOOLEAN_1)}',
      f'{BOOLEAN_1} xor {BOOLEAN_0} is: {(BOOLEAN_1 ^ BOOLEAN_0)}',
      f'{BOOLEAN_0} xor {BOOLEAN_1} is: {(BOOLEAN_0 ^ BOOLEAN_1)}',
      f'{BOOLEAN_0} xor {BOOLEAN_0} is: {(BOOLEAN_0 ^ BOOLEAN_0)}', sep=('\n\n'))
char_a = chr(97) # ASCII 97 = a
char_b = chr(98) # ASCII 98 = b
char_c = chr(99) # ASCII 99 = c
print(f'\nCharacter of 97 is: {char_a}',
      f'Character of 98 is: {char_b}',
      f'Character of 99 is: {char_c}', sep=('\n'), end=('\n\n'))