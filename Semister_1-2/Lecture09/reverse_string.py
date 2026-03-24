"""
File: reverse_string.py
------------------------
This program asks the user for some textual input
and then prints out what the reverse of that string
would be.
"""

def reverse_string(s):
	"""
	This function takes in a string, reverses the characters,
	and returns the reversed string back to the user. The original
	string is left unaffected.

	Parameters:
		* string s, original contents
	Return:
		* string, representing reversed version of the input

	>>> reverse_string("cs106a")
	'a601sc'

	>>> reverse_string("")
	''

	>>> reverse_string("mom")
	'mom'
	"""
	reverse = ""
	for ch in s:
		reverse = ch + reverse

	return reverse

def main():
	user_input = input("Enter some text: ")
	rev = reverse_string(user_input)
	print(f"{user_input} backwards is {rev}")

if __name__ == "__main__":
	main()