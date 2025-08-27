student_list = [
    "Alice", 
    "Bob", 
    "Charlie", 
    "David", 
    "Eve"
]

student_to_find = input("Enter the name of the student to find their position: ")

if student_to_find in student_list:
    index = student_list.index(student_to_find)
    print(f"The student '{student_to_find}' is at position {index}.")
else:
    print(f"The student '{student_to_find}' is not in the class list.")
