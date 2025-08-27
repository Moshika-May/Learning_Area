# Example CSV line representing a record
csv_line = "John Doe,35,New York"

# Split the line into individual fields based on the comma separator
fields = csv_line.split(",")

# Assign the fields to variables for easier access
name = fields[0]
age = fields[1]
city = fields[2]

print("Name:", name)
print("Age:", age)
print("City:", city)