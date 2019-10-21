import distances
import Package
import datetime
from datetime import time
from datetime import timedelta

class Truck:
    def __init__(self, inventory, speed, miles, count, name, packages, time):
        self.inventory = inventory
        self.speed = speed
        self.miles = miles
        self.count = count
        self.name = name
        self.packages = packages
        self.time = time

truck1Packages = []
truck2Packages = []
speed = 18
inventory1 = []
inventory2 = []
count1 = 0
count2 = 0
miles1 = 0
miles2 = 0
time1 = timedelta(hours = 9, minutes = 5)
time2 = timedelta(hours = 8, minutes = 0)
simTime = timedelta(hours = 8, minutes = 0)
maxSize = 16

truck1 = Truck(inventory1, speed, miles1, count1, "TRUCK 1", truck1Packages, time1)
truck2 = Truck(inventory2, speed, miles2, count2, "TRUCK 2", truck2Packages, time2)

packageList = Package.packageList
addressList = distances.addressList

# This is a lookup function as required by the project rubric
def lookUpPackage(id):
    for i in packageList:
        if (i.id == id):
            print()
            print ("Package ID: " + i.id)
            print ("Package address: " + i.address)
            print ("Package deadline: " + i.deadline)
            print ("Package zipCode: " + i.zipCode)
            print ("Package weight: " + i.weight)
            print ("Package status: " + i.status)
            print ("Delivery Time: " + str(i.deliveryTime))
            print ("Package notes: " + i.notes) 

# Print functions to show interface and simulation
# ================================================
def printPackageList():
    print('{:2}'.format("ID"), '{:40}'.format("Address"), '{:50}'.format("Deadline"), '{:55}'.format("Status"), '{:55}'.format("Delivery Time"))
    for i in range(len(packageList)):
        print('{:2}'.format(packageList[i].id), '{:40}'.format(packageList[i].address), '{:50}'.format(packageList[i].deadline), '{:50}'.format(packageList[i].status), '{:60}'.format(str(packageList[i].deliveryTime)))

def printTruckStatus(Truck):
    print("-"*20)
    print("-"*10 + Truck.name + "-"*10)
    print('{:2}'.format("ID"), '{:40}'.format("Address"), '{:50}'.format("Deadline"), '{:55}'.format("Status"), '{:50}'.format("Delivery Time"))
    for i in range(len(Truck.inventory)):
                print('{:2}'.format(Truck.inventory[i].id), 
                '{:40}'.format(Truck.inventory[i].address), 
                '{:50}'.format(Truck.inventory[i].deadline), 
                '{:50}'.format(Truck.inventory[i].status), 
                '{:60}'.format(str(Truck.inventory[i].deliveryTime)))


    print()
    print("Carrying " + str(Truck.count) + " packages")
    print("-"*20)

def calculateDeliveredPackages():
    packagesDelivered = 0
    for i in range(len(packageList)):
        if packageList[i].status == "Delivered":
            packagesDelivered += 1
    return packagesDelivered

def lookUpMenu():
    print("Which package are you looking for?")
    choice = input("Enter a package ID: ")
    lookUpPackage(choice)
    printMenu()

def printMenu():
    choice = "0"
    while choice == "0":
        print()
        print("---------- WGUPS ----------")
        print("Current Time: " + str(simTime))
        print("Packages Delivered: " + str(calculateDeliveredPackages()))
        print("TOTAL MILES")
        print('{:10}'.format("Truck 1"), '{:10}'.format("Truck 2"), '{:10}'.format("Total"),)
        print('{:10}'.format(str(int(truck1.miles))), '{:10}'.format(str(int(truck2.miles))), '{:10}'.format(str(int(truck1.miles + truck2.miles))))
        print()
        print('{:10}'.format("1. Run Simulation one Hour"))
        print('{:10}'.format("2. Print Truck Status"))
        print('{:10}'.format("3. View all Packages"))
        print('{:10}'.format("4. Look up specific package"))
        print('{:10}'.format("5. Exit"))
        
        choice = input("USER INPUT:")
        if choice == "1":
            advanceSimulationOneHour()
        elif choice == "2":
            printTruckStatus(truck1)
            printTruckStatus(truck2)
            printMenu()
        elif choice == "3":
            printPackageList()
            printMenu()
        elif choice == "4":
            lookUpMenu()
        elif choice == "5":
            exit()
        else:
            print("Please enter a valid menu item")    

