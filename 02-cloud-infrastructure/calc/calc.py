#!/usr/local/bin/python3

import cgi

# Create an HTML form
form = cgi.FieldStorage()

# Get the values of the GET parameters
a = form.getvalue('a')
b = form.getvalue('b')
op = form.getvalue('op')

# Check if the parameters are valid
if not a or not b or not op:
    print("Error: Missing parameters")
    exit()

# Perform the operation
result = 0
if op == 'add':
    result = float(a) + float(b)
elif op == 'sub':
    result = float(a) - float(b)
elif op == 'mul':
    result = float(a) * float(b)
elif op == 'div':
    if float(b) == 0:
        print("Error: Division by zero")
        exit()
    result = float(a) / float(b)
else:
    print("Error: Invalid operation")
    exit()

# Print the result
print("Content-type: text/plain")
print("")
print(result)
