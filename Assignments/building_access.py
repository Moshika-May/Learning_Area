# 6810742293 Kasidej Mahanin

# Define dictionary data
members = {
    "A1029": "Prayut S.",
    "B0071": "Nattaya K.",
    "C2210": "Michael T."
}

def main():

    # Input
    card_id = input("Input card ID: ")

    # Check if card_id exists in members dictionary
    if card_id in members:
        
        # Get name from value
        name = members[card_id]

        # Determine card type from first char
        first_char = card_id[0]
        card_type = ""

        if first_char == "A":
            card_type = "Staff"
        elif first_char == "B":
            card_type = "Student"
        elif first_char == "C":
            card_type = "Visitor"

        # Get sequence number (slice string from index 1 to end)
        sequence_num = card_id[1:]

        # Print found details
        print("Name:", name)
        print("Card type:", card_type)
        print("Sequence number:", sequence_num)

    else:
        # Case not found
        print("Access Denied")

# Call function
main()