import csv
import os
import time

class Warehouse:
    next_id = 1
    def __init__(self, item_name=None, item_location=None, item_capacity=None):
        self.item_id = Warehouse.next_id
        Warehouse.next_id += 1
        self.item_name = item_name
        self.item_location = item_location
        self.item_capacity = item_capacity

    def input_data(self):
        self.item_name = input('Give your Warehouse a name: ')
        self.item_location = input('Enter the location of your warehouse: ')
        self.item_capacity = input('Your warehouse capacity (%): ')

    def apply_edit_data(self, item_name, item_location, item_capacity):
        self.item_name = item_name
        self.item_location = item_location
        self.item_capacity = item_capacity

class WarehouseDatabase:
    name_old = None # For Route change after edit warehouse
    name_new = None
    def __init__(self):
        self.warehouse_items = []

    def add_warehouse(self, item):
        self.warehouse_items.append(item)

    def check_warehouse(self, item_name):
        for item in self.warehouse_items:
            if item.item_name == item_name:
                return True
        return False

    def edit_item(self, item_name):
        item_name = input('Enter the Warehouse name that you want to edit: ')
        new_name = item_name
        new_location = None
        new_capacity = None
        for item in self.warehouse_items:
            if item.item_name == item_name:
                while self.check_warehouse(new_name):
                    os.system('cls')
                    new_name = input('Enter a new name: ')
                    new_location = input('Enter the location of your warehouse: ')
                    new_capacity = input('Your warehouse capacity (%): ')
                    if self.check_warehouse(new_name):
                        print('This warehouse already exist')
                        time.sleep(2)
                self.name_old = item_name
                self.name_new = new_name
                item.apply_edit_data(new_name,new_location,new_capacity)
                print ("Successfully!")
                time.sleep(1)
                return True
        print("Item Name not found")
        time.sleep(2)
        return False

    def remove_item(self, item_name):
        item_name = input('Enter the Warehouse name that you want to remove: ')
        for item in self.warehouse_items:
            if item.item_name == item_name:
                self.warehouse_items.remove(item)
                self.name_old = item_name
                print ("Successfully!")
                time.sleep(1)
                return True
        print("Item Name not found")
        time.sleep(2)
        return False

    def show_item(self):
        print("Warehouse Database:")
        print("{:<10} {:<20} {:<20} {:<10}".format("ID", "Item Name", "Location", "Capacity"))
        for item in self.warehouse_items:
            print("{:<10} {:<20} {:<20} {:<10}".format(item.item_id, item.item_name, item.item_location, item.item_capacity))

    def save_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Item ID', 'Item Name', 'Item Location', 'Item Capacity'])
            for item in self.warehouse_items:
                writer.writerow([item.item_id, item.item_name, item.item_location, item.item_capacity])

    def load_from_csv(self, filename):
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                item = Warehouse(item_name=row['Item Name'])
                item.item_id = int(row['Item ID'])
                item.item_location = row['Item Location']
                item.item_capacity = float(row['Item Capacity'])
                self.add_warehouse(item)

class Route:
    next_id = 1
    def __init__(self):
        self.item_id = Route.next_id
        Route.next_id += 1
        self.origin = None
        #self.origin_location = None
        self.destination = None
        #self.destination_location = None
        self.cost = None

    def input_data(self):
        self.origin = input("Send from: ")
        self.destination = input("Send to: ")
        self.cost = float(input("Delivery Cost: "))

    def apply_new_cost(self):
        self.cost = float(input("Enter new delivery cost: "))

