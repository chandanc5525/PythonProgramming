# Python Programming — Session 01

---

## Table of Contents

- [Overview](#overview)
- [Data Types](#data-types-of-python-programming)
- [Data Structures](#data-structures-of-python-programming)
- [Mathematical Operators](#mathematical-operators-in-python-programming)
- [Logical Operators](#logical-operators-in-python-programming)
- [Getting Started](#getting-started)
- [Summary](#summary)

---

## Overview

Python is a high-level, interpreted, dynamically typed, and object-oriented programming language known for its clear syntax and readability.

Python is widely used in:

- **Data Science & AI** — Machine learning, data analysis, and visualization
- **Web Development** — Backend application development
- **Automation & Scripting** — Task automation and workflow processing
- **Software Engineering** — Application development, testing, and integration

---

## Data Types of Python Programming

Python provides built-in data types for storing and manipulating different forms of information.

### 1. Numeric Types

#### `int` — Integer

Represents positive or negative whole numbers without decimal values.

```python
age = 25
```

#### `float` — Floating Point

Represents numbers containing decimal values.

```python
price = 19.99
```

#### `complex` — Complex Number

Represents numbers with real and imaginary components.

```python
z = 3 + 5j
```

### 2. Text Type

#### `str` — String

Represents a sequence of characters enclosed within single, double, or triple quotes.

```python
name = "Python"
```

### 3. Boolean Type

#### `bool` — Boolean

Represents logical values: `True` or `False`.

```python
is_active = True
```

### 4. Type Conversion (Casting)

Python provides built-in functions to convert values between basic data types.

```python
x = int(3.14)   # Converts float to int -> 3
y = str(100)    # Converts int to string -> '100'
z = float("5")  # Converts string to float -> 5.0
```

---

## Data Structures of Python Programming

Data structures allow you to store, organize, and manage collections of data efficiently.

| Data Structure | Ordered | Mutable | Duplicates Allowed | Primary Use Case |
|---|:---:|:---:|:---:|---|
| **List** | Yes | Yes | Yes | General-purpose sequential storage |
| **Tuple** | Yes | No | Yes | Fixed/immutable sequential storage |
| **Dictionary (`dict`)** | Yes* | Yes | Keys: No / Values: Yes | Key-value mapping |
| **Set** | No | Yes | No | Unique elements and set operations |

> *Dictionaries maintain insertion order in Python 3.7+.*

### Usage Examples

```python
# 1. List
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")
print(fruits[0])  # Output: apple

# 2. Tuple
coordinates = (10.0, 20.0)

# 3. Dictionary
student = {
    "name": "Alice",
    "age": 21,
    "major": "Computer Science"
}

print(student["name"])  # Output: Alice

# 4. Set
unique_numbers = {1, 2, 3, 3, 4}
print(unique_numbers)  # Output: {1, 2, 3, 4}
```

---

## Mathematical Operators in Python Programming

Mathematical or arithmetic operators perform calculations on numeric values.

| Operator | Name | Description | Example (`a = 10, b = 3`) | Result |
|:---:|---|---|---|:---:|
| `+` | Addition | Adds two values | `a + b` | `13` |
| `-` | Subtraction | Subtracts the right operand from the left | `a - b` | `7` |
| `*` | Multiplication | Multiplies two values | `a * b` | `30` |
| `/` | Division | Divides the left operand by the right and returns a float | `a / b` | `3.3333...` |
| `%` | Modulus | Returns the remainder | `a % b` | `1` |
| `**` | Exponentiation | Calculates a power | `a ** b` | `1000` |
| `//` | Floor Division | Divides and rounds down | `a // b` | `3` |

### Code Example

```python
x = 15
y = 4

print("Addition:", x + y)         # Output: 19
print("Division:", x / y)         # Output: 3.75
print("Floor Division:", x // y)  # Output: 3
print("Modulus:", x % y)          # Output: 3
print("Exponent:", x ** y)        # Output: 50625
```

---

## Logical Operators in Python Programming

Logical operators combine conditional expressions and evaluate them as Boolean values (`True` or `False`).

| Operator | Description | Example | Result |
|:---:|---|---|:---:|
| `and` | Returns `True` when both conditions are true | `(5 > 3) and (10 > 5)` | `True` |
| `or` | Returns `True` when at least one condition is true | `(5 > 3) or (10 < 5)` | `True` |
| `not` | Reverses the logical result | `not(5 > 3)` | `False` |

### Truth Tables

#### `and`

| Condition 1 | Condition 2 | Result |
|:---:|:---:|:---:|
| True | True | True |
| True | False | False |
| False | False | False |

#### `or`

| Condition 1 | Condition 2 | Result |
|:---:|:---:|:---:|
| True | False | True |
| False | False | False |

#### `not`

| Condition | Result |
|:---:|:---:|
| True | False |
| False | True |

### Code Example

```python
age = 20
has_license = True

# Logical AND
can_drive = (age >= 18) and has_license
print("Can drive:", can_drive)  # Output: True

# Logical OR
is_student = False
has_discount = is_student or (age < 21)
print("Has discount:", has_discount)  # Output: True

# Logical NOT
is_logged_in = False

if not is_logged_in:
    print("Please log in to continue.")
```

---

## Getting Started

### Prerequisites

Install **Python 3.8 or later**.

Check your installed Python version:

```bash
python --version
```

### Execution

After downloading or cloning the repository, run a Python script using:

```bash
python main.py
```

---

## Summary

This guide covers the following Python fundamentals:

- **Data Types** — `int`, `float`, `complex`, `str`, and `bool`
- **Type Conversion** — Converting values using `int()`, `float()`, and `str()`
- **Data Structures** — `list`, `tuple`, `dict`, and `set`
- **Mathematical Operators** — `+`, `-`, `*`, `/`, `%`, `**`, and `//`
- **Logical Operators** — `and`, `or`, and `not`
- **Python Execution** — Checking the Python version and running Python scripts

---

## Learning Outcome

After completing this guide, learners should be able to:

1. Identify and use common Python data types.
2. Work with fundamental Python data structures.
3. Perform arithmetic calculations using Python operators.
4. Apply logical operators to evaluate conditions.
5. Perform basic type conversion.
6. Execute Python programs from the command line.
