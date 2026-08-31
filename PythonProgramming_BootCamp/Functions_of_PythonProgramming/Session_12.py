# --------------------------------------------------
# Session 12: Functions of Python Programming
# --------------------------------------------------
## Author: Chandan Chaudhari
## Github: https://github.com/chandanc5525
# --------------------------------------------------

# Concept of def(): 

def greeting(): # Function Definition
    print("Hello, welcome to the world of Python Programming!")
    
greeting() # Function Calling

''' 
Output:
Hello, welcome to the world of Python Programming!
'''



# ------------------------------------------------------------
# Function with parameters:
def greet(name): # Function Definition with parameter
    print(f"Hello, {name}! Welcome to the world of Python Programming!")
    
greet("Chandan") # Function Calling with argument

''' 
Output:
Hello, Chandan! Welcome to the world of Python Programming!
'''

# ------------------------------------------------------------

# Function with return statement:
def add(a, b): # Function Definition with parameters
    return a + b # Return statement

result = add(5, 3) # Function Calling with arguments and storing the result
print(f"The sum of 5 and 3 is: {result}") # Output the result

''' 
Output:
The sum of 5 and 3 is: 8
'''
# ------------------------------------------------------------

# Function with default parameters:
def greet(name="Guest"): # Function Definition with default parameter
    print(f"Hello, {name}! Welcome to the world of Python Programming!")
    
greet() # Function Calling without argument, will use default value

'''
Output:
Hello, Guest! Welcome to the world of Python Programming!
'''

# ------------------------------------------------------------

# Example of a function that calculates the factorial of a number:
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)
    
number = 5
result = factorial(number)
print(f"The factorial of {number} is: {result}")

'''
Output:
The factorial of 5 is: 120
'''

# ------------------------------------------------------------

# Example of a function that checks if a number is prime:
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True
number = 17
if is_prime(number):
    print(f"{number} is a prime number.")
    
'''
Output:
17 is a prime number.
'''

# ------------------------------------------------------------

# Example of a function that generates Fibonacci sequence up to n terms:
def fibonacci(n):
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

terms = 10
fib_sequence = fibonacci(terms)

print(f"Fibonacci sequence up to {terms} terms: {fib_sequence}")

'''
Output:
Fibonacci sequence up to 10 terms: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
'''

# ------------------------------------------------------------

# Example of a function that calculates the number is armstrong number

def is_armstrong(num):
    order = len(str(num))
    sum_of_digits = sum(int(digit) ** order for digit in str(num))
    return num == sum_of_digits

number = 153
if is_armstrong(number):
    print(f"{number} is an Armstrong number.")
    
'''
Output:
153 is an Armstrong number.
'''

# ------------------------------------------------------------

# Example of indian railway reservation system using functions:

def book_ticket(name, age, destination):
    print(f"Booking ticket for {name}, Age: {age}, Destination: {destination}")
    print("Ticket booked successfully!")
# Booking a ticket
book_ticket("Chandan", 25, "Mumbai")

'''
Output:
Booking ticket for Chandan, Age: 25, Destination: Mumbai
Ticket booked successfully!
'''

# ------------------------------------------------------------

# Concept of lambda function:

''' 
Lambda functions are anonymous functions that can have any number of arguments but only one expression. 
They are often used for short, throwaway functions that are not reused elsewhere in the code. 
The syntax for a lambda function is:

lambda arguments: expression

Example: 

x = lambda a, b: a + b
print(x(5, 3)) 

Output: 8

'''

# Comparison of regular function and lambda function:

''' 
# Comparison of regular function and lambda function based on latency:

'''

# %%
import time
# Regular function
def add(a, b):
    return a + b

start_time = time.time()
result = add(5, 3)
end_time = time.time()
print(f"Result of regular function: {result}, Time taken: {end_time - start_time} seconds")

'''
Output:
Result of regular function: 8, Time taken: 1.1920928955078125e-06 seconds
'''


#%%
# Lambda function

start_time = time.time()
add_lambda = lambda a, b: a + b
end_time = time.time()

'''

Output:
Result of lambda function: 8, Time taken: 1.1720928955078125e-06 seconds

'''

# %%

# ------------------------------------------------------------

# Write a function to print the multiplication table of a given number using lambda function

def multiplication_table(n):
    
    table = list(map(lambda x: f"{n} x {x} = {n * x}", range(1, 11)))
    return table

number = 5
result = multiplication_table(number)
print(f"Multiplication table of {number}:")
for line in result:
    print(line)

'''
Output:
Multiplication table of 5:
5 x 1 = 5
5 x 2 = 10
5 x 3 = 15
5 x 4 = 20
5 x 5 = 25
5 x 6 = 30
5 x 7 = 35
5 x 8 = 40
5 x 9 = 45
5 x 10 = 50
'''

# -