# --------------------------------------------------
# Session 3: Introduction to Python
# --------------------------------------------------
## Author: Chandan Chaudhari
## Github: https://github.com/chandanc5525
# --------------------------------------------------

# List in Python Programming

''' 
List: List is a built-in data structure in Python that represents an ordered collection of items.
Lists are mutable, meaning you can modify their contents after creation. 
They can contain elements of different data types, including integers, floats, strings, and even other lists.
Lists are defined using square brackets [] and elements are separated by commas.
Example:
my_list = [1, 2, 3, "Hello", 4.5, [5, 6]]

'''

lst = [1, 2, 3, 4, 5]
print(lst)

# Accessing elements in a list
print(lst[0])  # First element
print(lst[2])  # Third element  
print(lst[-1]) # Last element

# --------------------------------------------------

# List Methods are as follows:

# Modifying elements in a list
lst[1] = 20
print(lst) # Output: [1, 20, 3, 4, 5]

# Adding elements to a list
lst.append(6)  # Adds 6 to the end of the list
print(lst) # Output: [1, 20, 3, 4, 5, 6]

lst.insert(2, 15)  # Inserts 15 at index 2
print(lst) # Output: [1, 20, 15, 3, 4, 5, 6]

# Removing elements from a list
lst.remove(20)  # Removes the first occurrence of 20
print(lst) # Output: [1, 15, 3, 4, 5, 6]

lst.pop(2)  # Removes the element at index 2
print(lst) # Output: [1, 15, 4, 5, 6]

lst.count(5)  # Counts the number of occurrences of 5 in the list
print(lst.count(5)) # Output: 1

lst.sort()  # Sorts the list in ascending order
print(lst) # Output: [1, 4, 5, 6, 15]

lst.reverse()  # Reverses the order of the list
print(lst) # Output: [15, 6, 5, 4, 1]   


# --------------------------------------------------

# List Indexing and Slicing
my_list = [10, 20, 30, 40, 50]

# Indexing
print(my_list[0])  # Output: 10
print(my_list[-1]) # Output: 50
print(my_list[::1]) # Output: [10, 20, 30, 40, 50]
print(my_list[::2]) # Output: [10, 30, 50]
print(my_list[::-1]) # Output: [50, 40, 30, 20, 10]

# Slicing
print(my_list[1:4])  # Output: [20, 30, 40]
print(my_list[:3])   # Output: [10, 20, 30]
print(my_list[2:5])   # Output: [30, 40, 50]


# --------------------------------------------------

'''
# Exercise:

1. Create a list of your favorite fruits and perform the following operations:
1. Add a new fruit to the list.
2. Remove a fruit from the list.
3. Sort the list in alphabetical order.
4. Reverse the order of the list.
5. Count how many times a specific fruit appears in the list.
6. Extract a sublist of the first three fruits in the list.
7. Extract every second fruit from the list.
8. Reverse the list using slicing.

'''
# --------------------------------------------------

# List Comprehension in Python

''' 
Why use List Comprehension?
1. Conciseness: List comprehensions allow you to create lists in a single line of code, making it more concise and easier to read.
2. Readability: Many developers find list comprehensions more readable than traditional loops for creating lists
3. Performance: List comprehensions can be faster than using loops to create lists, especially for large datasets, because they are optimized in Python.
4. Flexibility: List comprehensions can include conditions and nested loops, allowing for more complex list creation in a clear and concise manner.
5. Functional Programming: List comprehensions align well with functional programming paradigms, allowing you to create new lists based on existing iterables in a more declarative way.
Example:
squares = [x**2 for x in range(10)]

'''

# Example of List Comprehension
squares = [x**2 for x in range(10)]
print(squares) # Output: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# List Comprehension with condition
even_squares = [x**2 for x in range(10) if x % 2 == 0]
print(even_squares) # Output: [0, 4, 16, 36, 64]

# Nested List Comprehension
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(flattened) # Output: [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Segregating even and odd numbers using list comprehension
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
even_numbers = [num for num in numbers if num % 2 == 0]
odd_numbers = [num for num in numbers if num % 2 != 0]
print("Even numbers:", even_numbers) # Output: Even numbers: [2, 4, 6, 8]
print("Odd numbers:", odd_numbers)   # Output: Odd numbers: [1, 3, 5, 7, 9]


# --------------------------------------------------

# Latency comparison between list comprehension and traditional loop
import time
# Using traditional loop
start_time = time.time()
squares_loop = []
for x in range(1000000):
    squares_loop.append(x**2)
    end_time = time.time()

print("Time taken using loop:", end_time - start_time)

# Output: Time taken using loop: 0.2002406120300293

# Using list comprehension
start_time = time.time()
squares_comprehension = [x**2 for x in range(1000000)]
end_time = time.time()
print("Time taken using list comprehension:", end_time - start_time)

# Output: Time taken using list comprehension: 0.0676877498626709


# --------------------------------------------------