#
# Rewrite the following program to use functions
#

# Example list of books read over a month
books_read = []

# Adding books to the list
books_read.append("1984 by George Orwell")
books_read.append("To Kill a Mockingbird by Harper Lee")
books_read.append("The Great Gatsby by F. Scott Fitzgerald")

# Display the books read
print("Books read this month:")
for book in books_read:
	print(book)

# Adding more books based on user input
while True:
    new_book = input("Enter a new book you've read (or 'q' to quit): ")
    if new_book.lower() == 'q':
        break
    books_read.append(new_book)

# Display the updated list of books
print("Updated list of books read this month:")
for book in books_read:
	print(book)
