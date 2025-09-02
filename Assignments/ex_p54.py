# Kasidej Mahanin 6810742293

# Constants
SERVICE_CHARGE = 24.62
VAT = 0.07

# Input energy consumption
power_unit = int(input('Enter the energy consumption (kilowatt-hours): '))

# calculate electricity cost
if power_unit >= 0:
    if power_unit <= 150:
        electicity_cost = power_unit * 3.2484
    elif power_unit <= 400:
        electicity_cost = (150 * 3.2484) + ((power_unit - 150) * 4.2218)
    else:
        electicity_cost = (150 * 3.2484) + (250 * 4.2218) + ((power_unit - 400) * 4.4217)

    
    vat_cost = (SERVICE_CHARGE + electicity_cost) * VAT
    total_cost = SERVICE_CHARGE + electicity_cost + vat_cost

    print(f'Electricity cost = {electicity_cost:.2f} Baht',
          f'Service charge = {SERVICE_CHARGE:.2f} Baht',
          f'VAT (7 Percent) = {vat_cost:.2f} Baht',
          f'Total cost = {total_cost:.2f} Baht', sep='\n')
else:
    print('Invalid input')