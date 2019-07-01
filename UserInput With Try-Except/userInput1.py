"""
    In this program we use user input.
    And we also user Exception Handling to handel error

"""

print("Type integers, each followed by Enter: or just Enter to  finish")
total = 0
count = 0

while True:
       try:
           line = input()
           if line:
               number = int(line)
               total += number
               count += 1
       except ValueError as err:
           print(err)
           continue
       except EOFError:  # CTRL + D or CTRL + Z
           break

if count:
    print("Count =", count, "Total =", total, "mean =", total/count)