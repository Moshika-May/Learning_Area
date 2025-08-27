# check Age must be >= 0
while True:
   age = int(input('Enter age: '))
   if age >= 0:
       break
   print('Invalid age')
print(f'Your age is {age}.') 	    
