# Cheat sheet python

# Mathmatical_Functions ====================================================================================================
# abs(): Returns the absolute value of a number.
# abs(-10) returns 10.

# divmod(): Returns the quotient and remainder of a division as a tuple.
# divmod(7, 3) returns (2, 1).

# max(): Returns the largest item in an iterable or the largest of two or more arguments.
# max([1, 5, 2]) returns 5.

# min(): Returns the smallest item in an iterable or the smallest of two or more arguments.
# min([1, 5, 2]) returns 1.

# pow(x, y, z=None): Returns x to the power of y. If z is present, it returns x to the power of y modulo z.
# pow(2, 3) returns 8.

# round(number, ndigits=None): Rounds a number to a specified number of decimal places.
# round(3.14159, 2) returns 3.14.

# sum(iterable, start=0): Sums the items of an iterable.
# sum([1, 2, 3]) returns 6.

# Type conversion and creation ====================================================================================================

# bool(x): Converts a value to its Boolean representation (True or False).
# bool(0) returns False.

# bytes(source, encoding, errors): Returns a new immutable bytes object.

# bytearray(source, encoding, errors): Returns a new mutable array of bytes.

# chr(i): Returns the string character for a given Unicode integer.
# chr(97) returns 'a'.

# complex(real, imag): Creates a complex number.
# complex(3, 4) returns (3+4j).

# dict(): Creates a new dictionary.

# float(x): Converts a string or number to a floating-point number.
# float('3.14') returns 3.14.

# frozenset(iterable): Returns a new frozenset object.

# int(x, base=10): Converts a string or number to an integer.
# int('10') returns 10.

# list(iterable): Creates a new list.

# set(iterable): Creates a new set.

# str(object): Returns the string representation of an object.
# str(123) returns '123'.

# tuple(iterable): Creates a new tuple. 

# Iterables and iterators ====================================================================================================

# all(iterable): Returns True if all elements of the iterable are true (or if the iterable is empty).

# any(iterable): Returns True if any element of the iterable is true.

# enumerate(iterable, start=0): Returns an enumerate object that yields pairs of (index, item).

# filter(function, iterable): Constructs an iterator from elements of an iterable for which a function returns true.

# iter(object, sentinel=None): Returns an iterator for an object.

# len(s): Returns the length of an object (sequence or collection).

# map(function, iterable, ...): Applies a function to all items in an iterable and returns a map object.

# next(iterator, default=None): Retrieves the next item from an iterator.

# range(start, stop, step): Returns an immutable sequence of numbers, often used in for loops.

# reversed(seq): Returns a reverse iterator.

# sorted(iterable, key=None, reverse=False): Returns a new sorted list from the items in an iterable.

# slice(start, stop, step): Returns a slice object.

# zip(iterable, ...): Creates an iterator of tuples from multiple iterables.

# Input and output ====================================================================================================

# input(prompt=None): Reads a line from user input.

# print(objects, sep=' ', end='\n', file=sys.stdout): Prints objects to the text stream file.

# Object inspection and utilities

# callable(object): Returns True if the object is callable (can be executed).

# dir(object): Tries to return a list of valid attributes for the object.

# getattr(object, name, default=None): Returns the value of a named attribute of an object.

# hasattr(object, name): Returns True if the object has a named attribute.

# hash(object): Returns the hash value of an object.

# help(object): Invokes the built-in help system.

# id(object): Returns the unique identity of an object.

# isinstance(object, classinfo): Returns True if the object is an instance of the class or a subclass.

# issubclass(class, classinfo): Returns True if class is a subclass of classinfo.

# repr(object): Returns a printable representation of an object.

# setattr(object, name, value): Sets the value of a named attribute of an object.

# type(object): Returns the type of an object.

# vars(object): Returns the __dict__ attribute of an object. 

# Program execution ====================================================================================================

# breakpoint(*args, **kwargs): Enters the debugger at the call site.

# compile(source, filename, mode, flags=0, dont_inherit=False, optimize=-1): Compiles a string or AST object into a code object.

# eval(expression, globals=None, locals=None): Evaluates a Python expression from a string.

# exec(object, globals=None, locals=None): Executes dynamically created program code.

# open(file, mode='r', ...): Opens a file and returns a file object.

# __import__(name, globals=None, locals=None, fromlist=(), level=0): Used by the import statement. 

# Object-oriented programming ====================================================================================================

# classmethod(function): Returns a class method for a function.

# object(): Returns a new featureless object.

# property(fget=None, fset=None, fdel=None, doc=None): Returns a property attribute.

# staticmethod(function): Returns a static method for a function.

# super(type, object_or_type=None): Returns a proxy object that delegates method calls to a parent or sibling class.

# Asynchronous functions ====================================================================================================

# aiter(async_iterable): Returns an asynchronous iterator.

# anext(async_iterator): Returns the next item from an asynchronous iterator.