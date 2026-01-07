Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows

PS C:\Users\6810742293> py
Python 3.12.5 (tags/v3.12.5:ff3bc82, Aug  6 2024, 20:45:27) [MSC v.1940 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> tuple1 = (1, 2, 3, 4)
>>> tuple1[0]
1
>>> tuple1[-1]
4
>>> tuple1[1:3]
(2, 3)
>>> tuple2 = tuple1[1:3]
>>> tuple2
(2, 3)
>>> tuple 1
  File "<stdin>", line 1
    tuple 1
          ^
SyntaxError: invalid syntax
>>> tuple1
(1, 2, 3, 4)
>>> max(tuple1), min(tuple1), sum(tuple1)
(4, 1, 10)
>>> 1, 2, 3
(1, 2, 3)
>>> tuple1 = 1, 2, 3, 4
>>> tuple1
(1, 2, 3, 4)
>>> 1 in tuple1
True
>>> 1 not in tuple1
False
>>> len(tuple1)
4
>>>
>>>
>>>
>>>
>>>
>>>
>>>
>>> tuple1
(1, 2, 3, 4)
>>> tuple1.index(2)
1
>>> tuple1.append(5)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'append'
>>> tuple1.remove(4)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'remove'
>>>
>>>
>>> tuple1.reverse()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'reverse'
>>>
>>>
>>>
>>> tuple1.sort()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'sort'
>>>
>>>
>>> tuple1
(1, 2, 3, 4)
>>> tuple1 = (3, 1, 2, 4)
>>> tuple1
(3, 1, 2, 4)
>>> tuple1.sort()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'sort'
>>>
>>>
>>> sorted(tuple1)
[1, 2, 3, 4]
>>> tuple1
(3, 1, 2, 4)
>>> list1 = sorted(tuple1)
>>> list1
[1, 2, 3, 4]
>>>
>>>
>>> tuple1 = tuple(list1)
>>> tuple1
(1, 2, 3, 4)
>>>
>>>
>>> tuple1 = (3, 1, 2, 4)
>>>
>>>
>>>
>>>
>>>
>>>
>>> tuple1
(3, 1, 2, 4)
>>> tuple1 = tuple(sorted(list(tuple1)))
>>> tuple1
(1, 2, 3, 4)
>>> for num in tuple1:
... print(num)
  File "<stdin>", line 2
    print(num)
    ^
IndentationError: expected an indented block after 'for' statement on line 1
>>>
>>>
>>>
>>>
>>>
>>>
>>>
>>>
>>>
>>>
>>> tuple1
(1, 2, 3, 4)
>>> list1 = list(tuple1)
>>> list1
[1, 2, 3, 4]
>>> list1.remove(3)
>>> list1
[1, 2, 4]
>>> tuple1 = tuple(list1)
>>> tuple1
(1, 2, 4)
>>>
>>>
>>>
>>>
>>>
>>>
>>> tuple2 = (2)
>>> tuple2
2
>>> tuple2 = (2,)
>>> tuple2
(2,)
>>>
>>>
>>>
>>> "yo bro".split()
['yo', 'bro']
>>> list1 = "Kasidej Mahanin".split()
>>> list1
['Kasidej', 'Mahanin']
>>> name = list1[0]
>>> surname = list1[1]
>>> name , surname
('Kasidej', 'Mahanin')
>>> name, surname = "Kasidej Mahanin".split()
>>> name
'Kasidej'
>>> surname
'Mahanin'
>>>
>>>
>>>
>>>
>>> full_name = input("Input your name: ")
Input your name: Somsak Rakthai
>>> full_name
'Somsak Rakthai'
>>> name ,surname = full_name.split()
>>> name , surnam
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'surnam' is not defined. Did you mean: 'surname'?
>>> name , surname
('Somsak', 'Rakthai')
>>>
>>>
>>>
>>>
>>>
>>> name, surname = input("Input your name: ").split()
Input your name: Somsak
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: not enough values to unpack (expected 2, got 1)
>>> name, surname = input("Input your name: ").split()
Input your name: Somsak Rakthai
>>> name, surname
('Somsak', 'Rakthai')
>>>
>>>
>>>
>>>
>>>
>>> numbers = input("Input 5 numbers: ".split())
['Input', '5', 'numbers:']1
>>> 2
2
>>> 3
3
>>> 4
4
>>> 5
5
>>>
>>>
>>>
>>>
>>>
>>> numbers = input("Input 5 numbers: ").split()
Input 5 numbers: 1
>>> 2
2
>>> numbers = input("Input 5 numbers: ").split()
Input 5 numbers: 1 2 3 4 5
>>> numbers
['1', '2', '3', '4', '5']
>>> numbers = int(input("Input 5 numbers: ").split())
Input 5 numbers: 1 2 3 4 5
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: int() argument must be a string, a bytes-like object or a real number, not 'list'
>>> numbers = int(input("Input 5 numbers: ")).split()
Input 5 numbers: 1 2 3 4 5
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: invalid literal for int() with base 10: '1 2 3 4 5'