def printSimCompletion():
    print()
    print('{:10}'.format("----- PROGRAM COMPLETE: ALL PACKAGES DELIVERED ----"))
    print('{:10}'.format("Truck 1: "), '{:15}'.format("Miles: " + str(truck1.miles)))
    print('{:10}'.format("Truck 2: "), '{:15}'.format("Miles: " + str(truck2.miles)))
    print('{:10}'.format("Total "), '{:15}'.format(str(truck1.miles + truck2.miles)))
    print()
    print('{:10}'.format("Time of Completion: " + str(simTime)))
    print()
    printPackageList()

# Load Functions for putting packages on Trucks
# =============================================

# These two functions work by splitting the list of packages into two smaller
# earmarked lists dedicated to each truck. This simplifies loading.

def loadTruck1PackageList():
    # Truck 1 handles all other packages that are left over from truck 2.
    temp = [2, 4, 6, 11, 12, 17, 21, 23, 24, 25, 27, 28, 31, 32, 33, 35]
    for i in range(len(packageList)):
        if int(packageList[i].id) in temp:
            truck1.packages.append(packageList[i])

def loadTruck2PackageList():
    # Truck 2 is loaded with all priority packages as well as all packages with special notes
    temp = [1, 3, 5, 7, 8, 9, 10, 13, 14, 15, 16, 18, 19, 20, 22, 26, 29, 30, 34, 36, 37, 38, 39, 40]
    for i in range(len(packageList)):
         if int(packageList[i].id) in temp:
            truck2.packages.append(packageList[i])

def loadClosestPackageWithDeadline(Truck):
    # This function takes the previous package in the list and searches the sorted package list for the next closest package. This function considers deadlines.
    sortedList = sortAddressesByDistance(truck2.inventory[-1].distanceDict)
    for i in range(len(sortedList)):
        for j in range(len(Truck.packages)):
            if (sortedList[i] == Truck.packages[j].address) and (Truck.packages[j].status == "Not Delivered") and (Truck.packages[j].deadline != "EOD") and (Truck.packages[j].notes != "Wrong address listed") and (Truck.count < maxSize):
                Truck.packages[j].status = "In Transit"
                Truck.inventory.append(Truck.packages[j])
                Truck.count += 1
                loadPackagesWithSameAddress(Truck)

def findPackageClosestToHub(Truck):
    # This function locates the closest package without a delivery date to the hub
    sortedAddressList = sorted(addressList[0], key=addressList[0].get, reverse=False)
    check = 0
    while check == 0:
        address = sortedAddressList.pop(0)
        for i in range(len(Truck.packages)):
            if (address == Truck.packages[i].address) and (Truck.packages[i].status == "Not Delivered"):
                Truck.packages[i].status = "In Transit"
                return Truck.packages[i]
                break

def findPackageWithDeliveryClosestToHub(Truck):
    # This function locates the closest package with a delivery date to the hub
    sortedAddressList = sorted(addressList[0], key=addressList[0].get, reverse=False)
    check = 0
    while check == 0:
        address = sortedAddressList.pop(0)
        for i in range(len(Truck.packages)):
            if (address == Truck.packages[i].address) and (Truck.packages[i].status == "Not Delivered") and (Truck.packages[i].deadline != "EOD"):
                Truck.packages[i].status = "In Transit"
                return Truck.packages[i]
                break

def loadPackage19():
    # package 19 has a special not but no other unique attributes, so it must be handled by itself. It will be loaded onto the same truck as the other
    # identified packages in the notes.
    if (truck2Packages[12].status == "Not Delivered"):
        sortedAddressList = sorted(truck2Packages[12].distanceDict, key=truck2Packages[12].distanceDict.get)
        for i in range(len(sortedAddressList)):
            for j in range(len(truck2.inventory)):
                if (sortedAddressList[i] == truck2.inventory[j].address) and (truck2Packages[12].status == "Not Delivered"):
                    truck2Packages[12].status = "In Transit"
                    truck2.inventory.insert(j+1, truck2Packages[12])
                    truck2.count += 1
                    if truck2.count > 16:
                        truck2.inventory[-1].status = "Not Delivered"
                        truck2.inventory.pop(-1)
                        truck2.count -= 1
                    break

