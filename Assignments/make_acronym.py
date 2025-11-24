# 6810742293 Kasidej Mahanin

# Define function
def make_acronym(sentence):

    # Split sentence into words
    words = sentence.split()

    # Variable for storing result
    acronym = ""

    # Loop each word
    for word in words:
        # Get first char and make it upper
        acronym += word[0].upper()

    # Return result
    return acronym

def main():

    # Input
    sentence_input = input("Input sentence: ")

    # Call func and print output
    result = make_acronym(sentence_input)
    print("Acronym =", result)

# Call function
main()