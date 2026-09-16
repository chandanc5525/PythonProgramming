# input() — reads user input from the console (always returns a string)
name = input("Enter your name: ")
print("Hello,", name)
print(type(name))  # <class 'str'>

# Cast input to other types when needed
age = int(input("Enter your age: "))
print(f"Next year you'll be {age + 1}")

height = float(input("Enter your height in meters: "))
print(f"Your height: {height}m")

# ── import — bring in modules ──────────────────────────────────
# 1. Import the entire module
import math

print(math.sqrt(16))    # 4.0
print(math.pi)          # 3.14159...
print(math.ceil(4.2))   # 5

# 2. Import specific items from a module
from math import factorial, gcd

print(factorial(5))      # 120
print(gcd(12, 8))        # 4

# 3. Import with an alias for convenience
import random as rnd

print(rnd.randint(1, 100))       # random integer between 1 and 100
print(rnd.choice(["a", "b", "c"]))  # random pick from a list

# 4. Import everything (not recommended — pollutes namespace)
# from math import *

# ── Practical example ──────────────────────────────────────────
import datetime

today = datetime.date.today()
print(f"Today's date: {today}")

birth_year = int(input("Enter your birth year: "))
approx_age = today.year - birth_year
print(f"You are approximately {approx_age} years old")
