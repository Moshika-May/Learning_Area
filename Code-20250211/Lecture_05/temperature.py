# Example temperature data for a month (30 days)
temperatures = [
    22.5, 23.0, 21.5, 22.0, 24.5, 25.0, 23.5, 
    24.0, 26.5, 27.0, 25.5, 26.0, 28.5, 29.0, 
    30.5, 28.0, 27.5, 28.0, 29.5, 30.0, 31.5, 
    32.0, 33.5, 31.0, 30.5, 32.0, 33.5, 34.0, 
    35.5, 36.0
]

# Get user input for operations
week_number = int(input("Enter the week number (1-4) to view temperatures: "))
num_hottest_days = int(input("Enter the number of hottest days to retrieve: "))
start_day = int(input("Enter the start day for average temperature calculation (1-30): "))
end_day = int(input("Enter the end day for average temperature calculation (1-30): "))

# Extract weekly temperatures
start = (week_number - 1) * 7
end = week_number * 7
weekly_temperatures = temperatures[start:end]
print(f"Temperatures for week {week_number}: {weekly_temperatures}")

# Find the hottest days
hottest_days = sorted(temperatures, reverse=True)[:num_hottest_days]
print(f"The top {num_hottest_days} hottest days: {hottest_days}")

# Calculate average temperature for a specified period
period_temperatures = temperatures[start_day-1:end_day]
sum_temperatures = 0
for temperature in period_temperatures:
    sum_temperatures += temperature
average_temperature = sum_temperatures / len(period_temperatures)
print(f"Average temperature from day {start_day} to day {end_day}: {average_temperature:.2f}°C")