class RouteDatabase:
    db = WarehouseDatabase()
    db.load_from_csv("warehouse_database.csv")
    def __init__(self):
        self.routes = []

    def add_route(self, route):
        self.routes.append(route)

    def check_route(self,origin,destination):
        for item in self.routes:
            # Check if already exist
            if item.origin == origin and item.destination == destination:
                print('This route already exist')
                return True
            # Check origin and destination
            check_origin = False
            check_destination = False
            for w_item in db.warehouse_items:
                if origin == w_item.item_name:
                    check_origin = True
                if destination == w_item.item_name:
                    check_destination = True
            if not check_destination or not check_origin:
                print('Some of your warehouses does not exist')
                print('Please add a new warehouse or enter another route')
                return True
            # Check origin same destination
            if origin == destination:
                print('Please enter another destination')
                return True

    def edit_route(self, item_id):
        item_id = int(input('Enter the ID of the Route that you want to edit delivery cost: '))
        for item in self.routes:
            if item.item_id == item_id:
                item.apply_new_cost()
                print("Successfully!")
                time.sleep(1)
                return True
        print("Route ID not found")
        time.sleep(2)
        return False


    def remove_item(self, item_id):
        item_id = int(input('Enter the ID of the Route that you want to remove: '))
        for item in self.routes:
            if item.item_id == item_id:
                self.routes.remove(item)
                print ("Successfully!")
                time.sleep(1)
                return True
        print("Route ID not found")
        time.sleep(2)
        return False

    # Applying changes from edited warehouses
    def apply_warehouse_edit(self, old_name, new_name):
        for item in self.routes:
            if item.origin == old_name:
                item.origin = new_name
            if item.destination == old_name:
                item.destination = new_name

    # Applying removed warehouse
    def apply_warehouse_remove(self, name):
        for route in self.routes[:]:
            if route.origin == name or route.destination == name:
                self.routes.remove(route)

    def show_item(self):
        print("Transportation Network:")
        print("{:<10} {:<20} {:<20} {:<10}".format("ID", "Origin", "Destination", "Cost"))
        for item in self.routes:
            print("{:<10} {:<20} {:<20} {:<10}".format(item.item_id, item.origin, item.destination, item.cost))

    def save_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID','From','To','Cost'])# ...
            for route in self.routes:
                writer.writerow([route.item_id,route.origin, route.destination, route.cost])

    def load_from_csv(self, filename):
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                route = Route()
                route.origin = row['From']
                route.destination = row['To']
                route.cost = float(row['Cost'])
                route.item_id = int(row['ID'])
                self.add_route(route)

# Shortest route algorithm
class Pair:
    def __init__(self, first, second):
        self.first = first
        self.second = second

class Node:

    def __init__(self, vertexNumber):
        self.vertexNumber = vertexNumber
        self.children = []

    def Add_child(self, vNumber, length):
        p = Pair(vNumber, length)
        self.children.append(p)

# Function to find the distance
def dijkstraDist(g, s, path):
    dist = [float('inf') for i in range(len(g))]
    visited = [False for i in range(len(g))]

    for i in range(len(g)):
        path[i] = -1
    dist[s] = 0
    path[s] = -1
    current = s
    sett = set()
    while (True):
        visited[current] = True
        for i in range(len(g[current].children)):
            v = g[current].children[i].first
            if (visited[v]):
                continue
            sett.add(v)
            alt = dist[current] + g[current].children[i].second
            if (alt < dist[v]):
                dist[v] = alt
                path[v] = current
        if current in sett:
            sett.remove(current)
        if (len(sett) == 0):
            break
        minDist = float('inf')
        index = 0
        for a in sett:
            if (dist[a] < minDist):
                minDist = dist[a]
                index = a
        current = index
    return dist

# Function to print the shortest path
def printPath(path, i, s):
    if (i != s):
        if (path[i] == -1):
            print("No available routes")
            return
        printPath(path, path[i], s)
        for item in db.warehouse_items:
            if path[i] == item.item_id:
                print(item.item_name ,end=" => ")
