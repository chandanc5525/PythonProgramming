# ── *args — variable-length positional arguments ──────────────
# *args collects extra positional arguments into a TUPLE
def add_all(*args):
    print(f"args = {args}, type = {type(args)}")
    return sum(args)

print(add_all(1, 2, 3))            # 6
print(add_all(10, 20, 30, 40))     # 100
print()

# Mix required params with *args
def greet_all(greeting, *names):
    for name in names:
        print(f"{greeting}, {name}!")

greet_all("Hi", "Alice", "Bob", "Charlie")
print()

# ── **kwargs — variable-length keyword arguments ──────────────
# **kwargs collects extra keyword arguments into a DICT
def build_profile(**kwargs):
    print(f"kwargs = {kwargs}, type = {type(kwargs)}")
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

build_profile(name="Alice", age=30, city="NYC")
print()

# ── Combining *args and **kwargs ──────────────────────────────
# Parameter order: positional, *args, keyword-only, **kwargs
def super_func(required, *args, **kwargs):
    print(f"required: {required}")
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")

super_func("hello", 1, 2, 3, color="red", size=10)
print()

# ── Unpacking with * and ** ───────────────────────────────────
def show_info(name, age, city):
    print(f"{name} is {age} years old, lives in {city}")

# Unpack a list with *
data_list = ["Bob", 25, "London"]
show_info(*data_list)

# Unpack a dict with **
data_dict = {"name": "Charlie", "age": 35, "city": "Paris"}
show_info(**data_dict)
print()

# ── Practical example: flexible calculator ────────────────────
def calculate(operation, *numbers):
    """Perform an operation on a variable number of inputs."""
    if operation == "add":
        return sum(numbers)
    elif operation == "multiply":
        result = 1
        for n in numbers:
            result *= n
        return result
    elif operation == "average":
        return sum(numbers) / len(numbers)
    else:
        return "Unknown operation"

print(calculate("add", 1, 2, 3, 4, 5))       # 15
print(calculate("multiply", 2, 3, 4))          # 24
print(calculate("average", 80, 90, 100, 70))   # 85.0
print()

# ── Practical example: HTML tag builder ───────────────────────
def make_tag(tag, content, **attributes):
    """Build an HTML tag with optional attributes."""
    attrs = " ".join(f'{k}="{v}"' for k, v in attributes.items())
    if attrs:
        return f"<{tag} {attrs}>{content}</{tag}>"
    return f"<{tag}>{content}</{tag}>"

print(make_tag("p", "Hello World"))
print(make_tag("a", "Click here", href="https://python.org", target="_blank"))
print(make_tag("div", "Content", id="main", style="color:red"))
