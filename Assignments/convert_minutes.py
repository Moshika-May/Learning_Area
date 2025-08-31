# 6810742293 กษิดิ์เดช มหานิล 760001

# Input section
receive = int(input('Enter number of minutes: '))

# Calculation section
x = int(receive // 1440)
y = int((receive % 1440) / 60)
z = int(receive % 60)

# print section
print(f"{x} day(s), {y} hour(s), {z} minute(s)")