import csv
import os
import time

class Warehouse:
    next_id = 1
    def __init__(self, item_name=None):
        self.item_id = Warehouse.next_id
        Warehouse.next_id += 1
        self.item_name = item_name

    def input_data(self):
        self.item_name = input("Give your Warehouse a name: ")

class WarehouseDatabase:
    def __init__(self):
        self.warehouse_items = []

    def add_warehouse(self, item):
        self.warehouse_items.append(item)

    def check_warehouse(self, item_name):
        for item in self.warehouse_items:
            if item.item_name == item_name:
                print('This warehouse already exist')
                return True
        return False

    def edit_item(self, item_name):
        item_name = input('Enter the Warehouse name that you want to edit: ')
        for item in self.warehouse_items:
            if item.item_name == item_name:
                item.input_data()
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
                print ("Successfully!")
                time.sleep(1)
                return True
        print("Item Name not found")
        time.sleep(2)
        return False

    def show_item(self):
        print("Warehouse Database:")
        print("{:<10} {:<20}".format("ID", "Item Name"))
        for item in self.warehouse_items:
            print("{:<10} {:<20}".format(item.item_id, item.item_name))

    def save_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Item ID', 'Item Name'])
            for item in self.warehouse_items:
                writer.writerow([item.item_id, item.item_name])

    def load_from_csv(self, filename):
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                item = Warehouse(item_name=row['Item Name'])
                item.item_id = int(row['Item ID'])  # Assigning the loaded ID
                self.add_warehouse(item)

class Route:
    next_id = 1
    def __init__(self):
        self.item_id = Route.next_id
        Route.next_id += 1
        self.origin = None
        self.destination = None
        self.cost = None

    def input_data(self):
        self.origin = input("Send from: ")
        self.destination = input("Send to: ")
        self.cost = float(input("Delivery Cost: "))

class RouteDatabase:
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
                print('Please change your Warehouse name or edit Warehouse')
                Warehouse.next_id -= 1
                time.sleep(2)
                os.system('cls')
        if c == '2':
            db.edit_item(None)
            os.system('cls')
        if c == '3':
            db.remove_item(None)
            os.system('cls')
        # No 4 not work properly
        while c == '4':
            item = Route()
            item.input_data()
            rdb.add_route(item)
            break;
        #if c == '5':

        #if c == '6':

        #if c == '7':

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
