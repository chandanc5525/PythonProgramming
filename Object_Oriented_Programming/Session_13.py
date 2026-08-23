# --------------------------------------------------
# Session 13: Object-Oriented Programming (OOP) in Python Programming
# --------------------------------------------------
## Author: Chandan Chaudhari
## Github: https://github.com/chandanc5525
# --------------------------------------------------

# Concept of Class and Object in Python Programming

''' 
Definition of Class:
A class is a blueprint or template for creating objects. It defines a set of attributes and methods that the objects created from the class will have. 
class can be thought of as a user-defined data type that encapsulates data and functions that operate on that data.

Definition of Object:
An object is an instance of a class. It is a specific realization of a class that has its own unique identity and state.

example:

class Car: # Define a class : Car
    def __init__(self, make, model, year): # Constructor method to initialize the attributes of the class
        self.make = make                   # self is a reference to the current instance of the class, and it is used to access the attributes and methods of the class
        self.model = model                 # The __init__ method is a special method that is called when an object is created from the class. It is used to initialize the attributes of the class with the values passed as arguments.
        self.year = year                   # The attributes make, model, and year are defined in the __init__ method and are assigned the values passed as arguments when creating an object of the Car class.

    def display_info(self):                # Method to display the information of the car
        print(f"{self.year} {self.make} {self.model}")  # The display_info method is a regular method that can be called on an object of the Car class to display the information of the car.

# Creating an object of the Car class

my_car = Car("Toyota", "Camry", 2026)     # An object my_car is created from the Car class, and the attributes make, model, and year are initialized with the values "Toyota", "Camry", and 2020 respectively.
my_car.display_info()                     # The display_info method is called on the my_car object to display the information of the car, which will output "2020 Toyota Camry".

# Output: 2026 Toyota Camry             
'''

class Person:
    pass

print(type(Person)) # Output: <class 'type'>

person1 = Person() # Object of the Person class
print(type(person1)) # Output: <class '__main__.Person'>

# ------------------------------------------------

# %%
class Program: # Class definition
    language = "Python" # Class attribute
    version = "3.9"     # Class attribute
    
    def display_info(self): # Method definition
        print(f"Programming Language: {self.language}, Version: {self.version}") # Accessing class attributes using self
        


    
print(Program.language) # Output: Python
print(Program.version)  # Output: 3.9

program1 = Program() # Object of the Program class
program1.language = "Java" # Modifying the class attribute for the object program1
program1.version = "15"   # Modifying the class attribute for the object program1
program1.display_info()   # Method calling with .operator to display the information of the programming language and version for the object program1

'''
Output:
Python
3.9
Programming Language: Java, Version: 15
'''


# ------------------------------------------------

# Function attribute in Python Programming

#%%
class Calculator: # Class definition
    
    num1 = float(input("Enter first number: ")) # Class attribute with user input
    num2 = float(input("Enter second number: ")) # Class attribute with user input
    
    def add(self,num1,num2): # Method definition for addition
        return num1 + num2
    def subtract(self,num1,num2): # Method definition for subtraction
        return num1 - num2
    def multiply(self,num1,num2): # Method definition for multiplication
        return num1 * num2
    def divide(self,num1,num2): # Method definition for division
        if num2 != 0:
            return num1 / num2
        else:
            return "Error: Division by zero is not allowed."
        
calculator = Calculator() # Object of the Calculator class

print(f"Addition: {calculator.add(calculator.num1, calculator.num2)}") # Method calling for addition
print(f"Subtraction: {calculator.subtract(calculator.num1, calculator.num2)}")
print(f"Multiplication: {calculator.multiply(calculator.num1, calculator.num2)}")
print(f"Division: {calculator.divide(calculator.num1, calculator.num2)}")

'''
Output:
Enter first number: 10
Enter second number: 5
Addition: 15.0
Subtraction: 5.0
Multiplication: 50.0
Division: 2.0
'''

# ------------------------------------------------

'''
Example: Write a python program to create a class named "BankAccount" with attributes "account_number", "account_holder", and "balance". The class should have methods to deposit money, withdraw money, and display the account information.
'''

class BankAccount: # Class definition
    
    def __init__(self, account_number, account_holder, balance): # Constructor method to initialize the attributes of the class
        self.account_number = account_number # Instance attribute for account number
        self.account_holder = account_holder # Instance attribute for account holder name
        self.balance = balance # Instance attribute for account balance
        
    def deposit(self, amount): # Method definition for depositing money
        if amount > 0:
            self.balance += amount
            print(f"Deposited: {amount}. New Balance: {self.balance}")
        else:
            print("Deposit amount must be positive.")
    
    def withdraw(self, amount): # Method definition for withdrawing money
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                print(f"Withdrew: {amount}. New Balance: {self.balance}")
            else:
                print("Insufficient funds.")
        else:
            print("Withdrawal amount must be positive.")
    
    def display_info(self): # Method definition for displaying account information
        print(f"Account Number: {self.account_number}, Account Holder: {self.account_holder}, Balance: {self.balance}")     
        
# Creating an object of the BankAccount class
account1 = BankAccount("123456789", "Chandan Chaudhari", 1000000.0) # Object Definition with account number, account holder name, and initial balance
account1.display_info() 


account1.deposit(50000) # Method calling for depositing money
account1.withdraw(20000) # Method calling for withdrawing money
account1.display_info() # Method calling for displaying account information

