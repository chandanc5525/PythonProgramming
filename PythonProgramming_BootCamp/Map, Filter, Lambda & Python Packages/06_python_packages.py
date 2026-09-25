# ── Python Packages & pip ──────────────────────────────────────
# Python has a massive ecosystem of third-party packages on PyPI
# (Python Package Index — https://pypi.org)
#
# pip = Python's package installer
#
# Common pip commands (run in terminal, NOT in Python):
#   pip install requests        # install a package
#   pip install requests==2.31  # install specific version
#   pip uninstall requests      # remove a package
#   pip list                    # show all installed packages
#   pip show requests           # details about a package
#   pip freeze                  # output for requirements.txt
#   pip freeze > requirements.txt   # save dependencies to file
#   pip install -r requirements.txt # install from file

# ── Virtual Environments ──────────────────────────────────────
# Always use a virtual environment to isolate project dependencies!
#
# Create:   python -m venv myenv
# Activate: myenv\Scripts\activate     (Windows)
#           source myenv/bin/activate   (Mac/Linux)
# Deactivate: deactivate

# ── Popular Python packages ───────────────────────────────────
# Let's explore some built-in modules (no pip install needed)

# --- os: operating system interaction ---
import os
print("Current directory:", os.getcwd())
print("Files here:", os.listdir(".")[:5], "...")  # first 5 files

# --- sys: system-specific parameters ---
import sys
print(f"\nPython version: {sys.version}")
print(f"Platform: {sys.platform}")

# --- json: work with JSON data ---
import json

data = {"name": "Alice", "age": 30, "skills": ["Python", "SQL"]}
json_str = json.dumps(data, indent=2)
print(f"\nJSON output:\n{json_str}")

parsed = json.loads(json_str)
print(f"Parsed back: {parsed['name']}")

# --- datetime: dates and times ---
from datetime import datetime, timedelta

now = datetime.now()
print(f"\nNow: {now.strftime('%Y-%m-%d %H:%M:%S')}")

future = now + timedelta(days=30)
print(f"30 days from now: {future.strftime('%Y-%m-%d')}")

# --- math: mathematical functions ---
import math

print(f"\npi = {math.pi:.4f}")
print(f"sqrt(144) = {math.sqrt(144)}")
print(f"ceil(4.2) = {math.ceil(4.2)}")
print(f"floor(4.8) = {math.floor(4.8)}")

# --- random: generate random data ---
import random

print(f"\nRandom int (1-100): {random.randint(1, 100)}")
print(f"Random choice: {random.choice(['apple', 'banana', 'cherry'])}")

items = [1, 2, 3, 4, 5]
random.shuffle(items)
print(f"Shuffled: {items}")

# ── Third-party packages (need pip install) ───────────────────
# These are some of the most popular — install when needed:
#
# pip install requests     → HTTP requests (APIs)
# pip install numpy        → Numerical computing
# pip install pandas       → Data analysis
# pip install matplotlib   → Plotting / charts
# pip install flask        → Web framework (lightweight)
# pip install django       → Web framework (full-featured)
# pip install pytest       → Testing framework
# pip install black        → Code formatter
# pip install pillow       → Image processing

# ── Example: using requests (if installed) ────────────────────
# Uncomment below if you have requests installed:
#
# import requests
# response = requests.get("https://api.github.com")
# print(response.status_code)   # 200
# print(response.json())        # parsed JSON response

print("\n--- Key Takeaways ---")
print("1. Use pip to install third-party packages from PyPI")
print("2. Always use virtual environments (python -m venv)")
print("3. Save deps with: pip freeze > requirements.txt")
print("4. Python's standard library is already very powerful!")
