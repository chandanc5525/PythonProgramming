# ── User-Defined Packages ──────────────────────────────────────
# A MODULE  = any single .py file you can import
# A PACKAGE = a folder containing modules + __init__.py
#
# Folder structure for a package:
#
#   my_project/
#   ├── main.py              ← your entry point
#   └── mypackage/           ← this is the package
#       ├── __init__.py       ← makes the folder a package (can be empty)
#       ├── math_utils.py     ← module with math functions
#       └── string_utils.py   ← module with string functions

# ── Creating a simple module (no package needed) ──────────────
# If you have a file called "helpers.py" in the same directory:
#
#   # helpers.py
#   def add(a, b):
#       return a + b
#
#   def multiply(a, b):
#       return a * b
#
# You can import it in another file:
#
#   import helpers
#   print(helpers.add(3, 4))       # 7
#
#   from helpers import multiply
#   print(multiply(3, 4))          # 12

# ── Let's simulate a module right here ─────────────────────────
# (Normally these would be in separate files)

# --- Imagine this is math_utils.py ---
def add(a, b):
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    return a - b

def factorial(n):
    """Calculate factorial of n."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


# --- Imagine this is string_utils.py ---
def shout(text):
    """Convert text to uppercase with exclamation."""
    return text.upper() + "!"

def whisper(text):
    """Convert text to lowercase with ellipsis."""
    return text.lower() + "..."

def title_all(words):
    """Title-case a list of words."""
    return [w.title() for w in words]


# ── Using our "modules" ───────────────────────────────────────
print("add(3, 4):", add(3, 4))
print("subtract(10, 3):", subtract(10, 3))
print("factorial(5):", factorial(5))
print("shout('hello'):", shout("hello"))
print("whisper('Hello'):", whisper("Hello"))
print("title_all:", title_all(["alice", "bob", "charlie"]))

# ── __init__.py explained ─────────────────────────────────────
# __init__.py runs when the package is first imported.
# It can be empty (just marks the folder as a package),
# or it can define what gets exported:
#
#   # mypackage/__init__.py
#   from .math_utils import add, subtract
#   from .string_utils import shout
#
# Then in main.py you can do:
#   from mypackage import add, shout
#   print(add(1, 2))
#   print(shout("hi"))

# ── __name__ and __main__ ─────────────────────────────────────
# When a .py file is RUN directly:  __name__ == "__main__"
# When a .py file is IMPORTED:      __name__ == "module_name"

if __name__ == "__main__":
    print("\nThis script is being run directly!")
    print("If imported, this block would NOT execute.")
    print("Use this pattern to add test/demo code to modules.")
