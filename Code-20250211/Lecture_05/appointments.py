# Initial list of appointments for a week
appointments = [
    "Monday: Doctor's appointment at 10:00 AM",
    "Tuesday: Team meeting at 2:00 PM",
    "Wednesday: Lunch with Sarah at 12:30 PM",
]

print("Initial list of appointments:")
for i, appointment in enumerate(appointments, 1):
    print(f"{i}. {appointment}")

# Prompt the user to input the number of the appointment to delete
appointment_number = int(input("Enter the number of the appointment to delete: "))

# Validate the appointment number
if 1 <= appointment_number <= len(appointments):
    del appointments[appointment_number - 1]
    print(f"\nAppointment number {appointment_number} has been deleted.")
else:
    print(f"\nInvalid appointment number: {appointment_number}")

print("\nList of appointments after deletion:")
for i, appointment in enumerate(appointments, 1):
    print(f"{i}. {appointment}")
