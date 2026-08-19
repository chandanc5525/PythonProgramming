# Python Programming — Session 02



---

## Table of Contents

- [Conditional Statements](#conditional-statements)
  - [if Statement](#1-if-statement)
  - [if-else Statement](#2-if-else-statement)
  - [if-elif-else Statement](#3-if-elif-else-statement)
  - [Nested if Statement](#4-nested-if-statement)
- [Comparison Operators](#comparison-operators)
- [Loops](#loops)
  - [for Loop](#1-for-loop)
  - [while Loop](#2-while-loop)
- [Loop Control Statements](#loop-control-statements)
  - [break](#break)
  - [continue](#continue)
  - [pass](#pass)
- [User Input](#user-input)
- [Practical Example](#practical-example)
- [Summary](#summary)
- [Learning Outcome](#learning-outcome)

---

## Conditional Statements

Conditional statements allow a program to make decisions based on whether a condition evaluates to `True` or `False`.

Python commonly uses:

- `if`
- `if-else`
- `if-elif-else`
- Nested `if`

### 1. `if` Statement

The `if` statement executes a block of code only when a specified condition is true.

```python
age = 20

if age >= 18:
    print("You are eligible to vote.")
```

### 2. `if-else` Statement

The `else` block executes when the `if` condition is false.

```python
age = 16

if age >= 18:
    print("You are eligible to vote.")
else:
    print("You are not eligible to vote.")
```

### 3. `if-elif-else` Statement

Use `elif` when multiple conditions need to be checked.

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

### 4. Nested `if` Statement

An `if` statement can be placed inside another `if` statement.

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

---

## Comparison Operators

Comparison operators compare two values and return a Boolean result: `True` or `False`.

| Operator | Meaning | Example | Result |
|:---:|---|---|:---:|
| `==` | Equal to | `10 == 10` | `True` |
| `!=` | Not equal to | `10 != 5` | `True` |
| `>` | Greater than | `10 > 5` | `True` |
| `<` | Less than | `5 < 10` | `True` |
| `>=` | Greater than or equal to | `10 >= 10` | `True` |
| `<=` | Less than or equal to | `5 <= 10` | `True` |

### Example

```python
a = 10
b = 5

print(a == b)
print(a != b)
print(a > b)
print(a < b)
print(a >= b)
print(a <= b)
```

---

## Loops

Loops are used to execute a block of code repeatedly.

Python provides two primary loops:

1. `for` loop
2. `while` loop

---

## 1. `for` Loop

A `for` loop is commonly used to iterate over a sequence such as a list, tuple, string, or range.

### Example with a List

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)
```

### Example with `range()`

```python
for number in range(1, 6):
    print(number)
```

**Output:**

```text
1
2
3
4
5
```

### Example: Calculate a Sum

```python
total = 0

for number in range(1, 6):
    total = total + number

print("Total:", total)
```

---

## 2. `while` Loop

A `while` loop repeatedly executes a block of code as long as its condition remains true.

```python
count = 1

while count <= 5:
    print(count)
    count += 1
```

**Output:**

```text
1
2
3
4
5
```

> **Important:** Make sure the condition of a `while` loop eventually becomes false. Otherwise, the program may run indefinitely.

---

## Loop Control Statements

Python provides special statements to control the execution of loops.

### `break`

The `break` statement immediately terminates the loop.

```python
for number in range(1, 11):

    if number == 6:
        break

    print(number)
```

**Output:**

```text
1
2
3
4
5
```

---

### `continue`

The `continue` statement skips the current iteration and moves to the next iteration.

```python
for number in range(1, 6):

    if number == 3:
        continue

    print(number)
```

**Output:**

```text
1
2
4
5
```

---

### `pass`

The `pass` statement does nothing. It is useful as a placeholder when a statement is syntactically required but no action is needed yet.

```python
for number in range(1, 6):

    if number == 3:
        pass

    print(number)
```

---

## User Input

The `input()` function allows a Python program to receive information from the user.

```python
name = input("Enter your name: ")

print("Hello", name)
```

### Numeric Input

By default, `input()` returns a string. Convert the input when a numeric value is required.

```python
age = int(input("Enter your age: "))

print("Your age is:", age)
```

### Example: Simple Calculator

```python
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

print("Addition:", num1 + num2)
print("Subtraction:", num1 - num2)
print("Multiplication:", num1 * num2)
print("Division:", num1 / num2)
```

---

## Practical Example

### Student Result Program

The following example combines input, comparison operators, and conditional statements.

```python
name = input("Enter student name: ")
marks = float(input("Enter marks: "))

if marks >= 90:
    grade = "A+"
elif marks >= 75:
    grade = "A"
elif marks >= 60:
    grade = "B"
elif marks >= 40:
    grade = "C"
else:
    grade = "Fail"

print("Student:", name)
print("Marks:", marks)
print("Grade:", grade)
```

---

## Mini Practice Programs

Try creating the following programs:

### 1. Even or Odd

Write a program that accepts a number and determines whether it is even or odd.

```python
number = int(input("Enter a number: "))

if number % 2 == 0:
    print("Even")
else:
    print("Odd")
```

### 2. Largest of Two Numbers

```python
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

if a > b:
    print("Largest:", a)
else:
    print("Largest:", b)
```

### 3. Multiplication Table

```python
number = int(input("Enter a number: "))

for i in range(1, 11):
    print(number, "x", i, "=", number * i)
```

### 4. Sum of Numbers

```python
total = 0

for i in range(1, 11):
    total += i

print("Sum:", total)
```

---

## Summary

In Part 2, we covered:

- **Conditional Statements** — `if`, `if-else`, `if-elif-else`, and nested `if`
- **Comparison Operators** — `==`, `!=`, `>`, `<`, `>=`, and `<=`
- **Loops** — `for` and `while`
- **Loop Control** — `break`, `continue`, and `pass`
- **User Input** — Reading and converting values using `input()`
- **Practical Programs** — Applying conditions and loops to solve simple problems

---

## Learning Outcome

After completing this part, learners should be able to:

1. Write programs using conditional statements.
2. Compare values using comparison operators.
3. Repeat operations using `for` and `while` loops.
4. Control loop execution using `break`, `continue`, and `pass`.
5. Accept and process user input.
6. Build simple Python programs using multiple concepts together.

---

## Next Part

The next part can build on these fundamentals with:

- Strings and string methods
- List methods and operations
- Tuple operations
- Dictionary methods
- Set operations
- Functions
- Arguments and return values
- Scope and reusable code
