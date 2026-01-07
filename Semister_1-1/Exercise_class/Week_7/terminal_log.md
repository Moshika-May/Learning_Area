Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows

PS C:\Users\6810742293> py
Python 3.12.5 (tags/v3.12.5:ff3bc82, Aug  6 2024, 20:45:27) [MSC v.1940 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> list1 = [0, 1, 2, 3, 4]
>>> list1.append(5)
>>> list1
[0, 1, 2, 3, 4, 5]
>>> list1.index
<built-in method index of list object at 0x0000015C9EE31240>
>>> list1.index(3)
3
>>> list1.insert(-1, 0)
>>> list1
[0, 1, 2, 3, 4, 0, 5]
>>> list1.insert(0, -1)
>>> list1
[-1, 0, 1, 2, 3, 4, 0, 5]
>>> list1.sort()
>>> list1
[-1, 0, 0, 1, 2, 3, 4, 5]
>>> cleaR
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'cleaR' is not defined
>>> CLEAR
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'CLEAR' is not defined
>>> clear
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'clear' is not defined
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
>>> list1
[-1, 0, 0, 1, 2, 3, 4, 5]
>>> list1.sort(reverse=True)
>>> list1
[5, 4, 3, 2, 1, 0, 0, -1]
>>> sorted(list1)
[-1, 0, 0, 1, 2, 3, 4, 5]
>>> list1
[5, 4, 3, 2, 1, 0, 0, -1]
>>> list1.sort()
>>> list1.append(6)
>>> list1
[-1, 0, 0, 1, 2, 3, 4, 5, 6]
>>> list1.index(4)
6
>>> index_4 = list1.index(4)
>>> index_4
6
>>> x = list1.append(7)
>>> x
>>> type(x)
<class 'NoneType'>
>>> y =
  File "<stdin>", line 1
    y =
        ^
SyntaxError: invalid syntax
>>> y = x
>>> type(y)
<class 'NoneType'>
>>> clear
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'clear' is not defined
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
>>>
>>>
>>>
>>>
>>>
>>>
>>>
>>>
>>>
>>> list1
[-1, 0, 0, 1, 2, 3, 4, 5, 6, 7]
>>> list1.remove(0)
>>> lost1
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'lost1' is not defined. Did you mean: 'list1'?
>>> list1
[-1, 0, 1, 2, 3, 4, 5, 6, 7]
>>> list1.remove(-1)
>>> list1
[0, 1, 2, 3, 4, 5, 6, 7]
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
>>>
>>>
>>> list1
[0, 1, 2, 3, 4, 5, 6, 7]
>>> list1.reverse()
>>>
>>> list1
[7, 6, 5, 4, 3, 2, 1, 0]
>>> list1.append(-1)
>>> list1
[7, 6, 5, 4, 3, 2, 1, 0, -1]
>>> list1.reverse()
>>> list1
[-1, 0, 1, 2, 3, 4, 5, 6, 7]
>>> list1[::-1]
[7, 6, 5, 4, 3, 2, 1, 0, -1]
>>> list1
[-1, 0, 1, 2, 3, 4, 5, 6, 7]
>>> list1 = list1[::-1]
>>> list1
[7, 6, 5, 4, 3, 2, 1, 0, -1]
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
>>>
>>>
>>>
>>>
>>>
>>>
>>>
>>>
>>>
>>> list1
[7, 6, 5, 4, 3, 2, 1, 0, -1]
>>> list1.reverse()
>>> list1
[-1, 0, 1, 2, 3, 4, 5, 6, 7]
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
>>>
>>> list1
[-1, 0, 1, 2, 3, 4, 5, 6, 7]
>>> list1.remove(-1)
>>> list1
[0, 1, 2, 3, 4, 5, 6, 7]
>>> del list1[6]
>>> list1
[0, 1, 2, 3, 4, 5, 7]
>>> del list1[list1.index(7)]
>>> list1
[0, 1, 2, 3, 4, 5]
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
>>>
>>>
>>> list1
[0, 1, 2, 3, 4, 5]
>>> max(list1)
5
>>> min(list1)
0
>>> sum(list1)
15
>>> sum(list1) / len(list1)
2.5
>>> sum(list1, 10)
25
>>> sum(list1, 100)
115
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
>>> list1
[0, 1, 2, 3, 4, 5]
>>> list2 += list1
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'list2' is not defined. Did you mean: 'list1'?
>>> list2 = list11
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'list11' is not defined. Did you mean: 'list1'?
>>> list2 = list1
>>> clear
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'clear' is not defined
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
>>>
>>>
>>>
>>>
>>>
>>>
>>>
>>>
>>>
>>> list1
[0, 1, 2, 3, 4, 5]
>>> list2
[0, 1, 2, 3, 4, 5]
>>> list2 *= 10
>>> list2
[0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5]
>>> list2 = list1
>>> list2[-1] *= 10
>>> list2
[0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 50]
>>> list1
[0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 50]
>>> list1 = [0, 1, 2, 3, 4, 5]
>>> list1
[0, 1, 2, 3, 4, 5]
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
>>>
>>>
>>> list2 = list1
>>> list2[-1] *= 10
>>> list2
[0, 1, 2, 3, 4, 50]
>>> list1
[0, 1, 2, 3, 4, 50]
>>> list1.append(6)
>>> list2
[0, 1, 2, 3, 4, 50, 6]
>>> list3 = list2
>>> list4 = list3
>>> list5 = list4
>>> list5
[0, 1, 2, 3, 4, 50, 6]
>>> list5.remove(50)
>>> list1
[0, 1, 2, 3, 4, 6]
>>> list1,list2,list3
([0, 1, 2, 3, 4, 6], [0, 1, 2, 3, 4, 6], [0, 1, 2, 3, 4, 6])
>>> list4, list5
([0, 1, 2, 3, 4, 6], [0, 1, 2, 3, 4, 6])
>>> id(list1), id(list2)
(1497314300480, 1497314300480)
>>> id(list3), id(list4), id(list5)
(1497314300480, 1497314300480, 1497314300480)
>>> list6 = [0, 1, 2, 3, 4, 6]
>>> list6
[0, 1, 2, 3, 4, 6]
>>> id(list6)
1497317918464
>>> list6.remove(6)
>>> list6
[0, 1, 2, 3, 4]
>>> list1
[0, 1, 2, 3, 4, 6]
>>> list1
[0, 1, 2, 3, 4, 6]
>>> list2 = [] + list1
>>> list2
[0, 1, 2, 3, 4, 6]
>>> id(list1), id(list2)
(1497314300480, 1497319232768)
>>> list3 = []
>>> for num in list1:
...     list3.append(num)
...
>>> list3
[0, 1, 2, 3, 4, 6]
>>> id(list1), id(list2), id(list3)
(1497314300480, 1497319232768, 1497314448896)
>>> list4 = list1[:]
>>> list4
[0, 1, 2, 3, 4, 6]
>>> id(list1), id(list2), id(list3), id(list4)
(1497314300480, 1497319232768, 1497314448896, 1497319235456)
>>> list5 = list1.copy()
>>> id(list1), id(list2), id(list3), id(list4), id(list5)
(1497314300480, 1497319232768, 1497314448896, 1497319235456, 1497319230912)