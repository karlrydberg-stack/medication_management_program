import datetime

class Medication:
    def __init__(self, name, cash, storage = {}, archive_node = None):
        self.name = name
        self.cash = cash
        self.storage = storage
        self.archive_node = archive_node
        
    def reg_med(self):
        try:
            article_number = input("Article number: ")
            if article_number in self.storage:
                raise ValueError("An existing product with an identical article number already found in storage")
            price = float(input("Price: "))
            if price < 0:
                raise ValueError("Price must be a positive number")
            else:
                manufacturer = input("Manufacturer: ")
                self.storage[article_number] = {}
                self.storage[article_number]["Quantity"] = 0
                self.storage[article_number]["Price"] = price
                self.storage[article_number]["Manufacturer"] = manufacturer
                print(f"'{article_number}' has been registered")
                if self.archive_node:
                    string = f"{self.name} registered article '{article_number}'. Price: {price}, Manufacturer: {manufacturer}"
                    self.archive_node.action(string)
        except ValueError as ve:
            print(f"ERROR: {ve}")
        
    def del_med(self):
        try:
            article_number = input("Article number: ")
            if article_number not in self.storage:
                raise ValueError("Article number not found in storage")
            quantity = float(input("Quantity: "))
            if quantity < 0:
                raise ValueError("Quantity must be a positive number")
            else:
                if self.storage[article_number]["Quantity"] - quantity < 0:
                    raise ValueError("Insufficient balance")
                elif self.storage[article_number]["Quantity"] - quantity == 0:
                    del self.storage[article_number]
                    print(f"'{article_number}' has been deleted")
                    if self.archive_node:
                        string = f"{self.name} deleted '{article_number}'"
                        self.archive_node.action(string)
                elif self.storage[article_number]["Quantity"] - quantity > 0:
                    self.storage[article_number]["Quantity"] -= quantity
                    print(f"{quantity} of '{article_number}' has been removed")
                    if self.archive_node:
                        string = f"{self.name} scrapped {quantity} of '{article_number}'"
                        self.archive_node.action(string)
        except ValueError as ve:
            print(f"ERROR: {ve}")

    def buy_med(self):
        try:
            article_number = input("Article number: ")
            if article_number not in self.storage:
                raise ValueError("This article has not been registered in storage")
            quantity = float(input("Quantity: "))
            if quantity < 0:
                raise ValueError("Quantity must be a positive number")
            if self.cash - self.storage[article_number]["Price"] * quantity < 0:
                raise ValueError("Insufficient cash balance")
            else:
                self.storage[article_number]["Quantity"] += quantity
                self.cash -= self.storage[article_number]["Price"] * quantity
                print(f"{quantity} of '{article_number}' has been bought")
                if self.archive_node:
                    string = f"{self.name} bought {quantity} of '{article_number}'"
                    self.archive_node.action(string)
        except ValueError as ve:
            print(f"ERROR: {ve}")
    
    def sell_med(self):
        try:
            article_number = input("Article number: ")
            if article_number not in self.storage:
                raise ValueError("This article has not been registered in storage")
            quantity = float(input("Quantity: "))
            if quantity < 0:
                raise ValueError("Quantity must be a positive number")
            if self.storage[article_number]["Quantity"] - quantity < 0:
                raise ValueError("Insufficient balance")
            else:
                self.storage[article_number]["Quantity"] -= quantity
                self.cash += quantity * self.storage[article_number]["Price"]
                print(f"{quantity} of '{article_number}' has been sold")
                if self.archive_node:
                    string = f"{self.name} sold {quantity} of '{article_number}'"
                    self.archive_node.action(string)
        except ValueError as ve:
            print(f"ERROR: {ve}")

    def check_balance(self):
        print(f"Storage: {self.storage}.\nCash: {self.cash}")

    def run(self):
        print("Running...")
        print("Welcome to the Medication Management System!")
        if self.archive_node:
            self.archive_node.open_store(self.name, self.cash, self.storage)
        while True:
            try:
                print("1. Register medication\n2. Delete medication\n3. Buy medication\n4. Sell medication\n5. Check balance\n6. Quit")
                user_choice = input("Choose: ")
                if user_choice not in ["1", "2", "3", "4", "5", "6"]:
                    raise ValueError("invalid alternative")
                if user_choice == "1":
                    self.reg_med()
                elif user_choice == "2":
                    self.del_med()
                elif user_choice == "3":
                    self.buy_med()
                elif user_choice == "4":
                    self.sell_med()
                elif user_choice == "5":
                    self.check_balance()
                elif user_choice == "6":
                    if self.archive_node:
                        self.archive_node.close_store(self.name, self.cash, self.storage)
                    print("Quitting...")
                    break
            except ValueError as ve:
                print(f"ERROR: {ve}")

class Archiver:
    def open_store(self, name, cash, storage):
        try:
            with open("log.txt", "x") as file:
                pass
        except FileExistsError:
            pass    
        with open("log.txt", "a") as file:
            opening_time = datetime.datetime.now()
            full_sentence = f"{name} just opened the store on {opening_time}. Cash: {cash}, Storage: {storage}\n"
            file.write(full_sentence)
            
    def close_store(self, name, cash, storage):
        with open("log.txt", "a") as file:
            closing_time = datetime.datetime.now()
            full_sentence = f"{name} closed the store on {closing_time}. Cash: {cash}, Storage: {storage}\n"
            file.write(full_sentence)
    
    def action(self, string):
        with open("log.txt", "a") as file:
            current_time = datetime.datetime.now()
            full_sentence = f"{current_time} {string}\n"
            file.write(full_sentence)