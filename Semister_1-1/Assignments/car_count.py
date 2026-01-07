# 6810742293 Kasidej Mahanin

# Declaring variables section
# These variables will be used to track cars across all days and slots.
average_car_week = 0       # Store weekly average of cars
total_car_week = 0         # Total cars for all slots in all days
slot_time = 0              # Counter for total time slots (used for averaging)
car_highest_week = 0       # Maximum cars seen in a single slot across the whole week
highest_car_day = 0        # Day number that had the most cars in a slot

# Input validation loop for days.
# Ask user to input number of days (1–7)
# Repeat until a valid number is entered
while True:
    days_number = int(input('Input number of days: '))
    if days_number <= 7 and days_number > 0:
        break
    else:
        print('Invalid day plase enter number of day(1-7)')

# Input for slot capacity
# After days_number is validated, program asks how many time slots per day.
slot_capacity = int(input('Input number of time slots per day: '))

# Outer for-loop section
# Iterates through each day from 1 up to number of days entered by user.
# For each day, program initializes counters for daily average and max.

for day_list in range(1, days_number + 1):
    print(f'Day {day_list} ----------')
    average_car_day = 0   # Temporary storage for total cars in a single day
    slot_car = 0          # Number of cars entered in current slot
    car_highest_day = 0   # Highest car count seen in current day
    count = 0             # Slot counter for current day

    # Inner for-loop section
    # Iterates through each time slot for the current day.
    # For every slot, user inputs number of cars and program processes it.
    for slot_list in range(1, slot_capacity + 1):
        slot_car = int(input(f'Time slot no.{slot_list}: '))
        count += 1
        slot_time += 1
        total_car_week += slot_car
        average_car_day += slot_car

        # Check and update daily maximum
        if slot_car > car_highest_day:
            car_highest_day = slot_car

        # Check and update weekly maximum
        # If current slot has more cars than current weekly max,
        # update weekly maximum and also note which day it occurred.
        if slot_car > car_highest_week:
            car_highest_week = slot_car
            highest_car_day = day_list
        
        # When finished all slots of the day (count == slot_capacity),
        # calculate and print daily average and daily maximum.
        if count == slot_capacity:
            average_car_day = average_car_day / count
            print(f'Average cars in this day: {average_car_day:.2f}')
            print(f'Most cars in this day: {car_highest_day}')

# Weekly average calculation section
# After all days and slots are completed,
# program computes the weekly average from total cars and total slots.
average_car_week = total_car_week / slot_time

# Output section
# Program prints the overall average cars per week
# and reports the day that had the single highest number of cars in any slot.
print(f'Average cars per week: {average_car_week:.2f}')
print(f'Day {highest_car_day} had the most cars: {car_highest_week}')