def sortAddressesByDistance(dict):
    # this function sorts packages by distance
    sortedAddressList = sorted(dict, key=dict.get)
    return sortedAddressList

def loadPackagesWithSameAddress(Truck):
    # This is a vital function. Everytime a package is loaded, the list is searched for any packages going to the same address.
    for i in range(len(Truck.inventory)):
        for j in range(len(Truck.packages)):
            if (Truck.packages[j].address == Truck.inventory[i].address) and (Truck.packages[j].status == "Not Delivered") and (Truck.count < maxSize) and (Truck.packages[j].notes != "Wrong address listed"):
                Truck.inventory.append(Truck.packages[j])
                Truck.packages[j].status = "In Transit"
                Truck.count += 1

def loadClosestPackage(Truck):
    # This function takes the previous package in the list and searches the sorted package list for the next closest package. This function doesn't considers deadlines.
    sortedList = sortAddressesByDistance(Truck.inventory[-1].distanceDict)
    for i in range(len(sortedList)):
        for j in range(len(Truck.packages)):
            if (sortedList[i] == Truck.packages[j].address) and (Truck.packages[j].status == "Not Delivered") and (Truck.packages[j].deadline == "EOD") and (Truck.count < maxSize):
                Truck.packages[j].status = "In Transit"
                Truck.inventory.append(Truck.packages[j])
                Truck.count += 1
                loadPackagesWithSameAddress(Truck)

def loadTruck1():
    # This function sets the initial conditions for truck 1
    truck1.inventory.clear()
    p = findPackageWithDeliveryClosestToHub(truck1)
    truck1.inventory.append(p)
    truck1.count += 1
    loadPackagesWithSameAddress(truck1)
    loadClosestPackageWithDeadline(truck1)
    loadClosestPackage(truck1)

def loadTruck2():
    # This function sets the initial conditions for truck 2
    truck2.inventory.clear()
    p = findPackageWithDeliveryClosestToHub(truck2)
    truck2.inventory.append(p)
    truck2.count += 1
    loadPackagesWithSameAddress(truck2)
    loadClosestPackageWithDeadline(truck2)
    loadPackage19()
    
def loadPackagesWithDeliveryDates(Truck):
    for i in range(len(packageList)):
        if (packageList[i].deadline != "EOD") and (packageList[i].status == "Not Delivered") and (packageList[i].notes != "Wrong address listed") and (Truck.count < maxSize):
            Truck.inventory.append(packageList[i])
            packageList[i].status = "In Transit"
            Truck.count += 1
            loadPackagesWithSameAddress(Truck)

# The Following function handles the delivery of all packages
# ===========================================================

def deliverPackages(Truck):
    for i in range(len(Truck.inventory)):
        # Check that the next package in the list has not been delivered yet
        # Also check that the first package has been delivered. This is necessary because otherwise the
        # algorithm for distance and time wont accurately be reflected. The first package must've been delivered
        # in order for the loop to have a previous iteration to reference.
        if (Truck.inventory[i].status != "Delivered"):
            # Find the distance to the next address
            if i == 0:
                distance = distances.address1[Truck.inventory[i].address]
                if ((Truck.time + timedelta(minutes = ((distance/Truck.speed)*60)) <= simTime)):                    
                    Truck.miles += distance
                    Truck.time += timedelta(minutes = ((distance/Truck.speed)*60))
                    Truck.inventory[i].status = "Delivered"
                    Truck.inventory[i].deliveryTime = Truck.time
                    print()
                    print("Address: " + str(Truck.inventory[i].address))
                    print("Distance: " + str(distance))
                    print("truck miles = " + str(Truck.miles))
                    print("Truck Time= " + str(Truck.time))
                    print("Package: " + Truck.inventory[i].id + " delivered")
            elif (Truck.inventory[i].address == Truck.inventory[i-1].address) and (Truck.inventory[i-1].status == "Delivered"):
                distance = 0
            elif (Truck.inventory[i].address != Truck.inventory[i-1].address) and (Truck.inventory[i-1].status == "Delivered"):
                distance = (Truck.inventory[i-1].distanceDict[Truck.inventory[i].address])
            
            # Check if the truck will make it to the next location before the next tick of the timer
            if ((Truck.time + timedelta(minutes = ((distance/Truck.speed)*60)) <= simTime)) and (Truck.inventory[i-1].status == "Delivered"):
                Truck.miles += distance
                Truck.time += timedelta(minutes = ((distance/Truck.speed)*60))
                Truck.inventory[i].status = "Delivered"
                Truck.inventory[i].deliveryTime = Truck.time
                print()
                print("Address: " + str(Truck.inventory[i].address))
                print("Distance: " + str(distance))
                print("truck miles = " + str(Truck.miles))
                print("Truck Time= " + str(Truck.time))
                print("Package: " + Truck.inventory[i].id + " delivered")

