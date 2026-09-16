# ── The LEGB Rule ─────────────────────────────────────────────
# Python resolves variable names in this order:
#   L — Local       (inside the current function)
#   E — Enclosing   (inside an outer/enclosing function)
#   G — Global      (top level of the module / .py file)
#   B — Built-in    (pre-loaded names: print, len, range, etc.)

# ── Example 1: Local vs Global ────────────────────────────────
x = "global"

def show_local():
    x = "local"         # creates a NEW local variable, doesn't touch global
    print("Inside function:", x)

show_local()            # Inside function: local
print("Outside function:", x)   # Outside function: global

# ── Example 2: Enclosing scope (nested functions) ─────────────
def outer():
    message = "enclosing"

    def inner():
        print("Inner sees:", message)  # finds 'message' in enclosing scope

    inner()

outer()  # Inner sees: enclosing

# ── Example 3: Full LEGB demonstration ────────────────────────
x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print("inner:", x)      # local

    inner()
    print("outer:", x)          # enclosing

outer()
print("module:", x)             # global

# ── The global keyword ────────────────────────────────────────
counter = 0

def increment():
    global counter      # tells Python to use the global 'counter'
    counter += 1

increment()
increment()
increment()
print("Counter:", counter)  # 3

# ── The nonlocal keyword ──────────────────────────────────────
def make_counter():
    count = 0

    def increment():
        nonlocal count  # modifies the enclosing variable
        count += 1
        return count

    return increment

counter_fn = make_counter()
print(counter_fn())   # 1
print(counter_fn())   # 2
print(counter_fn())   # 3

# ── Common pitfall: UnboundLocalError ─────────────────────────
total = 100

def broken_update():
    # total += 10       # UnboundLocalError! Python sees assignment and
    pass                 # treats 'total' as local, but it's not defined yet

def fixed_update():
    global total
    total += 10

fixed_update()
print("Total:", total)  # 110
