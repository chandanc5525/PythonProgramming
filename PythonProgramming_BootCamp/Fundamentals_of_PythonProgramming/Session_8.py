# --------------------------------------------------
# Session 8: Fundamentals of Python Programming
# --------------------------------------------------
## Author: Chandan Chaudhari
## Github: https://github.com/chandanc5525
# --------------------------------------------------

# Concept of pass, continue and break statements in Python

# pass statement
for i in range(5):
    if i == 2:
        pass  # This will do nothing and continue to the next iteration
    print(i)
''' 
Output:
0
1
2
3
4
'''    
# continue statement
for i in range(5):
    if i == 2:
        continue  # This will skip the rest of the code in the loop for this iteration
    print(i)
 
'''
Output:
0
1
3
4
'''   
# break statement
for i in range(5):
    if i == 2:
        break  # This will exit the loop completely
    print(i)
'''
Output:
0
1
'''    

# --------------------------------------------------

for i in range(1, 8):
    if i % 2 == 0:
        continue
    print(i)

'''
Output:
1
3
5
7
'''

for i in range(1, 10):
    if i % 3 == 0:
        break
    print(i)
    
'''
Output:
1
2
'''


for i in range(1, 5):
    if i == 2:
        continue
    elif i == 4:
        break
    print(i)
    
'''
Output:
1
3
'''

# ---------------------------------------------------

'''
Exercise:
Write a program to check whether a given number is prime or not.
'''

num = int(input("Enter a number: "))
if num > 1:
    for i in range(2, num):
        if (num % i) == 0:
            print(num, "is not a prime number")
            break
    else:
        print(num, "is a prime number")
else:
    print(num, "is not a prime number")
    

# ---------------------------------------------------

'''
Exercise:
Write a program to print all the prime numbers between 1 and 100.
'''

for num in range(1, 101):
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                break
        else:
            print(num)
            
# ---------------------------------------------------

''' 
Exercise:
Write a program to check armstrong number or not.
An armstrong number is a number that is equal to the sum of its own digits raised to the power of the number of digits.
For example, 153 is an armstrong number because 1^3 + 5^3 + 3^3 = 153.
'''
num = int(input("Enter a number: "))
order = len(str(num))
sum = 0
temp = num
while temp > 0:
    digit = temp % 10
    sum += digit ** order
    temp //= 10
if num == sum:
    print(num, "is an armstrong number")
else:
    print(num, "is not an armstrong number")
    
    
# ---------------------------------------------------

'''
Exercise:
Write a program to print the Fibonacci series up to n terms.
The Fibonacci series is a series of numbers where each number is the sum of the two preceding ones, usually starting with 0 and 1.
For example, the first 10 terms of the Fibonacci series are:
0, 1, 1, 2, 3, 5, 8, 13, 21, 34
'''

n = int(input("Enter the number of terms: "))
a, b = 0, 1
for i in range(n):
    print(a, end=' ')
    a, b = b, a + b

# ---------------------------------------------------

'''
Exercise:
Write a program to find the factorial of a given number.
factorial of a non-negative integer n is the product of all positive integers less than or equal to n.
For example, the factorial of 5 is 5! = 5 * 4 * 3 * 2 * 1 = 120.
'''    

num = int(input("Enter a number: "))
factorial = 1
if num < 0:
    print("Factorial does not exist for negative numbers")
elif num == 0:
    print("The factorial of 0 is 1")
else:
    for i in range(1, num + 1):
        factorial *= i
    print("The factorial of", num, "is", factorial)
    
# The same can be done using recursion as well
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

num = int(input("Enter a number: "))
if num < 0:
    print("Factorial does not exist for negative numbers")
elif num == 0:
    print("The factorial of 0 is 1")
else:
    print("The factorial of", num, "is", factorial(num))
   
# ---------------------------------------------------

'''
Exercise:
Interview Question:
1. Write a program to find the largest and smallest number in a list.
2. Write a program to find the second largest number in a list.
3. Write a program to find the common elements between two lists.
4. Write a program to remove duplicates from a list.
5. Write a program to check if a list is empty or not.
'''

# 1
numbers = [3, 5, 1, 2, 4]
largest = max(numbers)
smallest = min(numbers)
print("Largest number:", largest)
print("Smallest number:", smallest)

# 2
numbers = [3, 5, 1, 2, 4]
largest = max(numbers)
second_largest = max(num for num in numbers if num != largest)
print("Second largest number:", second_largest)

# 3
list1 = [1, 2, 3, 4, 5]
list2 = [4, 5, 6, 7, 8]
common_elements = set(list1) & set(list2)
print("Common elements:", common_elements)

# 4
numbers = [1, 2, 3, 4, 5, 2, 3]
unique_numbers = list(set(numbers))
print("Unique numbers:", unique_numbers)

# 5
my_list = []
if not my_list:
    print("The list is empty")
else:
    print("The list is not empty")
    
# ---------------------------------------------------


 

