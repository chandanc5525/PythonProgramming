# --------------------------------------------------
# Session 6: Introduction to Python
# --------------------------------------------------
## Author: Chandan Chaudhari
## Github: https://github.com/chandanc5525
# --------------------------------------------------

# Dictionary in Python Programming

''' 
Dictionary: A dictionary is a built-in data structure in Python that represents a collection of key-value pairs.
Dictionaries are defined using curly braces {} and consist of keys and their corresponding values.
Dictionaries are mutable, meaning you can add, remove, or modify key-value pairs after creation. They are
commonly used for storing and retrieving data based on unique keys.

Example:

my_dict = {
    "name": "Chandan",
    "age": 30,
    "city": "New York"
}

Here my_dict is a dictionary with three key-value pairs. The keys are "name", "age", and "city", and their
corresponding values are "Chandan", 30, and "New York". You can access the values in the dictionary using their keys, for example, my_dict["name"] will return "Chandan".

'''

# ---------------------------------------------------

my_dict = {
    "name": "Chandan",
    "age": 30,
    "city": "New York"
}

print(my_dict) # Output: {'name': 'Chandan', 'age': 30, 'city': 'New York'}

# Accessing values in a dictionary
print(my_dict["name"]) # Output: Chandan
print(my_dict["age"]) # Output: 30

# Adding a new key-value pair to the dictionary
my_dict["country"] = "USA"
print(my_dict) # Output: {'name': 'Chandan', 'age': 30, 'city': 'New York', 'country': 'USA'}

# Removing a key-value pair from the dictionary
del my_dict["city"]
print(my_dict) # Output: {'name': 'Chandan', 'age': 30, 'country': 'USA'}   

# Checking if a key is in the dictionary
print("name" in my_dict) # Output: True
print("city" in my_dict) # Output: False

# ----------------------------------------------------

# Methods of Dictionary are as follows:

# Get the keys of the dictionary
keys = my_dict.keys()
print(keys) # Output: dict_keys(['name', 'age', 'country'])

# Get the values of the dictionary
values = my_dict.values()
print(values) # Output: dict_values(['Chandan', 30, 'USA'])

# Get the key-value pairs of the dictionary
items = my_dict.items()
print(items) # Output: dict_items([('name', 'Chandan'), ('age', 30), ('country', 'USA')])

# Clear all key-value pairs from the dictionary
my_dict.clear()
print(my_dict) # Output: {}

# Copy a dictionary
my_dict_copy = my_dict.copy()
print(my_dict_copy) # Output: {}

# Update a dictionary with another dictionary
my_dict.update({"name": "Chandan", "age": 30})
print(my_dict) # Output: {'name': 'Chandan', 'age': 30}

# ------------------------------------------------------

# Dictionary Comprehension

# Create a dictionary using dictionary comprehension
squared_dict = {x: x**2 for x in range(1, 6)}
print(squared_dict) # Output: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Create a dictionary from two lists using dictionary comprehension
keys = ['a', 'b', 'c']
values = [1, 2, 3]
my_dict_from_lists = {k: v for k, v in zip(keys, values)}
print(my_dict_from_lists) # Output: {'a': 1, 'b': 2, 'c': 3}

# Create a dictionary with conditional logic using dictionary comprehension
even_squared_dict = {x: x**2 for x in range(1, 11) if x % 2 == 0}
print(even_squared_dict) # Output: {2: 4, 4: 16, 6: 36, 8: 64, 10: 100}

# Create a dictionary with nested dictionary comprehension
nested_dict = {x: {y: y**2 for y in range(1, 4)} for x in range(1, 4)}
print(nested_dict) # Output: {1: {1: 1, 2: 4, 3: 9}, 2: {1: 1, 2: 4, 3: 9}, 3: {1: 1, 2: 4, 3: 9}}

# ------------------------------------------------------
