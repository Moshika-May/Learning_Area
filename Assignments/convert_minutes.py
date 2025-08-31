receive = int(input('Enter number of minutes: '))

x = int(receive//1440)
y = int((receive%1440)/60)
z = int(receive%60)
print(f"{x} day(s), {y} hour(s), {z} minute(s)")