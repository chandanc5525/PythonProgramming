# --------------------------------------------------
# Session 5: Introduction to Python
# --------------------------------------------------
## Author: Chandan Chaudhari
## Github: https://github.com/chandanc5525
# --------------------------------------------------

# Sets in Python Programming
'''
Set: A set is a built-in data structure in Python that represents an unordered collection of unique items.
Sets are defined using curly braces {} or the set() constructor, and they do not allow duplicate
elements. Sets are mutable, meaning you can add or remove elements after creation. They are commonly
used for operations like union, intersection, and difference.

Example:
my_set = {1, 2, 3, "Hello", 4.5}

'''

# ---------------------------------------------------

my_set = {1, 2, 3, "Hello", 4.5}
print(my_set)

# Adding an element to a set
my_set.add(6)
print(my_set) # Output: {1, 2, 3, 'Hello', 4.5, 6}

# Removing an element from a set
my_set.remove(2)
print(my_set) # Output: {1, 3, 'Hello', 4.5, 6}

# Checking if an element is in a set
print(3 in my_set) # Output: True
print(2 in my_set) # Output: False

# ---------------------------------------------------

# Set Methods are as follows:

# Union of two sets
set1 = {1, 2, 3}
set2 = {3, 4, 5}

union_set = set1.union(set2)
print(union_set) # Output: {1, 2, 3, 4, 5}

# Intersection of two sets
intersection_set = set1.intersection(set2)
print(intersection_set) # Output: {3}

# Difference of two sets
difference_set = set1.difference(set2)
print(difference_set) # Output: {1, 2}

# Symmetric difference of two sets
symmetric_difference_set = set1.symmetric_difference(set2)
print(symmetric_difference_set) # Output: {1, 2, 4, 5}

# Subset and Superset
print(set1.issubset(union_set)) # Output: True
print(union_set.issuperset(set1)) # Output: True

# ---------------------------------------------------


