# --------------------------------------------------
# Session 11: Functions of Python Programming
# --------------------------------------------------
## Author: Chandan Chaudhari
## Github: https://github.com/chandanc5525
# --------------------------------------------------

'''
# Functions in Python Programming:

Defintion: A function is a reusable block of code that performs a specific task. It allows you to break down your code into smaller, more manageable pieces, making it easier to read, maintain, and debug.

Types of functions in Python Programming:

1. Built-in Functions: These are functions that are provided by Python and are available for use without needing to import any modules. Examples include print(), len(), type(), etc.
2. User-defined Functions: These are functions that you create yourself to perform specific tasks. You can define a function using the def keyword, followed by the function name and parentheses.
3. Lambda Functions: These are anonymous functions that are defined using the lambda keyword. They are typically used for short, simple functions that are not intended to be reused elsewhere in the code.
4. Recursive Functions: These are functions that call themselves in order to solve a problem. They typically have a base case that stops the recursion and a recursive case that breaks the problem into smaller subproblems.
5. Generator Functions: These are functions that use the yield keyword to produce a sequence of values. They are useful for creating iterators and can be more memory-efficient than using lists to store large sequences of data.
6. Higher-order Functions: These are functions that can take other functions as arguments or return functions as their result. Examples include map(), filter(), and reduce().
7. Decorator Functions: These are functions that modify the behavior of other functions. They are typically defined using the @decorator syntax and can be used to add functionality to existing functions without modifying their code.
8. Async Functions: These are functions that are defined using the async keyword and are used for asynchronous programming. They allow you to write code that can run concurrently without blocking the main thread of execution.
9. Static Methods: These are methods that belong to a class rather than an instance of the class. They are defined using the @staticmethod decorator and can be called on the class itself without needing to create an instance.
10. Class Methods: These are methods that belong to a class and can access and modify class-level attributes. They are defined using the @classmethod decorator and take the class itself as the first argument (usually named cls).
11. Instance Methods: These are methods that belong to an instance of a class and can access and modify instance-level attributes. They are defined without any decorators and take the instance itself as the first argument (usually named self).
12. Abstract Methods: These are methods that are declared in an abstract class and must be implemented by any subclass that inherits from the abstract class. They are defined using the @abstractmethod decorator from the abc module.
13. Static Methods: These are methods that belong to a class rather than an instance of the class. They are defined using the @staticmethod decorator and can be called on the class itself without needing to create an instance.
    
'''

# --------------------------------------------------

# Built-in Functions in Python Programming

'''
Built in functions are as follows:
1. print(): This function is used to display output on the console.
2. len(): This function is used to get the length of an object, such as a string, list, or tuple.
3. type(): This function is used to get the type of an object.
4. int(): This function is used to convert a value to an integer.
5. float(): This function is used to convert a value to a floating-point number.
6. str(): This function is used to convert a value to a string.
7. list(): This function is used to convert an iterable to a list.
8. tuple(): This function is used to convert an iterable to a tuple.
9. dict(): This function is used to create a dictionary from a sequence of key-value pairs.
10. set(): This function is used to create a set from an iterable.
11. sum(): This function is used to calculate the sum of a sequence of numbers.
12. max(): This function is used to find the maximum value in a sequence of numbers.
13. min(): This function is used to find the minimum value in a sequence of numbers.
14. abs(): This function is used to get the absolute value of a number.
15. round(): This function is used to round a number to a specified number of decimal places.
16. sorted(): This function is used to sort a sequence of items in ascending order.
17. reversed(): This function is used to reverse the order of a sequence of items.
18. enumerate(): This function is used to add a counter to an iterable and return it as an enumerate object.
19. zip(): This function is used to combine two or more iterables into a single iterable of tuples.
20. map(): This function is used to apply a specified function to each item in an iterable and return a map object.
21. filter(): This function is used to filter items in an iterable based on a specified condition
22. reduce(): This function is used to apply a specified function cumulatively to the items in an iterable, reducing the iterable to a single value.
23. any(): This function is used to check if any item in an iterable is true.
24. all(): This function is used to check if all items in an iterable are true.
25. isinstance(): This function is used to check if an object is an instance of a specified class or a subclass thereof.
26. issubclass(): This function is used to check if a class is a subclass of another class.
27. math.sqrt(): This function is used to calculate the square root of a number.
28. random.randint(): This function is used to generate a random integer between a specified range.
29. datetime.now(): This function is used to get the current date and time.
30. os.listdir(): This function is used to get a list of files and directories in a specified directory.
31. sys.exit(): This function is used to exit the program.
32. open(): This function is used to open a file and return a file object.


'''

# %%
import math 

print(math.sqrt(16))  # Output: 4.0
print(math.ceil(20.99))  # Output: 21
print(math.floor(20.99))  # Output: 20


