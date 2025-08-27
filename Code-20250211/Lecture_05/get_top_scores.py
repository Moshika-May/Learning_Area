# Define the scores list
scores = [98, 95, 93, 89, 87, 85, 80, 75]

# Get the number of top scores to retrieve from the user
num_top = int(input("Enter the number of top scores to retrieve: "))

# Retrieve the top scores
top_scores = scores[:num_top]

# Print the top scores
print(f"Top {num_top} scores: {top_scores}")
