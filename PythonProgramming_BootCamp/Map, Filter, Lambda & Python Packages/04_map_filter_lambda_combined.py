# ── Chaining map() + filter() + lambda ─────────────────────────
# A powerful pattern: filter first, then transform (or vice versa)

# ── Example 1: Squares of even numbers ────────────────────────
nums = range(1, 11)

# Step by step
evens = filter(lambda x: x % 2 == 0, nums)     # keep evens
squared = map(lambda x: x ** 2, evens)           # square them
result = list(squared)
print("Squared evens:", result)  # [4, 16, 36, 64, 100]

# Same thing in one line (reads inside-out)
result2 = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, range(1, 11))))
print("One-liner:", result2)     # [4, 16, 36, 64, 100]

# Equivalent list comprehension (often more readable)
result3 = [x**2 for x in range(1, 11) if x % 2 == 0]
print("Comprehension:", result3)  # [4, 16, 36, 64, 100]

# ── Example 2: Process student data ───────────────────────────
students = [
    {"name": "Alice", "score": 88},
    {"name": "Bob", "score": 42},
    {"name": "Charlie", "score": 95},
    {"name": "Diana", "score": 31},
    {"name": "Eve", "score": 76},
]

# Get names of students who passed (score >= 50)
passed_names = list(
    map(
        lambda s: s["name"],                    # extract name
        filter(lambda s: s["score"] >= 50, students)  # keep passers
    )
)
print("Passed:", passed_names)  # ['Alice', 'Charlie', 'Eve']

# ── Example 3: Clean and transform data ───────────────────────
raw_data = ["  alice  ", "", "BOB", "  ", "charlie", None, "DIANA"]

# Step 1: filter out None and blank strings
valid = filter(lambda x: x is not None and x.strip(), raw_data)
# Step 2: strip whitespace and title-case
cleaned = list(map(lambda x: x.strip().title(), valid))
print("Cleaned:", cleaned)  # ['Alice', 'Bob', 'Charlie', 'Diana']

# ── Example 4: Price calculator with discounts ────────────────
products = [
    {"name": "Laptop", "price": 999, "on_sale": True},
    {"name": "Mouse", "price": 25, "on_sale": False},
    {"name": "Keyboard", "price": 75, "on_sale": True},
    {"name": "Monitor", "price": 450, "on_sale": False},
    {"name": "Headset", "price": 120, "on_sale": True},
]

# Get discounted prices (10% off) for items on sale
sale_prices = list(
    map(
        lambda p: f"{p['name']}: ${p['price'] * 0.9:.2f}",
        filter(lambda p: p["on_sale"], products)
    )
)
print("\nSale prices:")
for item in sale_prices:
    print(f"  {item}")

# ── Example 5: Using reduce for the complete picture ──────────
from functools import reduce

nums = [1, 2, 3, 4, 5]

# Sum of squares of odd numbers
result = reduce(
    lambda acc, x: acc + x,         # accumulate (sum)
    map(lambda x: x**2,              # square each
        filter(lambda x: x % 2 != 0, nums))  # keep odds
)
print(f"\nSum of odd squares: {result}")  # 1 + 9 + 25 = 35

# ── Comparison summary ────────────────────────────────────────
print("\n--- Quick Reference ---")
print("map(fn, iter)    → transforms each item")
print("filter(fn, iter) → keeps items where fn returns True")
print("reduce(fn, iter) → accumulates items into single value")
print("lambda args: expr → anonymous one-line function")
