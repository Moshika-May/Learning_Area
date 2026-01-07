# Example list of books read over a month
books_read = []

# Adding more books based on user input
while True:
    new_book = input("Enter a new book you've read (or 'q' to quit): ")
    if new_book == 'q':
        break
    books_read.append(new_book)
    
# Display the updated list of books
print("Updated list of books read this month:")
for book in books_read:
	print(book)
