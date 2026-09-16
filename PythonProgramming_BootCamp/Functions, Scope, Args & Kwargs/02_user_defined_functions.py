# ── Basic function with def ────────────────────────────────────
def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}!"

print(greet("Alice"))   # Hello, Alice!
print(greet("Bob"))     # Hello, Bob!

# ── Parameters and arguments ──────────────────────────────────
def add(a, b):
    return a + b

print(add(3, 4))        # 7
print(add(10, 20))      # 30

# ── Default parameter values ──────────────────────────────────
def power(base, exp=2):
    """Raise base to exp (defaults to squaring)."""
    return base ** exp

print(power(5))          # 25   (exp defaults to 2)
print(power(2, 10))      # 1024
print(power(3, 3))       # 27

# ── Keyword arguments — order doesn't matter ──────────────────
def describe_pet(animal, name):
    print(f"I have a {animal} named {name}.")

describe_pet("dog", "Rex")
describe_pet(name="Whiskers", animal="cat")  # keyword args

# ── Returning multiple values (tuple unpacking) ──────────────
def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([3, 1, 7, 2, 9])
print(f"Min: {lo}, Max: {hi}")  # Min: 1, Max: 9

# ── Lambda — anonymous one-liner functions ────────────────────
square = lambda x: x ** 2
print(square(6))        # 36

# Useful with built-in functions like sorted
students = [("Alice", 88), ("Bob", 72), ("Charlie", 95)]
sorted_students = sorted(students, key=lambda s: s[1], reverse=True)
print(sorted_students)  # [('Charlie', 95), ('Alice', 88), ('Bob', 72)]

# ── Functions as first-class objects ──────────────────────────
def shout(text):
    return text.upper() + "!"

def whisper(text):
    return text.lower() + "..."

def speak(func, message):
    return func(message)

print(speak(shout, "hello"))     # HELLO!
print(speak(whisper, "Hello"))   # hello...
