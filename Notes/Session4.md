# Python Programming — Part 3

This part continues the Python programming series after **data types, data structures, operators, conditional statements, loops, and user input**.

The focus of this part is on **strings, collection operations, functions, and reusable code**.

---

## Table of Contents

- [Strings](#strings)
- [Lists](#lists)
- [Tuples](#tuples)
- [Dictionaries](#dictionaries)
- [Sets](#sets)
- [Functions](#functions)
- [Practical Examples](#practical-examples)
- [Practice Programs](#practice-programs)
- [Summary](#summary)
- [Learning Outcome](#learning-outcome)

---

## Strings

A string is a sequence of characters enclosed within single quotes, double quotes, or triple quotes.

```python
name = "Python"
message = 'Welcome to Python programming'

print(name)
print(message)
```

### Creating Strings

```python
single_quote = 'Hello'
double_quote = "Hello"
multi_line = """This is
a multi-line
string."""
```

### String Indexing

Python uses zero-based indexing.

```python
language = "Python"

print(language[0])   # P
print(language[1])   # y
print(language[-1])  # n
```

### String Slicing

```python
language = "Python"

print(language[0:3])  # Pyt
print(language[2:6])  # thon
print(language[:4])   # Pyth
print(language[2:])   # thon
print(language[::-1]) # nohtyP
```

### Common String Methods

| Method | Purpose | Example |
|---|---|---|
| `upper()` | Converts text to uppercase | `"python".upper()` |
| `lower()` | Converts text to lowercase | `"PYTHON".lower()` |
| `strip()` | Removes leading/trailing spaces | `" hello ".strip()` |
| `replace()` | Replaces text | `"hello".replace("h", "H")` |
| `split()` | Splits text into a list | `"a,b,c".split(",")` |
| `find()` | Finds the position of text | `"Python".find("t")` |
| `count()` | Counts occurrences | `"banana".count("a")` |
| `startswith()` | Checks starting text | `"Python".startswith("Py")` |
| `endswith()` | Checks ending text | `"Python".endswith("on")` |

```python
text = "  Python Programming  "

print(text.upper())
print(text.lower())
print(text.strip())
print(text.replace("Python", "Java"))
```

---

## Lists

A list is an ordered and mutable collection that can contain duplicate elements.

```python
fruits = ["apple", "banana", "cherry"]

print(fruits)
print(fruits[0])
```

### Accessing List Elements

```python
numbers = [10, 20, 30, 40, 50]

print(numbers[0])   # 10
print(numbers[-1])  # 50
```

### List Methods

| Method | Purpose |
|---|---|
| `append()` | Adds an item to the end |
| `insert()` | Adds an item at a specific position |
| `extend()` | Adds multiple items |
| `remove()` | Removes a specific item |
| `pop()` | Removes an item |
| `sort()` | Sorts the list |
| `reverse()` | Reverses the list |
| `clear()` | Removes all elements |

```python
numbers = [30, 10, 20]

numbers.append(40)
numbers.insert(0, 5)
numbers.remove(10)
numbers.sort()

print(numbers)
```

### List Slicing

```python
numbers = [10, 20, 30, 40, 50]

print(numbers[0:3])
print(numbers[2:])
print(numbers[:3])
print(numbers[::-1])
```

---

## Tuples

A tuple is an ordered and immutable collection.

```python
coordinates = (10, 20)

print(coordinates[0])
print(coordinates[1])
```

Tuple elements cannot be changed after creation.

```python
numbers = (10, 20, 30)

# numbers[0] = 100  # TypeError
```

### Tuple Methods

```python
numbers = (10, 20, 20, 30)

print(numbers.count(20))
print(numbers.index(30))
```

---

## Dictionaries

A dictionary stores data in **key-value pairs**.

```python
student = {
    "name": "Alice",
    "age": 21,
    "course": "Python"
}

print(student)
```

### Accessing Dictionary Values

```python
print(student["name"])
print(student["age"])
print(student.get("course"))
```

### Dictionary Methods

| Method | Purpose |
|---|---|
| `keys()` | Returns all keys |
| `values()` | Returns all values |
| `items()` | Returns key-value pairs |
| `get()` | Retrieves a value safely |
| `update()` | Adds or updates values |
| `pop()` | Removes a key-value pair |
| `clear()` | Removes all elements |

```python
student["city"] = "Mumbai"

print(student.keys())
print(student.values())
print(student.items())
```

---

## Sets

A set is an unordered collection of unique elements.

```python
numbers = {1, 2, 3, 3, 4}

print(numbers)
```

Duplicate values are automatically removed.

### Set Operations

#### Union

```python
set_a = {1, 2, 3}
set_b = {3, 4, 5}

print(set_a.union(set_b))
```

#### Intersection

```python
print(set_a.intersection(set_b))
```

#### Difference

```python
print(set_a.difference(set_b))
```

#### Symmetric Difference

```python
print(set_a.symmetric_difference(set_b))
```

---

## Functions

A function is a reusable block of code designed to perform a specific task.

Functions help make programs more reusable, organized, and maintainable.

### Creating a Function

```python
def greet():
    print("Welcome to Python programming!")

greet()
```

### Function Arguments

```python
def greet(name):
    print("Hello", name)

greet("Alice")
greet("Bob")
```

### Multiple Arguments

```python
def add(a, b):
    print(a + b)

add(10, 20)
```

### Return Statement

The `return` statement sends a result back to the calling code.

```python
def add(a, b):
    return a + b

result = add(10, 20)

print("Result:", result)
```

### Default Arguments

```python
def greet(name="Student"):
    print("Hello", name)

greet()
greet("Alice")
```

### Function with Conditional Logic

```python
def check_number(number):

    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

print(check_number(10))
```

---

## Practical Examples

### 1. Count Characters

```python
def count_characters(text):
    return len(text)

text = input("Enter text: ")

print("Number of characters:", count_characters(text))
```

### 2. Calculate Average

```python
def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)

    return total / count

numbers = [10, 20, 30, 40, 50]

print("Average:", calculate_average(numbers))
```

### 3. Find Largest Number

```python
def find_largest(numbers):
    return max(numbers)

numbers = [10, 45, 23, 67, 12]

print("Largest:", find_largest(numbers))
```

### 4. Student Result

```python
def calculate_grade(marks):

    if marks >= 90:
        return "A+"
    elif marks >= 75:
        return "A"
    elif marks >= 60:
        return "B"
    elif marks >= 40:
        return "C"
    else:
        return "Fail"

marks = float(input("Enter marks: "))

print("Grade:", calculate_grade(marks))
```

---

## Practice Programs

### 1. Reverse a String

```python
def reverse_string(text):
    return text[::-1]

print(reverse_string("Python"))
```

### 2. Count Vowels

```python
def count_vowels(text):

    count = 0

    for char in text.lower():
        if char in "aeiou":
            count += 1

    return count

print(count_vowels("Python Programming"))
```

### 3. Remove Duplicates

```python
numbers = [1, 2, 2, 3, 4, 4, 5]

unique_numbers = list(set(numbers))

print(unique_numbers)
```

### 4. Find Even Numbers

```python
def find_even_numbers(numbers):

    result = []

    for number in numbers:
        if number % 2 == 0:
            result.append(number)

    return result

numbers = [1, 2, 3, 4, 5, 6, 7, 8]

print(find_even_numbers(numbers))
```

---

## Summary

In Part 3, we covered:

- **Strings** — Creating, indexing, slicing, and manipulating strings
- **String Methods** — `upper()`, `lower()`, `strip()`, `replace()`, `split()`, and more
- **Lists** — Accessing, modifying, slicing, and using list methods
- **Tuples** — Working with immutable collections
- **Dictionaries** — Managing key-value data
- **Sets** — Storing unique values and performing set operations
- **Functions** — Creating reusable blocks of code
- **Arguments** — Passing data into functions
- **Return Values** — Returning results from functions
- **Practical Programs** — Applying Python fundamentals to programming problems

---

## Learning Outcome

After completing Part 3, learners should be able to:

1. Manipulate strings using indexing, slicing, and built-in methods.
2. Perform common operations on lists, tuples, dictionaries, and sets.
3. Choose an appropriate data structure for a programming task.
4. Create reusable functions using `def`.
5. Pass arguments to functions.
6. Return values from functions.
7. Use functions together with conditions and loops.
8. Build small Python programs using multiple concepts together.

---

## Next Part

The next part can cover:

- List, set, and dictionary comprehensions
- Lambda functions
- `map()`, `filter()`, and `reduce()`
- `*args` and `**kwargs`
- Modules and packages
- Exception handling
- File handling
- Working with CSV and JSON files
