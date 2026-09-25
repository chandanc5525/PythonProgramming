# ── help() — displays full documentation ──────────────────────
# Uncomment any of these to see the docs in your terminal:
# help(print)
# help(str.upper)
# help(list)

# ── dir() — lists all attributes and methods ──────────────────
# Shows every method available on a string
print("String methods:")
print(dir("hello"))
print()

# Filter out dunder methods for a cleaner view
print("Public string methods:")
public_methods = [m for m in dir("hello") if not m.startswith("_")]
print(public_methods)
print()

# Works on any object — lists, dicts, modules
import math
print("Math module contents:")
print([m for m in dir(math) if not m.startswith("_")])
print()

# ── type() — check the type of any object ────────────────────
print(type(42))           # <class 'int'>
print(type(3.14))         # <class 'float'>
print(type("hello"))      # <class 'str'>
print(type([1, 2, 3]))    # <class 'list'>
print(type(len))          # <class 'builtin_function_or_method'>
print()

# ── Docstrings (__doc__) ──────────────────────────────────────
def calculate_bmi(weight_kg, height_m):
    """
    Calculate Body Mass Index (BMI).

    Parameters:
        weight_kg (float): Weight in kilograms
        height_m  (float): Height in meters

    Returns:
        float: The BMI value
    """
    return weight_kg / (height_m ** 2)

# Access the docstring directly
print(calculate_bmi.__doc__)

# Or use help() to see it formatted
# help(calculate_bmi)

# Try it out
bmi = calculate_bmi(70, 1.75)
print(f"BMI: {bmi:.1f}")  # BMI: 22.9

# ── isinstance() — check if an object is of a certain type ───
print(isinstance(42, int))          # True
print(isinstance("hi", str))        # True
print(isinstance(3.14, (int, float)))  # True (checks multiple types)
