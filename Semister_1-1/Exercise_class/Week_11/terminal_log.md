>>> import random
>>> random.random()
0.16581741951526285
>>> random.random()
0.18506944421889304
>>> random.random()
0.2524165952542172
>>> random.random()
0.9133825838719356
>>> random.random()
0.18294962177127583
>>> round(random.random())
1
>>> round(random.random())
0
>>> round(random.random())
0
>>> round(random.random())
1
>>> round(random.random())
0
>>> round(random.random())
1
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
>>> random.uniform(10, 20)
13.690402313324398
>>> random.uniform(10, 20)
18.28053121960053
>>> random.uniform(10, 20)
10.385827084932995
>>> random.uniform(10, 20)
16.440392436151946
>>> random.uniform(10, 20)
19.23152783490149
>>> random.uniform(10, 20)
14.089731337492108
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
>>> from random import randint, ran
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: cannot import name 'ran' from 'random' (C:\Program Files\Python312\Lib\random.py)
>>> from random import randint
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
>>> randint(1, 5)
5
>>> randint(1, 5)
1
>>> randint(1, 5)
5
>>> randint(1, 5)
2
>>> randint(1, 5)
4
>>> randint(1, 5)
3
>>> randint(1, 5)
2
>>> randint(1, 5)
4
>>> randint(1, 5)
2
>>> seed(1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'seed' is not defined
>>> from random import seed
>>> seed(1)
>>> randint(1, 5)
2
>>> randint(1, 5)
5
>>> randint(1, 5)
1
>>> randint(1, 5)
3
>>> randint(1, 5)
1
>>> randint(1, 5)
4
>>>
>>>
>>>
>>> seed(2)
>>> randint(1, 5)
1
>>> randint(1, 5)
1
>>> randint(1, 5)
1
>>> randint(1, 5)
3
>>> randint(1, 5)
2
>>> randint(1, 5)
3
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
>>> str1 = "CN101"
>>> str1[0]
'C'
>>> str1[-5]
'C'
>>> str1[0] = 'B'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'str' object does not support item assignment
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
>>> str1
'CN101'
>>> str1[0:2]
'CN'
>>> 'cn101'.isalnum()
True
>>> 'cnN'.isalnum()
True
>>> '2222'.isalnum()
True
>>> 'cn-101'.isalnum()
False
>>> 'cn-101'.isalpha()
False
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
>>> '100'.isdigit()
True
>>> 'tse100'.isdigit()
False
>>> 'tse100'.islower()
True
>>> 'tse100'.isupper()
False
>>> 'TSE100'.isupper()
True
>>> 'CN101'.isspace()
False
>>> ' '.isspace()
True
>>> ' \n'.isspace()
True
>>> ' \n'.isspace()
True
>>> '\n'.isspace()
True
>>> '\t'.isspace()
True
>>> 'CN101'.lower()
'cn101'
>>> 'cn101'.upper()
'CN101'
>>> ' CN101 '.strip()
'CN101'
>>> ' CN101\n '.strip()
'CN101'
>>> ' CN\t101\n '.strip()
'CN\t101'
>>> ' CN101\n '.lstrip()
'CN101\n '
>>> ' \tCN101\n '.lstrip()
'CN101\n '
>>> ' \tCN101\n '.rstrip()
' \tCN101'
>>> ' \tCN101\n '.strip()
'CN101'
>>> 'CN101'.strip('1')
'CN10'
>>> 'CN101'.strip('C')
'N101'
>>> 'CN101'.strip()
'CN101'
>>> 'CN101'.strip('10')
'CN'
>>> 'CN101'.strip('0123456789')
'CN'
>>> '784272453CN10175645786278523'.strip('0123456789')
'CN'
>>> '784272453CN10175645786278523'.lstrip('0123456789')
'CN10175645786278523'
>>> '784272453CN10175645786278523'.rstrip('0123456789')
'784272453CN'
>>> '784272453CN10175645786278523'.strip('0123456789')
'CN'
>>> ' CN\t101\n '.strip()
'CN\t101'
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
>>> 'CN101'.endswith('101')
True
>>> 'CN101'.endswith('10')
False
>>> 'CN101'.endswith('01')
True
>>> 'CN101'.endswith('CN')
False
>>> 'CN101'.startswith('CN')
True
>>> 'cn101'.startswith('CN')
False
>>> 'cn101'.startswith('CN')
False
>>> 'cn101'.upper().startswith('CN')
True
>>> 'cn101'.startswith('CN').startswith('cn')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'bool' object has no attribute 'startswith'
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
>>> 'CN' in 'CN101'
True
>>> 'CN101'.find('CN')
0
>>> 'CN101'.find('CN101')
0
>>> 'CN101'.find('101')
2
>>> 'CN101'.replace('101', '111')
'CN111'
>>> 'CN101'.replace('1', '2')
'CN202'
>>> 'CN101'.replace('1', '22')
'CN22022'
>>> 'CN101'.replace('1', '')
'CN0'
>>> 'Mr.Somsak Rakthai'.replace('Mr.', '')
'Somsak Rakthai'
>>> 'Mr. Somsak Rakthai'.replace('Mr.', '').strip()
'Somsak Rakthai'
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
>>> 'CN\n101'.split()
['CN', '101']
>>> 'CN\t101'.split()
['CN', '101']
>>> 'CN 101'.split()
['CN', '101']
>>> 'CN                           101'.split()
['CN', '101']
>>> 'CN         \n          \t        101'.split()
['CN', '101']
>>> 'CN/101'.split('/')
['CN', '101']
>>> '4/Nov/1989'.split('/')
['4', 'Nov', '1989']
>>> date, month, year = '4/Nov/1989'.split('/')
>>> date
'4'
>>> month
'Nov'
>>> year
'1989'
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
>>> date = '4/Nov/1989'.split('/')
>>> date
['4', 'Nov', '1989']
>>>
>>> '/'.join(date)
'4/Nov/1989'
>>>
>>> 'abcdbdb'.split('b')
['a', 'cd', 'd', '']
>>>
>>> 'b'.join(['a', 'cd', 'd', ''])
'abcdbdb'
>>> 'b'.join(['a', 'cd', 'd'])
'abcdbd'
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
>>> print('a\b')
a
>>> print('a\b\b')
a
>>>