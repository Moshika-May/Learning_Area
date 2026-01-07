import time
import os

count = 0
for dd in range(1, 7):
    for hh in range(24):
        for mm in range(60):
            for ss in range(60):
                print(f"{dd:02d}:{hh:02d}:{mm:02d}:{ss:02d}")
                count += 1
                time.sleep(0.001)
                os.system('cls')       # for windows, use 'clear' for Linux/Mac
print(f"Total combinations: {count}")