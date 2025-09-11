# 6810742293 Kasidej Mahanin

average_car_week = 0
total_car_week = 0
slot_time = 0
car_highest_week = 0
highest_car_day = 0

while True:
    days_number = int(input('Input number of days: '))
    if days_number <= 7 and days_number > 0:
        break
    else:
        print('Invalid day plase enter number of day(1-7)')

slot_capacity = int(input('Input number of time slots per day: '))

for day_list in range(1, days_number + 1):
    print(f'Day {day_list} ----------')
    average_car_day = 0
    slot_car = 0
    car_highest_day = 0
    count = 0
    for slot_list in range(1, slot_capacity + 1):
        slot_car = int(input(f'Time slot no.{slot_list}: '))
        count += 1
        slot_time += 1
        total_car_week += slot_car
        average_car_day += slot_car
        if slot_car > car_highest_day:
            car_highest_day = slot_car
        if slot_car > car_highest_week:
            car_highest_week = slot_car
            highest_car_day = day_list
        if count == slot_capacity:
            average_car_day = average_car_day / count
            print(f'Average cars in this day: {average_car_day:.2f}')
            print(f'Most cars in this day: {car_highest_day}')

average_car_week = total_car_week / slot_time

print(f'Average cars per week: {average_car_week:.2f}')
print(f'Day {highest_car_day} had the most cars: {car_highest_week}')