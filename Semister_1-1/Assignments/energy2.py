# Kasidej Mahanin 6810742293

# Declaring section

# Declaring Constants
# Fixed service charge, VAT percentage, and electricity unit rates
SERVICE_CHARGE = 24.62  # Base service charge
VAT = 0.07              # VAT rate (7%)
UNIT_RATE_1 = 3.2484    # Rate for first 150 units
UNIT_RATE_2 = 4.2218    # Rate for 151–400 units
UNIT_RATE_3 = 4.4217    # Rate for units above 400

# Declaring variables
# Variables to control looping and input validation
loop_input = 'y'        # User input to decide continue or stop
input_unit_loop = True  # Control while-loop for validating power_unit input
continue_loop = True    # Control while-loop for main program

# Main loop section
# Repeats program until user chooses "n"
# For each run: validate input, calculate costs, print results
while continue_loop == True:
    if loop_input == 'y':
        # Input section
        # Ask user for power consumption (must be 0–1000)
        power_unit = int(input('Enter the energy consumption (kilowatt-hours): '))

        # Validation loop: keep asking until input is between 0–1000
        if power_unit < 0 or power_unit > 1000:
            while input_unit_loop == True:
                if power_unit >= 0 and power_unit <= 1000:
                    input_unit_loop = False
                else:
                    power_unit = int(input('Enter a valid energy consumption [0-1000]: '))

        input_unit_loop = True  # Reset input_unit_loop for next round

        # Electricity cost calculation section
        # Split by tier system: first 150, next 250, and above 400 units
        if power_unit <= 150:
            electicity_cost = power_unit * UNIT_RATE_1
        elif power_unit <= 400:
            electicity_cost = (150 * UNIT_RATE_1) + ((power_unit - 150) * UNIT_RATE_2)
        else:
            electicity_cost = (150 * UNIT_RATE_1) + (250 * UNIT_RATE_2) + ((power_unit - 400) * UNIT_RATE_3)
                    
        # VAT and total calculation
        vat_cost = (SERVICE_CHARGE + electicity_cost) * VAT
        total_cost = SERVICE_CHARGE + electicity_cost + vat_cost

        # Output section
        # Display detailed breakdown of the electricity bill
        print(f'Electricity cost = {electicity_cost:,.2f} Baht',
              f'Service charge = {SERVICE_CHARGE:.2f} Baht',
              f'VAT (7 Percent) = {vat_cost:,.2f} Baht',
              f'Total cost = {total_cost:,.2f} Baht', sep='\n')

        # Ask user whether to continue or not
        loop_input = input('Do you want to continue? (y/n): ')

    elif loop_input == 'n':     # Exit program
        continue_loop = False
    else:                       # Invalid input for continuation
        loop_input = input('Enter [y/n] to continue: ')
print('Goodbye!')