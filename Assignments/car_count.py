# 6810742293 Kasidej Mahanin

days_number = int(input('Input number of days: '))
slot_capacity = int(input('Input number of time slots per day: '))

for day_parked in range(0, days_number):
    print(f'Day {day_parked} ----------')
    for slot in range(0, slot_capacity):
        slot_1 = int(input())
