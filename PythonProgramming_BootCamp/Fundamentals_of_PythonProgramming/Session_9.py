# --------------------------------------------------
# Session 9: Fundamentals of Python Programming
# --------------------------------------------------
## Author: Chandan Chaudhari
## Github: https://github.com/chandanc5525
# --------------------------------------------------

# Concept of Zip and Unzip in Python Programming

# Zip Function
list1 = [1, 2, 3]
list2 = ['a', 'b', 'c']
zipped = zip(list1, list2)
print(list(zipped))  
# Output: [(1, 'a'), (2, 'b'), (3, 'c')]

# Unzip Function
zipped = [(1, 'a'), (2, 'b'), (3, 'c')]
unzipped = zip(*zipped)
print(list(unzipped))
# Output: [(1, 2, 3), ('a', 'b', 'c')]

# Use case of Zip and Unzip : Real life example of Zip and Unzip in Python Programming

''' 
Scenario: Indian Railway Reservation System

Ask user to enter the number of passengers, and then for each passenger, ask for their name and age.
Then, use the zip function to combine the names and ages into a list of tuples, and print the result.
'''

# %%
# Get number of passengers
num_passengers = int(input("Enter the number of passengers: "))

# Initialize empty lists for names and ages
names = []
ages = []

# Get passenger details
for i in range(num_passengers):
    name = input(f"Enter the name of passenger {i+1}: ")
    age = int(input(f"Enter the age of passenger {i+1}: "))
    names.append(name)
    ages.append(age)
    
# Zip names and ages into a list of tuples
passenger_details = zip(names, ages)
# Print the passenger details
print("Passenger Details:")
for name, age in passenger_details:
    print(f"Name: {name}, Age: {age}")
    
''' 
Output:
Enter the number of passengers: 5
Enter the name of passenger 1: Chandan
Enter the age of passenger 1: 25
Enter the name of passenger 2: Anjali
Enter the age of passenger 2: 22
Enter the name of passenger 3: Rohan
Enter the age of passenger 3: 30
Enter the name of passenger 4: Priya
Enter the age of passenger 4: 28
Enter the name of passenger 5: Rahul
Enter the age of passenger 5: 27

Passenger Details:
Name: Chandan, Age: 25
Name: Anjali, Age: 22
Name: Rohan, Age: 30
Name: Priya, Age: 28
Name: Rahul, Age: 27

'''
