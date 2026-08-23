# --------------------------------------------------
# Session 10: Fundamentals of Python Programming
# --------------------------------------------------
## Author: Chandan Chaudhari
## Github: https://github.com/chandanc5525
# --------------------------------------------------

# Enumerate Function in Python Programming

''' 
What is Enumerate Function in Python Programming?

The enumerate() function in Python is a built-in function that adds a counter to an iterable and returns it as an enumerate object. This is particularly useful when you need to loop through an iterable and also need to keep track of the index of the current item.

The syntax of the enumerate() function is as follows:

enumerate(iterable, start=0)

- iterable: This is the collection of items that you want to loop through. It can be a list, tuple, string, or any other iterable object.
- start: This is an optional parameter that specifies the starting index for the counter. By default
, it starts at 0. You can set it to any integer value if you want the counter to start from a different number.
The enumerate() function returns an enumerate object, which is an iterator that produces pairs of index and value from the iterable. You can convert this object into a list or use it directly in a loop.

'''

# ---------------------------------------------------
names = ['chandan', 'anjali', 'rohit', 'priya', 'sneha']

for index, name in enumerate(names):
    print(f"Index: {index}, Name: {name}")
    
'''
Output:
Index: 0, Name: chandan
Index: 1, Name: anjali
Index: 2, Name: rohit
Index: 3, Name: priya
Index: 4, Name: sneha
'''

# --------------------------------------------------

tickets = [
    ("Amit", 25, "S1-23"),
    ("Neha", 22, "S1-24"),
    ("Rahul", 30, "S1-25")
]

for i, t in enumerate(tickets, start=1):
    print(f"{i}. Name: {t[0]}, Age: {t[1]}, Seat: {t[2]}")
    
'''
Output:
1. Name: Amit, Age: 25, Seat: S1-23
2. Name: Neha, Age: 22, Seat: S1-24
3. Name: Rahul, Age: 30, Seat: S1-25
'''

# --------------------------------------------------

names = ["Amit", "Neha", "Rahul","Chandan", "Anjali"]
ages = [25, 22, 30, 25, 22]
seats = ["S1-23", "S1-24", "S1-25", "S1-26", "S1-27"]

for i, (name, age, seat) in enumerate(zip(names, ages, seats), start=1):
    print(f"{i}. {name} | {age} | {seat}")
    
'''
Output:
1. Amit | 25 | S1-23
2. Neha | 22 | S1-24
3. Rahul | 30 | S1-25
4. Chandan | 25 | S1-26
5. Anjali | 22 | S1-27
'''

# --------------------------------------------------