# The following functions handle boolean operations such as checking
# if packages are left or if a truck needs to return to the hub, or if
# the simulation has been completed
# ====================================================================

def returnToHub(Truck):
    # Check to see if Truck is already back at Hub.
    # This is necessary since this function is checked every tick of the timer
    # and if the inventory of a truck has been cleared, then it will throw an exception
    if (Truck.inventory):
        allDelivered = True
        for i in range(len(Truck.inventory)):
            if Truck.inventory[i].status != "Delivered":
                allDelivered = False

        if allDelivered:
            # Get distance back to Hub
            distance = distances.address1[Truck.inventory[-1].address]
            if ((Truck.time + timedelta(minutes = ((distance/Truck.speed)*60)) <= simTime)):
                Truck.miles += distance
                Truck.time += timedelta(minutes = ((distance/Truck.speed)*60))
                return True

def checkForUndeliveredPackages(Truck):
    check = False
    for i in range(len(Truck.packages)):
        if Truck.packages[i].status != "Delivered":
            check = True
    return check

def checkForSimulationCompletion():
    for i in range(len(packageList)):
        if packageList[i].status != "Delivered":
            return False
    return True

# The following functions handle the simulation
# =============================================

def advanceSimulationOneHour():
    global simTime
    timer = simTime + timedelta(hours = 1)
    if (checkForSimulationCompletion()):
        printSimCompletion()
    else:
        while simTime < timer:

            # Check if wrong address is corrected
            if (simTime >= timedelta(hours = 10, minutes = 20)):
                truck2Packages[5].address = "410 S State St"
            # Check if the delayed packages have arrive since that is when truck 1 leaves the HUB
            if (simTime >= timedelta(hours = 9, minutes = 5)):
                deliverPackages(truck1)
            deliverPackages(truck2)

            # Check if either Truck needs to return to hub and load more packages:
            if(returnToHub(truck1)):
                print("Truck 1 returning to Hub")
                truck1.inventory.clear()
                truck1.count = 0
                if (checkForUndeliveredPackages(truck1)):
                    p = findPackageClosestToHub(truck1)
                    truck1.inventory.append(p)
                    truck1.count += 1
                    loadClosestPackage(truck1)
            if(returnToHub(truck2)):
                truck2.inventory.clear()
                truck2.count = 0
                if (checkForUndeliveredPackages(truck2)):
                    p = findPackageClosestToHub(truck2)
                    truck2.inventory.append(p)
                    truck2.count += 1
                    loadClosestPackage(truck2)

            simTime += timedelta(minutes = 5)
        printMenu()

def startSimulation():

    # The packages have been divided into two lists, one for each truck. This not only makes the lists smaller and easier to do computations on, but also simplifies
    # the loading and delivery for each truck.
    loadTruck1PackageList()
    loadTruck2PackageList()

    # The loading algorithm goes as follows:
    # 1a. The package with the earliest deadline is selected and loaded
    # 1b. If the packages with a deadline are equal, then the closest is selected and loaded
    # 2. Any packages going to the same location are selected and loaded
    # 3. The program finds the closest location with a package that has a deadline
    # 4. The program finds, selects, and loads any packages going to that same location
    # 5. If there are no more packages with deadlines to select, the program simply choses the next package by closest location.
    # 6. Any packages going to the same location are selected and loaded.

    # Load The Trucks
    loadTruck2()
    loadTruck1()
    printMenu()


# Program Start
def main():
    startSimulation()

main()