'''
Output:

Account Number: 123456789, Account Holder: Chandan Chaudhari, Balance: 1000000.0
Deposited: 50000. New Balance: 1050000.0
Withdrew: 20000. New Balance: 1030000.0
Account Number: 123456789, Account Holder: Chandan Chaudhari, Balance: 1030000.0
'''

    
# ------------------------------------------------

'''
Example: Write a python program for indian railway ticket booking system using OOP concepts. The program should have a class named "Train" with attributes "train_number", "train_name", and "available_seats". 
The class should have methods to book a ticket, cancel a ticket, and display the train information.
'''

class Train: # Class definition
    
    def __init__(self, train_number, train_name, available_seats): # Constructor method to initialize the attributes of the class
        self.train_number = train_number # Instance attribute for train number
        self.train_name = train_name # Instance attribute for train name
        self.available_seats = available_seats # Instance attribute for available seats
        
    def book_ticket(self, num_tickets): # Method definition for booking a ticket
        if num_tickets > 0:
            if self.available_seats >= num_tickets:
                self.available_seats -= num_tickets
                print(f"Booked {num_tickets} tickets. Remaining Seats: {self.available_seats}")
            else:
                print("Not enough seats available.")
        else:
            print("Number of tickets must be positive.")
    
    def cancel_ticket(self, num_tickets): # Method definition for canceling a ticket
        if num_tickets > 0:
            self.available_seats += num_tickets
            print(f"Canceled {num_tickets} tickets. Available Seats: {self.available_seats}")
        else:
            print("Number of tickets must be positive.")
    
    def display_info(self): # Method definition for displaying train information
        print(f"Train Number: {self.train_number}, Train Name: {self.train_name}, Available Seats: {self.available_seats}") 
        
# Creating an object of the Train class

train1 = Train("12345", "Rajdhani Express", 100) # Object Definition with train number, train name, and available seats
train1.display_info() # Method calling for displaying train information
train1.book_ticket(5) # Method calling for booking tickets
train1.cancel_ticket(2) # Method calling for canceling tickets
train1.display_info() # Method calling for displaying train information

'''
Output:

Train Number: 12345, Train Name: Rajdhani Express, Available Seats: 100
Booked 5 tickets. Remaining Seats: 95
Canceled 2 tickets. Available Seats: 97
Train Number: 12345, Train Name: Rajdhani Express, Available Seats: 97
'''

# ------------------------------------------------

'''
Example: Write a python program to create a class named "Library" with attributes "library_name", "books_available", and "members". 
The class should have methods to add a book, remove a book, add a member, remove a member, and display the library information.
'''

class Library: # Class definition
    
    def __init__(self, library_name): # Constructor method to initialize the attributes of the class
        self.library_name = library_name # Instance attribute for library name
        self.books_available = [] # Instance attribute for books available in the library
        self.members = [] # Instance attribute for members of the library
        
    def add_book(self, book_name): # Method definition for adding a book to the library
        self.books_available.append(book_name)
        print(f"Added book: {book_name}. Books Available: {self.books_available}")
    
    def remove_book(self, book_name): # Method definition for removing a book from the library
        if book_name in self.books_available:
            self.books_available.remove(book_name)
            print(f"Removed book: {book_name}. Books Available: {self.books_available}")
        else:
            print("Book not found in the library.")
    
    def add_member(self, member_name): # Method definition for adding a member to the library
        self.members.append(member_name)
        print(f"Added member: {member_name}. Members: {self.members}")
    
    def remove_member(self, member_name): # Method definition for removing a member from the library
        if member_name in self.members:
            self.members.remove(member_name)
            print(f"Removed member: {member_name}. Members: {self.members}")
        else:
            print("Member not found in the library.")
    
    def display_info(self): # Method definition for displaying library information
        print(f"Library Name: {self.library_name}, Books Available: {self.books_available}, Members: {self.members}")   
        
# Creating an object of the Library class

library1 = Library("City Library") # Object Definition with library name
library1.display_info() # Method calling for displaying library information
library1.add_book("The Great Gatsby") # Method calling for adding a book to the library
library1.add_book("To Kill a Mockingbird") # Method calling for adding a book to the library
library1.remove_book("The Great Gatsby") # Method calling for removing a book from the library
library1.add_member("Chandan Chaudhari") # Method calling for adding a member to the library
library1.add_member("Deepti Shah") # Method calling for adding a member to the library
library1.remove_member("Deepti Shah") # Method calling for removing a member from the library
library1.display_info() # Method calling for displaying library information

'''
Output:

Library Name: City Library, Books Available: [], Members: []
Added book: The Great Gatsby. Books Available: ['The Great Gatsby']
Added book: To Kill a Mockingbird. Books Available: ['The Great Gatsby', 'To Kill a Mockingbird']
Removed book: The Great Gatsby. Books Available: ['To Kill a Mockingbird']
Added member: Chandan Chaudhari. Members: ['Chandan Chaudhari']
Added member: Deepti Shah. Members: ['Chandan Chaudhari', 'Deepti Shah']
Removed member: Deepti Shah. Members: ['Chandan Chaudhari']

Library Name: City Library, Books Available: ['To Kill a Mockingbird'], Members: ['Chandan Chaudhari']
'''

# ------------------------------------------------
