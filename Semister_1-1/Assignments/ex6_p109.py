# 6810742293 Kasidej Mahanin

import math
def area_of_circular_sector(r, d):
    Area = (d / 360) * math.pi * math.pow(r, 2)
    return Area

area_1 = area_of_circular_sector(10, 90)
area_2 = area_of_circular_sector(10, 180)
print(f'Area 1 = {area_1:.2f}, Area 2 = {area_2:.3f}')