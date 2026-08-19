Python Programming — Session 03

---
Table of Contents
Session 02: Control Flow & User Input
Conditional Statements
Comparison Operators
Loops
Loop Control Statements
User Input
Session 03: Data Structures & Reusable Code
Data Structures: Collections
Functions & Reusable Code
Practical Real-World Implementations
Course Summary & Learning Outcomes
---
Session 02: Control Flow & User Input
Control flow statements break step-by-step linear execution, allowing programs to dynamically make decisions and repeat blocks of logic based on state conditions.
Conditional Statements
Python evaluates truthiness to branch execution paths using `if`, `elif`, and `else`.
1. Basic `if` Statement
Executes a block of code only when the specified boolean condition evaluates to `True`.
```python
age = 20

if age >= 18:
    print("You are eligible to vote.")
```
2. Binary Branching `if-else`
Provides an fallback execution path when the primary `if` condition evaluates to `False`.
```python
age = 16

if age >= 18:
    print("You are eligible to vote.")
else:
    print("You are not eligible to vote.")
```
3. Chained Multi-Condition `if-elif-else`
Handles complex, mutually exclusive conditions in sequential order.
```python
marks = 75

if marks >= 90:
    print("Grade A+")
elif marks >= 75:
    print("Grade A")
elif marks >= 60:
    print("Grade B")
elif marks >= 40:
    print("Grade C")
else:
    print("Fail")
```
4. Nested `if` Structures
Embeds conditional evaluations inside existing blocks to enforce granular workflows.
```python
age = 25
has_id = True

if age >= 18:
    if has_id:
        print("Entry allowed.")
    else:
        print("ID required.")
else:
    print("Entry not allowed.")
```
Comparison Operators
Comparison operators act as structural foundations for conditionals, evaluating scalar relationships into precise Booleans (`True` / `False`).
Operator	Meaning	Code Example	Result
`==`	Equal to	`10 == 10`	`True`
`!=`	Not equal to	`10 != 5`	`True`
`>`	Greater than	`10 > 5`	`True`
`<`	Less than	`5 < 10`	`True`
`>=`	Greater than or equal to	`10 >= 10`	`True`
`<=`	Less than or equal to	`5 <= 10`	`True`
---
Loops
Loops allow block repetition without manual duplication of instructions.
1. Fixed Range / Iterable `for` Loop
Ideal for iterating through explicit collections, strings, or programmatic ranges.
```python
# Iterating through arrays/lists
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Iterating over sequence increments
for number in range(1, 6):
    print(number)
```
2. Conditional State `while` Loop
Runs continuously as long as a monitored logical state remains `True`. Ensure state modifiers are embedded to prevent infinite loops.
```python
count = 1

while count <= 5:
    print(count)
    count += 1
```
Loop Control Statements
Fine-tune programmatic execution blocks mid-iteration.
`break`: Immediately halts the loop and drops down to the next un-indented block.
`continue`: Halts the execution of the current iteration and jumps straight to the next loop evaluation.
`pass`: Syntactic placeholder that executes absolute null actions; used to avoid structure errors in empty frames.
---
User Input
Interact dynamically with end-users via the terminal using `input()`. Remember that incoming values default strictly to strings and require explicit type casting.
```python
# String capture
name = input("Enter your name: ")

# Numeric parsing (Integer & Float)
age = int(input("Enter your age: "))
weight = float(input("Enter your weight (kg): "))
```
---
Session 03: Data Structures & Reusable Code
Data collection selection directly governs runtime performance, storage efficiency, and stability.
Data Structures: Collections
Collection	Ordered?	Mutable (Changeable)?	Allows Duplicates?	Basic Syntax
List	Yes	Yes	Yes	`languages = ["Python", "Rust"]`
Tuple	Yes	No	Yes	`coordinates = (40.7128, -74.0060)`
Dictionary	Yes	Yes	No (Keys Only)	`user = {"id": 1, "role": "Admin"}`
Set	No	Yes	No	`unique_ids = {101, 102, 103}`
1. Lists (Dynamic Arrays)
Mutable collections tailored for changing array data.
```python
languages = ["Python", "JavaScript", "C++"]
languages[1] = "TypeScript"  # Modification
languages.append("Rust")      # Dynamic push
languages.insert(1, "Go")     # Element insertion
languages.remove("C++")       # Selective deletion
```
2. Tuples (Fixed Records)
Immutable sequences used to protect historical records or runtime constants from execution side-effects.
```python
pixel_coordinates = (1080, 1920)
# Unpacking structures cleanly
width, height = pixel_coordinates
```
3. Dictionaries (Hash Maps)
Key-value storage offering instantaneous data lookup using explicit indices instead of index parsing.
```python
student_profile = {
    "name": "Alex",
    "course": "Python Basics",
    "completed_sessions": 2
}
# Safe accessing method without risk of unexpected crashes
grade = student_profile.get("grade", "Not Assigned")
```
4. Sets (Unique Tables)
Unordered items guaranteeing complete deduplication with mathematical union/intersection checks.
```python
visitor_ids = {101, 102, 103, 101, 104} # Automatically resolves into {101, 102, 103, 104}
staff_ids = {104, 106, 107}
common_entities = visitor_ids.intersection(staff_ids) # Evaluates to {104}
```
---
Functions & Reusable Code
Functions let programmers aggregate repeating expressions under single logical aliases, adhering strictly to the DRY (Don't Repeat Yourself) engineering paradigm.
```python
def calculate_area(radius):
    """Calculates circular area using geometric parameter bindings."""
    pi = 3.14159
    area = pi * (radius ** 2)
    return area  # Passes the functional calculation back to caller frame

circle_size = calculate_area(5)
```
Scope Resolution Rules
Variables configured inside functions reside entirely within their local stack frameworks. Outside scripts cannot reference local components without explicit bindings or structural parameters.
---
Practical Real-World Implementations
Practical Example 1: Terminal Calculator
```python
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

print("Addition:", num1 + num2)
print("Subtraction:", num1 - num2)
print("Multiplication:", num1 * num2)
print("Division:", num1 / num2 if num2 != 0 else "Undefined (Div by Zero)")
```
Practical Example 2: Inventory Warehouse Application
```python
inventory = [
    {"name": "Laptop", "stock": 15, "price": 899.99},
    {"name": "Mouse", "stock": 50, "price": 25.00},
    {"name": "Monitor", "stock": 8, "price": 249.99}
]

def display_inventory():
    print("\n--- Current Inventory Status ---")
    for item in inventory:
        print(f"Product: {item['name']} | Stock: {item['stock']} | Price: ${item['price']}")

def restock_item(product_name, amount):
    for item in inventory:
        if item["name"].lower() == product_name.lower():
            item["stock"] += amount
            print(f"\nUpdated! New {item['name']} stock count: {item['stock']}")")
            return
    print(f"\nProduct '{product_name}' not found.")

display_inventory()
restock_item("Monitor", 5)
```
---
🎯 Course Summary & Learning Outcomes
By executing these modules, you are trained to:
Incorporate flexible control flow architectures via dynamic conditions.
Manipulate processing loops seamlessly using targeted loop control directives.
Abstract multi-layered functional tracking tools using lists, dictionaries, tuples, and sets based on optimization guidelines.
Enforce structured functional boundaries to compose clean, maintainable, modular software codebases.
