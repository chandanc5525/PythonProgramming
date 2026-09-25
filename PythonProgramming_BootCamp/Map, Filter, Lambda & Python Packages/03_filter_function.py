# ── filter() — keep items that pass a test ─────────────────────
# Syntax: filter(function, iterable)
# The function must return True or False (a predicate)
# Returns a filter object (lazy iterator) — wrap in list()

# ── Example 1: Keep even numbers ──────────────────────────────
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, nums))
print("Evens:", evens)  # [2, 4, 6, 8, 10]

# ── Example 2: Keep odd numbers ───────────────────────────────
odds = list(filter(lambda x: x % 2 != 0, nums))
print("Odds:", odds)    # [1, 3, 5, 7, 9]

# ── Example 3: Filter adults (age >= 18) ──────────────────────
ages = [12, 25, 8, 30, 17, 42, 15, 21]
adults = list(filter(lambda a: a >= 18, ages))
print("Adults:", adults)  # [25, 30, 42, 21]

# ── Example 4: Filter positive numbers ────────────────────────
numbers = [-5, 3, -1, 7, 0, -3, 8, 2]
positives = list(filter(lambda x: x > 0, numbers))
print("Positives:", positives)  # [3, 7, 8, 2]

# ── Example 5: Filter non-empty strings ───────────────────────
items = ["hello", "", "world", "", "python", ""]
non_empty = list(filter(lambda s: len(s) > 0, items))
print("Non-empty:", non_empty)  # ['hello', 'world', 'python']

# ── Example 6: Using None — removes falsy values ──────────────
mixed = [0, 1, "", "hi", None, True, False, [], [1, 2], 42]
truthy = list(filter(None, mixed))
print("Truthy:", truthy)  # [1, 'hi', True, [1, 2], 42]

# ── Example 7: Using a named function ─────────────────────────
def is_passing(score):
    return score >= 50

scores = [88, 42, 73, 31, 95, 50, 19]
passing = list(filter(is_passing, scores))
print("Passing:", passing)  # [88, 73, 95, 50]

# ── Example 8: Filter words longer than 4 characters ──────────
words = ["hi", "hello", "hey", "world", "python", "ok", "great"]
long_words = list(filter(lambda w: len(w) > 4, words))
print("Long words:", long_words)  # ['hello', 'world', 'python', 'great']

# ── Example 9: Filter dictionary data ─────────────────────────
employees = [
    {"name": "Alice", "salary": 70000},
    {"name": "Bob", "salary": 50000},
    {"name": "Carol", "salary": 85000},
    {"name": "Dave", "salary": 45000},
]

high_earners = list(filter(lambda e: e["salary"] >= 60000, employees))
for emp in high_earners:
    print(f"  {emp['name']}: ${emp['salary']:,}")

# ── filter vs list comprehension ──────────────────────────────
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

using_filter = list(filter(lambda x: x > 5, nums))
using_comp = [x for x in nums if x > 5]

print("filter:", using_filter)  # [6, 7, 8, 9, 10]
print("comp:", using_comp)      # [6, 7, 8, 9, 10]
