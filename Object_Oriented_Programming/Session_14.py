# --------------------------------------------------
# Session 14: Object-Oriented Programming (OOP) in Python Programming
# --------------------------------------------------
## Author: Chandan Chaudhari
## Github: https://github.com/chandanc5525
# --------------------------------------------------

# Concept of *args and **kwargs in Python Programming

'''
*args and **kwargs are special syntax in Python that allow you to pass a variable number of arguments to a function.
- *args (Non-Keyword Arguments): This allows you to pass a variable number of non-keyword arguments to a function. The arguments are passed as a tuple.
- **kwargs (Keyword Arguments): This allows you to pass a variable number of keyword arguments to a function. The arguments are passed as a dictionary.

Example of *args:

def my_function(*args):  # Function Definition with *args

    for arg in args:
        print(arg)
        
        
my_function(1, 2, 3, 'Hello', 'World')  # Passing multiple arguments to the function

Output:
1
2
3
Hello
World

-------------------------------------------------------------------
Example of **kwargs:

def my_function(**kwargs):      # Function Definition with **kwargs

    for key, value in kwargs.items():
        print(f"{key}: {value}")

my_function(name='Chandan Chaudhari', age=30, city='Mumbai') # Passing multiple keyword arguments to the function

Output:

name: Chandan Chaudhari
age: 30
city: Mumbai

'''

# Write a program to demonstrate the use of *args and **kwargs in a function that calculates the total price of items in a shopping cart.

class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, item_name, price):
        self.items[item_name] = price

    def calculate_total(self, *args, **kwargs):
        total = 0
        
        # Calculate total from *args
        for item in args:
            if item in self.items:
                total += self.items[item]
        
        # Calculate total from **kwargs
        for item, quantity in kwargs.items():
            if item in self.items:
                total += self.items[item] * quantity
        
        return total
    
# Create a shopping cart instance
cart = ShoppingCart()

# Add items to the shopping cart
cart.add_item('Apple', 1.5)
cart.add_item('Banana', 0.5)
cart.add_item('Orange', 0.75)

# Calculate total price using *args
total_price_args = cart.calculate_total('Apple', 'Banana')
print(f"Total price using *args: {total_price_args}")

# Calculate total price using **kwargs
total_price_kwargs = cart.calculate_total(Apple=2, Banana=3, Orange=1)
print(f"Total price using **kwargs: {total_price_kwargs}")

'''
Output:
Total price using *args: 2.0
Total price using **kwargs: 7.25
'''

# -----------------------------------------------------------------



# write a program for indian railway reservation system using OOP in python programming language using *args and **kwargs

#
class RailwayReservationSystem:
    
    def __init__(self):
        self.reservations = {}

    def book_ticket(self, passenger_name, train_number, *args, **kwargs):
        reservation_id = len(self.reservations) + 1
        reservation_details = {
            'passenger_name': passenger_name,
            'train_number': train_number,
            'additional_info': args,
            'preferences': kwargs
        }
        self.reservations[reservation_id] = reservation_details
        return reservation_id
    
    def get_reservation_details(self, reservation_id):
        return self.reservations.get(reservation_id, "Reservation not found")
    
# Create an instance of the Railway Reservation System
reservation_system = RailwayReservationSystem()

# Book a ticket with additional information and preferences
reservation_id = reservation_system.book_ticket(
    passenger_name='Chandan Chaudhari',
    train_number='12345',
    'Window Seat', 'Vegetarian Meal',  # Additional information using *args
    seat_preference='Window', meal_preference='Vegetarian'  # Preferences using **kwargs
)

# Get reservation details
details = reservation_system.get_reservation_details(reservation_id)
print(f"Reservation ID: {reservation_id}")
print("Reservation Details:")
print(details)


'''
Output:

Reservation ID: 1
Reservation Details:
{'passenger_name': 'Chandan Chaudhari', 'train_number': '12345', 'additional_info': ('Window Seat', 'Vegetarian Meal'), 'preferences': {'seat_preference': 'Window', 'meal_preference': 'Vegetarian'}}
'''

# -----------------------------------------------------------------

# Write a program for library management system using OOP in python programming language using *args and **kwargs

class LibraryManagementSystem:
    
    def __init__(self):
        self.books = {}
        self.borrowers = {}

    def add_book(self, book_id, title, author):
        self.books[book_id] = {
            'title': title,
            'author': author,
            'available': True
        }

    def register_borrower(self, borrower_id, name):
        self.borrowers[borrower_id] = {
            'name': name,
            'borrowed_books': []
        }

    def borrow_book(self, borrower_id, book_id, *args, **kwargs):
        if book_id in self.books and self.books[book_id]['available']:
            self.books[book_id]['available'] = False
            self.borrowers[borrower_id]['borrowed_books'].append(book_id)
            return f"{self.borrowers[borrower_id]['name']} borrowed '{self.books[book_id]['title']}'"
        else:
            return "Book is not available"
        
# Create an instance of the Library Management System
library_system = LibraryManagementSystem()
# Add books to the library
library_system.add_book(book_id=1, title='The Great Gatsby', author='F. Scott Fitzgerald')
library_system.add_book(book_id=2, title='To Kill a Mockingbird', author='Harper Lee')

# Register a borrower
library_system.register_borrower(borrower_id=1, name='Chandan Chaudhari')

# Borrow a book
borrow_result = library_system.borrow_book(borrower_id=1, book_id=1)
print(borrow_result)

'''
Output:

Chandan Chaudhari borrowed 'The Great Gatsby'
'''

# -----------------------------------------------------------------