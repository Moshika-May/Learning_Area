# Kasidej Mahanin 6810742293

# Input section
water_need = int(input('ป้อนจำนวนน้ำที่ต้องการดื่ม (ml): '))

# Calculation section
bottle_size = 150
bottle_price = 5

if water_need <= 250 and water_need > 150:
    bottle_size = 250
    bottle_price = 7
elif water_need <= 500 and water_need > 250:
    bottle_size = 500
    bottle_price = 10
elif water_need <= 1000 and water_need > 500:
    bottle_size = 1000
    bottle_price = 20
elif water_need <= 2000 and water_need > 1000:
    bottle_size = 2000
    bottle_price = 35

# Print section
print(f'แนะนำให้ซื้อขวดน้ำขนาด {bottle_size} ml',
      f'รวมเป็นเงิน: {bottle_price} Baht', sep=('\n'))