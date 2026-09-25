# ── Lambda — Anonymous one-liner functions ─────────────────────
# Syntax: lambda arguments: expression
# - Can take any number of arguments
# - Only ONE expression (automatically returned)
# - No "return" keyword needed

# ── Basic examples ─────────────────────────────────────────────

# Regular function vs lambda
def square_func(x):
    return x ** 2

square_lambda = lambda x: x ** 2

print(square_func(5))     # 25
print(square_lambda(5))   # 25 — identical result

# Multiple arguments
add = lambda a, b: a + b
print(add(10, 20))        # 30

multiply = lambda a, b: a * b
print(multiply(3, 7))     # 21

# No arguments
greet = lambda: "Hello, World!"
print(greet())            # Hello, World!

# ── Conditional (ternary) inside lambda ────────────────────────
check_even = lambda x: "Even" if x % 2 == 0 else "Odd"
print(check_even(4))      # Even
print(check_even(7))      # Odd

# Absolute value using lambda
absolute = lambda x: x if x >= 0 else -x
print(absolute(-5))       # 5
print(absolute(3))        # 3

# Grade assigner
grade = lambda score: "Pass" if score >= 50 else "Fail"
print(grade(75))          # Pass
print(grade(30))          # Fail

# ── Lambda with sorted() — sorting by custom key ──────────────
words = ["banana", "pie", "apple", "fig", "cherry"]

by_length = sorted(words, key=lambda w: len(w))
print("By length:", by_length)
# ['pie', 'fig', 'apple', 'banana', 'cherry']

by_last_char = sorted(words, key=lambda w: w[-1])
print("By last char:", by_last_char)
# ['banana', 'apple', 'pie', 'cherry', 'fig']

# Sorting dictionaries
students = [
    {"name": "Alice", "grade": 88},
    {"name": "Bob", "grade": 72},
    {"name": "Charlie", "grade": 95},
    {"name": "Diana", "grade": 81},
]

by_grade = sorted(students, key=lambda s: s["grade"], reverse=True)
for s in by_grade:
    print(f"  {s['name']}: {s['grade']}")

# ── Lambda with max() / min() ─────────────────────────────────
products = [("Laptop", 999), ("Mouse", 25), ("Keyboard", 75), ("Monitor", 450)]

cheapest = min(products, key=lambda p: p[1])
priciest = max(products, key=lambda p: p[1])
print(f"Cheapest: {cheapest[0]} (${cheapest[1]})")
print(f"Priciest: {priciest[0]} (${priciest[1]})")

# ── Lambda in a list (storing operations) ──────────────────────
operations = [
    ("add 10", lambda x: x + 10),
    ("double", lambda x: x * 2),
    ("square", lambda x: x ** 2),
    ("negate", lambda x: -x),
]

value = 5
for name, op in operations:
    print(f"  {name}({value}) = {op(value)}")

# ── Immediately invoked lambda ─────────────────────────────────
result = (lambda x, y: x + y)(3, 4)
print("Immediately invoked:", result)  # 7

# ── Key takeaway ───────────────────────────────────────────────
# Use lambda for SHORT, SIMPLE operations passed to other functions.
# If it gets complex or hard to read, use a regular def function instead.
