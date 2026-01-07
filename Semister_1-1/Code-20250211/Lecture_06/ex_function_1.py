# Q01. write a function that should print the student ids, names and their marks".
# Q02. write a function that should print the number of students".
# Q03. write a function that should print the number of tests".
# Q04. write a function that should print the highest mark of each student".
# Q05. write a function that should print the lowest mark of each student".
# Q06. write a function that should print the average mark of each student".
# Q07. write a function that should print the highest mark of a given test".
# Q08. write a function that should print the lowest mark of a given test".
# Q09. write a function that should print the average mark of a given test".
# Q10. write a function that should print the test with the highest total mark".
# Q11. write a function that should print the test with the lowest total mark".
# Q12. write a function that should print the test with the highest average mark".
# Q13. write a function that should print the test with the lowest average mark".
# Q14. write a function that should print the student ids and names with the highest average mark".
# Q15. write a function that should print the student ids and names with the lowest average mark".
# Q16. write a function that should print the student ids and names with the highest total mark".
# Q17. write a function that should print the student ids and names with the lowest total mark".
# Q18. write a function that should print the student ids and names with the highest mark in each test".
# Q19. write a function that should print the student ids and names with the lowest mark in each test".
# Q20. write a function that should print the student ids and names who pass a given test with the given minimum pass mark".
# Q21. write a function that should print the student ids and names who fail a given test with the given minimum pass mark".
# Q22. write a function that should print the standard deviation of a given test".
# Q23. write a function that should print the median of a given test".
# Q24. write a function that should print the mode of a given test".
# Q25. write a function that should print the student ids and names that have mark more than standard deviation in a given test".
# Q26. write a function that should print the student ids and names that have mark more than median in a given test".
# Q27. write a function that should print the student ids and names that have mark more than mode in a given test".
# Q28. write a function that should print the student ids and names that sorted in ascending order by mark in a given test".
# Q29. write a function that should print the student ids and names that sorted in descending order by mark in a given test".
# Q30. write a function that should print the student ids and names that sorted in ascending order by student id in a given test".
# Q31. write a function that should print the student ids and names that sorted in descending order by student id in a given test".

# For each function. the first parameter should be "data".
# any other parameters should be added as needed for each question
# e.g. student id. test number. etc.

import csv

DEFAULT_CSV_FILENAME = "data_1.csv"


def read_csv(filename=DEFAULT_CSV_FILENAME):
    """
    Reads a CSV file containing student marks and returns its contents as a list of lists.

    Parameters
    ----------
    filename: str
      The path to the CSV file to be read.
      If not provided. the default filename will be used.

    Returns
    -------
    res: list
      A list of lists representing the contents of the CSV file.
      Each inner list represents a row in the CSV file.
      with each element representing a column value.
        format: [
                    [id, fist_name, last_name, mark1, mark2, ...],
                    [id, fist_name, last_name, mark1, mark2, ...],
                    ...
                ]
    """
    res = []
    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            items = [row[0], row[1], row[2]]
            for mark in row[3:]:
                items.append(int(mark))
            res.append(items)
    return res


def print_students(data):
    for item in data:
        marks = [ str(m) for m in item[3:] ]
        s = ""
        for mark in marks:
            s += ", " + mark
        print(f"{item[0]}: {item[1]} {item[2]}{s}")


def main():
    data = read_csv()
    print_students(data)


if __name__ == "__main__":
    main()
