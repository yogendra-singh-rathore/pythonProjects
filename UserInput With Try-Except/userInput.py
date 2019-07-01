"""
    In this program we use user input.
    And we also user Exception Handling to handel error

"""

print("Type integers, each followed by Enter: or just Enter to  finish")
total = 0
count = 0

while True:
    #  user input assign in "line"
    line = input("integer: ")
    # we are using if condition for checking using enter " Integer or String "
    if line:
        # Exception Handling if user enter Integer then it will pass else it show error
        try:
            number = int(line)
        except ValueError as err:
            print(err)
            # Here we user continue to skip this error part so count didn't  include it.
            continue
        total += number
        count += 1
    # To end this loop Just press Enter with passing any value
    else:
        break

if count:
    print("Count =", count, "Total =", total, "mean =", total/count)