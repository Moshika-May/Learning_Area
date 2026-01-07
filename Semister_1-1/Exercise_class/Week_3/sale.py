sales = float(input('Input sales: '))
salary = float(input('Input salary: '))

if sales > 50000:
    bonus = 500.00
    commission_rate = 0.12
    print('You met your sales quota!')
else:
    bonus = 0.00

salary_bonus = salary * commission_rate
total_salary = salary + salary_bonus
    
print(f'{sales = :,.2f}')
print(f'{bonus = :.2f}')
print(f'Total salary = {total_salary:,.2f}')