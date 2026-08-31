# --------------------------------------------------
# Session 2: Introduction to Python
# --------------------------------------------------
## Author: Chandan Chaudhari
## Github: https://github.com/chandanc5525
# --------------------------------------------------

# Asking user for input
name = input("Please enter your name: ")
print(f"Hello, {name}! Welcome to the world of Python programming.")

# --------------------------------------------------

# Concept of Slicing and Indexing in Python with String
string = "Hello, Welcome to the world of Python Programming"

# Indexing
print(string[0])   
print(string[-1])

# Slicing
''' 
string[start:stop:step]
- start: The starting index of the slice (inclusive).
- stop: The ending index of the slice (exclusive).
- step: The step size or the interval between characters in the slice (optional).
'''

print(string[0:5])
print(string[7:14])
print(string[::2])  # Every second character
print(string[::-1]) # Reversed string

# --------------------------------------------------

''' 
Exercise:
[A]. Ask the user to input a string and perform the following operations:
1. Extract the word "Welcome" from the string.
2. Extract the word "Python" from the string.
3. Extract every third character from the string.
4. Reverse the string using slicing.
'''
# --------------------------------------------------

# Boolean Logic and Comparison Operators
a = 10
b = 20
print(a > b)   # output: False
print(a < b)   # output: True
print(a == b)  # output: False
print(a != b)  # output: True
print(a >= b)  # output: False
print(a <= b)  # output: True

# Using and logical operator
print((a > 5) and (b > 15))  # output: True
print((a > 15) and (b > 15)) # output: False

# Using or logical operator
print((a > 5) or (b > 15))   # output: True
print((a > 15) or (b > 15))  # output: True
print((a > 15) or (b > 25))  # output: False

# --------------------------------------------------

# Difference between == and = operator
''' 
=  This is the assignment operator, used to assign a value to a variable.
== This is the equality operator, used to compare two values for equality. 
   It returns True if the values are equal and False otherwise.

'''

x = 10
y = 10
print(x == y)  # output: True
print(x = y)   # output: Error

# --------------------------------------------------
 