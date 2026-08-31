# --------------------------------------------------
# Session 1: Introduction to Python
# --------------------------------------------------
## Author: Chandan Chaudhari
## Github: https://github.com/chandanc5525
# --------------------------------------------------

# Data types in Python Programming
''' 
1. Integer (int): Represents whole numbers without a decimal point. Example: 10, -5, 0
2. Float (float): Represents numbers with a decimal point. Example: 3.14
3. String (str): Represents a sequence of characters enclosed in quotes. Example: "Hello", 'Python'
4. Boolean (bool): Represents a value that can be either True or False. Example: True, False
5. List (list): Represents an ordered collection of items, which can be of different types
6. Tuple (tuple): Represents an ordered collection of items, which can be of different types,
   but is immutable (cannot be changed after creation)
7. Dictionary (dict): Represents a collection of key-value pairs, where each key is unique and maps to a value. 
   Example: {"name": "Alice", "age": 30}
8. Set (set): Represents an unordered collection of unique items. Example: {1, 2, 3}

'''
# --------------------------------------------------

# Define various variables in python 
a = 10
b = 20
c = 100.456
str = "Hello World"

# Print the variables
print(a)
print(b)
print(c)
print(str)

# Define multiples variables in one line
x, y, z = 1, 2, 3
print(x)
print(y)
print(z)


# --------------------------------------------------

# Math operations
sum = a + b
diff = a - b
product = a * b
quotient = a / b
modulo = a % b

print("Sum:", sum)
print("Difference:", diff)
print("Product:", product)
print("Quotient:", quotient)
print("Modulo:", modulo)

# BODMAS rule
result = (a + b) * c / x - y
print("Result of BODMAS operation:", result)
# %%

# --------------------------------------------------

# Define String and perform various operations
str1 = "Hello"
str2 = "World"

# Checking Data type of the string
print("Data type of str1:", type(str1))

# Checking the length of the string
print("Length of str1:", len(str1))


# Concatenation
greeting = str1 + " " + str2
print(greeting)

#%%
# Methods of string
print(greeting.upper())  # Convert to uppercase
print(greeting.lower())  # Convert to lowercase
print(greeting.split())  # Split the string into a list
print(greeting.replace("World", "Python"))  # Replace a substring

# --------------------------------------------------

# Concept of f-string and format method
name = "Chandan Chaudhari"
age = 39

# Using f-string
print(f"My name is {name} and I am {age} years old.")

# Using format method
print("My name is {} and I am {} years old.".format(name, age))

# --------------------------------------------------