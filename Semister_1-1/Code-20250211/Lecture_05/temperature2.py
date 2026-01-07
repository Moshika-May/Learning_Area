# Initial list of daily temperatures over a week
temperatures = [22.5, 24.0, 19.8, 21.3, 25.0]

print("Initial daily temperatures:")
for i, temp in enumerate(temperatures, 1):
    print(f"Day {i}: {temp}°C")

# Adding new temperature readings
while True:
    new_temp = input("Enter a new temperature reading (or 'q' to quit): ")
    if new_temp == 'q':
        break
    temperatures.append(float(new_temp))

print("\nUpdated daily temperatures:")
for i, temp in enumerate(temperatures, 1):
    print(f"Day {i}: {temp}°C")

# Analyzing temperature data
min_temp = min(temperatures)
max_temp = max(temperatures)
avg_temp = sum(temperatures) / len(temperatures)

print(f"\nMinimum temperature: {min_temp}°C")
print(f"Maximum temperature: {max_temp}°C")
print(f"Average temperature: {avg_temp:.2f}°C")
