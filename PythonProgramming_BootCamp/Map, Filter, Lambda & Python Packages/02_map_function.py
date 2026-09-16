# ── map() — apply a function to every item ─────────────────────
# Syntax: map(function, iterable)
# Returns a map object (lazy iterator) — wrap in list() to see results

# ── Example 1: Square every number ─────────────────────────────
nums = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, nums))
print("Squared:", squared)  # [1, 4, 9, 16, 25]

# ── Example 2: Using a named function ─────────────────────────
def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

temps_c = [0, 20, 37, 100]
temps_f = list(map(celsius_to_fahrenheit, temps_c))
print("Fahrenheit:", temps_f)  # [32.0, 68.0, 98.6, 212.0]

# ── Example 3: Convert strings to integers ────────────────────
str_numbers = ["10", "20", "30", "40"]
int_numbers = list(map(int, str_numbers))
print("Integers:", int_numbers)  # [10, 20, 30, 40]

# ── Example 4: Uppercase all strings ──────────────────────────
names = ["alice", "bob", "charlie"]
upper_names = list(map(str.upper, names))
print("Upper:", upper_names)  # ['ALICE', 'BOB', 'CHARLIE']

# ── Example 5: Get string lengths ─────────────────────────────
words = ["hello", "world", "python", "is", "great"]
lengths = list(map(len, words))
print("Lengths:", lengths)  # [5, 5, 6, 2, 5]

# ── Example 6: map with two iterables ─────────────────────────
prices = [10.0, 20.0, 30.0]
quantities = [3, 5, 2]
totals = list(map(lambda p, q: p * q, prices, quantities))
print("Totals:", totals)  # [30.0, 100.0, 60.0]

# ── Example 7: Add corresponding elements from three lists ────
a = [1, 2, 3]
b = [10, 20, 30]
c = [100, 200, 300]
sums = list(map(lambda x, y, z: x + y + z, a, b, c))
print("Sums:", sums)  # [111, 222, 333]

# ── map vs list comprehension ─────────────────────────────────
# Both produce the same result — pick the one that reads better
nums = [1, 2, 3, 4, 5]

using_map = list(map(lambda x: x * 3, nums))
using_comp = [x * 3 for x in nums]

print("map:", using_map)    # [3, 6, 9, 12, 15]
print("comp:", using_comp)  # [3, 6, 9, 12, 15]