def menu():
    c = ''
    while c not in ['1','2','3','4','5','6','7','8','9','Q','q']:
        print()
        print('   PLEASE SELECT CODE FROM MENU  ')
        print('+-------------------------------+')
        print('| 1- Add Warehouse              |')
        print('| 2- Edit Warehouse             |')
        print('| 3- Remove Warehouse           |')
        print('| 4- Add Route                  |')
        print('| 5- Edit Delivery Cost         |')
        print('| 6- Delete Route               |')
        print('| 7- Find optimal route         |')
        print('| 8- Display Warehouses         |')
        print('| 9- Display Network            |')
        print('| Q- Quit                       |')
        print('+-------------------------------+')
        c = input('Your selection: ')
        os.system("cls")
    return c

if __name__ == "__main__":
    # Variables
    warehouse_file = "warehouse_database.csv"
    route_file = "route_database.csv"
    origin_id = destination_id = 0
    c = ''
    db = WarehouseDatabase()
    rdb = RouteDatabase()
    db.load_from_csv(warehouse_file)
    rdb.load_from_csv(route_file)
    # Main code
    print(' WELCOME TO WAREHOUSE MANAGER 1.0 ')
    while c != 'Q' and c != 'q':
        c = menu()
        while c == '1':
            item = Warehouse()
            item.input_data()
            if not db.check_warehouse(item.item_name):
                db.add_warehouse(item)
                print('Successfully!')
                time.sleep(1)
                os.system('cls')
                break;
            else:
                print('This warehouse already exist')
                print('Please change your Warehouse name or edit Warehouse')
                Warehouse.next_id -= 1
                time.sleep(2)
                os.system('cls')
        if c == '2':
            db.edit_item(None)
            rdb.apply_warehouse_edit(db.name_old, db.name_new)
            os.system('cls')
        if c == '3':
            db.remove_item(None)
            rdb.apply_warehouse_remove(db.name_old)
            Warehouse.next_id -= 1
            os.system('cls')
        while c == '4':
            item = Route()
            item.input_data()
            if not rdb.check_route(item.origin,item.destination):
                rdb.add_route(item)
                os.system('cls')
                break;
            else:
                Route.next_id -= 1
                time.sleep(2)
            os.system('cls')
        if c == '5':
            rdb.edit_route(None)
            os.system('cls')
        if c == '6':
            rdb.remove_item(None)
            os.system('cls')
        if c == '7':
            wares = Warehouse()
            origin = input('Go from: ')
            destination = input('Go to: ')
            stats = "Ready to go!" # For the capacity status
            v = []
            if not db.check_warehouse(origin) or not db.check_warehouse(destination):
                print('Some of the warehouses does not exist')
                time.sleep(2)
                os.system('cls')
                continue
            else:
                for item in range(wares.next_id-1):
                    a = Node(item)
                    v.append(a)
                for route in rdb.routes:
                    # Get the IDs
                    for item in db.warehouse_items:
                        if route.origin == item.item_name:
                            origin_id = item.item_id
                        if route.destination == item.item_name:
                            destination_id = item.item_id
                    v[origin_id].Add_child(destination_id, route.cost)
                # Get origin and destination ID's
                for item in db.warehouse_items:
                    if origin == item.item_name:
                        origin_id = item.item_id
                        if item.item_capacity == 0:
                            stats = "Nothing to delivery!"
                    if destination == item.item_name:
                        destination_id = item.item_id
                        if item.item_capacity == 100:
                            stats = "Destination Warehouse is full!"
                path = [0 for i in range(len(v))]
                distance = dijkstraDist(v,origin_id,path)
                # Print the cost
                print("Lowest cost from {} to {} is: {}".format(origin, destination, distance[destination_id]));
                # Print the path
                printPath(path,destination_id,origin_id)
                print(destination)
                # Print the status
                print("Status: ",stats)
                input('Done Reading? Press Enter to continue..')
                os.system('cls')
        if c == '8':
            db.show_item()
            print()
            input('Done Reading? Press Enter to continue..')
            os.system('cls')
        if c == '9':
            rdb.show_item()
            print()
            input('Done Reading? Press Enter to continue..')
            os.system('cls')

        db.save_to_csv(warehouse_file)
        rdb.save_to_csv(route_file)
    # Save the database to a CSV file
