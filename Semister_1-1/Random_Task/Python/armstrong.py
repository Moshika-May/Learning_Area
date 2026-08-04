def armstrong_numbers(n):
    # 1. Handle invalid inputs
    if n <= 0:
        return
        
    # 2. Set the exact boundaries for n-digit numbers
    if n == 1:
        start = 0
    else:
        start = 10 ** (n - 1)
        
    end = 10 ** n
    
    # List to store the numbers we find
    results = []
    
    # 3. Iterate through every number in our range
    for num in range(start, end):
        
        # Create a temporary variable so we don't destroy the original number
        temp = num
        total_sum = 0
        # 4. Extract digits mathematically
        while temp > 0:
            print(f"temp_before: {temp}")
            # Get the rightmost digit (e.g., 153 % 10 = 3)
            digit = temp % 10
            print(f"digit: {digit}")
            # Raise that digit to the power of n and add it to our running total
            total_sum = total_sum + (digit ** n)
            print(f"total_sum: {total_sum}")
            # Remove the rightmost digit from temp (e.g., 153 // 10 = 15)
            temp = temp // 10
            print(f"temp_after: {temp}")

        # 5. Check if it is an Armstrong number
        if total_sum == num:
            print("total_sum == num: True")
            results.append(str(num))
            
    # 6. Print the results on a single line separated by spaces
    if len(results) > 0:
        print(" ".join(results))

# Example call
armstrong_numbers(7)