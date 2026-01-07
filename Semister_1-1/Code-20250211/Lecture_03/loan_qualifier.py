# This program determines whether a bank customer
# qualifies for a loan.

MIN_SALARY = 30000.0  # The minimum annual salary
MIN_YEARS = 2         # The minimum years on the job

# Get the customer's annual salary.
salary = float(input('Enter your annual salary: '))

# Get the number of years on the current job.
prompt = 'Enter the number of years employed: '
years_on_job = int(input(prompt))

# Determine whether the customer qualifies.
if salary >= MIN_SALARY:
    if years_on_job >= MIN_YEARS:
        print('You qualify for the loan.')
    else:
        msg = 'You must have been employed '
        msg += f'for at least {MIN_YEARS} '
        msg += 'years to qualify.'  
        print(msg)
else:
    msg = 'You must earn at least '
    msg += f'{MIN_SALARY:,.2f} per year to qualify.'
    print(msg)
