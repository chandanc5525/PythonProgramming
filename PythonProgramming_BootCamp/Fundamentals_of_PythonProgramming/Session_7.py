# --------------------------------------------------
# Session 7: Fundamentals of Python Programming
# --------------------------------------------------
## Author: Chandan Chaudhari
## Github: https://github.com/chandanc5525
# --------------------------------------------------

# If statement
x = 10
if x > 5:
    print("x is greater than 5")
    
# If-else statement
y = 3
if y % 2 == 0:
    print("y is even")
else:
    print("y is odd")
    
# Elif statement
z = 15
if z < 10:
    print("z is less than 10")  
elif z == 10:
    print("z is equal to 10")
else:    
    print("z is greater than 10")
    
# Nested if statement
a = 20
if a > 10:
    if a < 30:
        print("a is between 10 and 30")
    else:
        print("a is greater than or equal to 30")
else:    
    print("a is less than or equal to 10")
    
# --------------------------------------------------


''' 
Exercise:
A company gives bonus based on salary:

Salary > 50,000 → Bonus = 20%
Salary between 30,000–50,000 → Bonus = 10%
Salary < 30,000 → Bonus = 5%

Write a program to calculate and print the bonus.
'''

salary = float(input("Enter your salary: "))

if salary > 50000:
    bonus = salary * 0.20
    print(f"Your bonus is: {bonus}")
elif salary >= 30000:
    bonus = salary * 0.10
    print(f"Your bonus is: {bonus}")
else:
    bonus = salary * 0.05
    print(f"Your bonus is: {bonus}")

# --------------------------------------------------

# While loop
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1

# Output:   # Count: 0
#           # Count: 1  
#           # Count: 2
#           # Count: 3
#           # Count: 4
    
# --------------------------------------------------

# For loop
for i in range(5):
    print(f"i: {i}")
        
# Output:   # i: 0
#           # i: 1
#           # i: 2
#           # i: 3
#           # i: 4

# --------------------------------------------------

# For loop with list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"Fruit: {fruit}")    

# Output:   # Fruit: apple
#           # Fruit: banana 
#           # Fruit: cherry

# --------------------------------------------------

# For loop with dictionary

person = {"name": "Chandan", "age": 30, "city": "NewYork"},
for key, value in person.items():  # Note: This Concept is also called as Destructuring in Python Programming
    print(f"{key}: {value}")
    
# Output:   # name: Chandan
#           # age: 30
#           # city: NewYork

# --------------------------------------------------

# for loop with string
name = "Chandan"
for char in name:
    print(f"Character: {char}")
    
# Output:   # Character: C
#           # Character: h  
#           # Character: a
#           # Character: n
#           # Character: d
#           # Character: a
#           # Character: n

# --------------------------------------------------

# for loop with range and step
# range(start, stop, step)
for i in range(0, 10, 2):
    print(f"i: {i}")
    
# Output:   # i: 0
#           # i: 2
#           # i: 4
#           # i: 6
#           # i: 8

# --------------------------------------------------

''' 
Exercise:
Write a program to ask user to enter a string and print the number of vowels in the string.
'''

string = input("Enter a string: ")
vowels = "aeiouAEIOU"
count = 0
for char in string:
    if char in vowels:
        count += 1
print(f"Number of vowels in the string: {count}")

# output:   # Enter a string: Hello World
#           # Number of vowels in the string: 3

# --------------------------------------------------

'''
Exercise:
Write a program to ask user to enter a string and check repeated characters in the string. 
If there are repeated characters, print the character and its count.
'''

string1 = input("Enter a string: ")
char_count = {}
for char in string1:
    if char in char_count:
        char_count[char] += 1
    else:
        char_count[char] = 1
for char, count in char_count.items():
    if count > 1:
        print(f"Character: {char}, Count: {count}")
        
# output:   # Enter a string: Hello World
#           # Character: l, Count: 3

# --------------------------------------------------

