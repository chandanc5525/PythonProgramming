# --------------------------------------------------
# Session 4: Introduction to Python
# --------------------------------------------------
## Author: Chandan Chaudhari
## Github: https://github.com/chandanc5525
# --------------------------------------------------

# Tuple in Python Programming

''' 
Tuple: Tuple is a built-in data structure in Python that represents an ordered collection of items, similar to lists.
However, tuples are immutable, meaning you cannot modify their contents after creation.
They can contain elements of different data types, including integers, floats, strings, and even other
tuples.
Tuples are defined using parentheses () and elements are separated by commas.

Example:
my_tuple = (1, 2, 3, "Hello", 4.5, (5, 6))

'''

my_tuple = (1, 2, 3, "Hello", 4.5, (5, 6))
print(my_tuple)

# Accessing elements in a tuple
print(my_tuple[0])  # First element
print(my_tuple[2])  # Third element
print(my_tuple[-1]) # Last element

# ---------------------------------------------------

# Tuple Methods are as follows:

# Counting occurrences of an element in a tuple
print(my_tuple.count(2))  # Output: 1

# Finding the index of an element in a tuple
print(my_tuple.index("Hello"))  # Output: 3

# Concatenating two tuples

tuple1 = (1, 2, 3)
tuple2 = (4, 5, 6)

concatenated_tuple = tuple1 + tuple2
print(concatenated_tuple)  # Output: (1, 2, 3, 4, 5, 6)

# Repeating a tuple
repeated_tuple = tuple1 * 2
print(repeated_tuple)  # Output: (1, 2, 3, 1, 2, 3)

# Slicing a tuple
sliced_tuple = concatenated_tuple[1:5]
print(sliced_tuple)  # Output: (2, 3, 4, 5)

# ---------------------------------------------------

# tuple Comprehension in Python

# Note: Python does not have a built-in syntax for tuple comprehensions like list comprehensions.
# However, you can create a tuple using a generator expression and the tuple() constructor.

squared_tuple = tuple(x**2 for x in range(5))
print(squared_tuple)  # Output: (0, 1, 4, 9, 16)

# ---------------------------------------------------