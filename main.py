import json
import os
import msvcrt
from datetime import datetime, timedelta
from plants import PlantsDashboard
from add_plant_function import add_plant
import time

class PlantCareSystem:
    USER_DB = "users.json"
    PLANT_DB = "plants.json"
    REMINDER_DB = "reminders.json"
    MAINTENANCE_DB = "maintenance.json"

    def __init__(self):
        self.current_user = None

    def load_data(self, file):
        if not os.path.exists(file):
            return []
        with open(file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def save_data(self, file, data):
        with open(file, "w") as f:
            json.dump(data, f, indent=4)

    def get_password(self, prompt="Enter password: "):
        print(prompt, end="", flush=True)
        password = []
        while True:
            char = msvcrt.getch()
            if char == b"\r":
                print("")
                break
            elif char == b"\b": 
                if password:
                    password.pop()
                    print("\b \b", end="", flush=True)
            else:
                password.append(char.decode("utf-8"))
                print("*", end="", flush=True)
        return "".join(password)

    def generate_user_id(self):
        users = self.load_data(self.USER_DB)
        return max((user["user_id"] for user in users), default=0) + 1

    def register_user(self):
        users = self.load_data(self.USER_DB)
        user_id = self.generate_user_id()
        name = input("Enter name: ").strip()
        email = input("Enter email: ").strip()
        
        if not name or not email:
            print("⚠️ Name and email cannot be empty!")
            return
        
        if any(user["email"] == email for user in users):
            print("⚠️ Email already registered!")
            return
        
        if any(user["name"].lower() == name.lower() for user in users):
            print("⚠️ Username already taken!")
            return
        
        password = self.get_password("Enter password: ")
        if not password:
            print("⚠️ Password cannot be empty!")
            return
        
        users.append({"user_id": user_id, "name": name, "email": email, "password": password})
        self.save_data(self.USER_DB, users)
        print("✅ User registered successfully!")

    def login(self):
        users = self.load_data(self.USER_DB)
        email = input("Enter email: ").strip()
        password = self.get_password("Enter password: ")

        for user in users:
            if user["email"] == email and user["password"] == password:
                print(f"✅ Welcome back, {user['name']}!")
                self.current_user = user
                return True
        print("❌ Invalid email or password!")
        return False

    def remove_plant(self):
        plants = self.load_data(self.PLANT_DB)
        if not plants:
            print("⚠️ No plants available!")
            return

        print("📜 Plant List:")
        for plant in plants:
            print(f"{plant['plant_id']}. {plant['name']}")

        try:
            plant_id = int(input("Enter plant ID to remove: "))
            plants = [plant for plant in plants if plant["plant_id"] != plant_id]
            self.save_data(self.PLANT_DB, plants)
            print("✅ Plant removed successfully!")
        except ValueError:
            print("⚠️ Invalid input! Please enter a valid plant ID.")

    def show_added_plants(self):
        plants = self.load_data(self.PLANT_DB)
        if not plants:
            print("⚠️ No plants available!")
            return

        print("\n🌱 Added Plants List:\n")
        for plant in plants:
            print(f"🌿 Name: {plant['name']} | Water Schedule: {plant['water_schedule']} | Fertilize Schedule: {plant['fertilize_schedule']} | Harvest Schedule: {plant['harvest_schedule']}")
        input("\nPress enter to return to the dashboard...")
    
    def check_plant_care(self):
        plants = self.load_data(self.PLANT_DB)
        if not plants:
            print("⚠️ No plants available!")
            return

        print("\n🌱 Check Plant Care Schedule:\n")
        current_time = int(time.time())  # current timestamp in seconds

        for plant in plants:
            print(f"🌿 Name: {plant['name']}")
            
            # Calculate minutes left for each task
            minutes_since_watered = (current_time - plant["last_watered"]) // 60
            minutes_since_fertilized = (current_time - plant["last_fertilized"]) // 60
            minutes_since_harvested = (current_time - plant["last_harvested"]) // 60

            water_left = plant["water_schedule"] - minutes_since_watered
            fertilize_left = plant["fertilize_schedule"] - minutes_since_fertilized
            harvest_left = plant["harvest_schedule"] - minutes_since_harvested


            print(f"💧 Water in: {max(water_left, 0)} minute(s)")
            print(f"🌾 Fertilize in: {max(fertilize_left, 0)} minute(s)")
            print(f"🧺 Harvest in: {max(harvest_left, 0)} minute(s)")

            print("\n")

            reminders = []
            if water_left <= 0:
                reminders.append("💧 Time to WATER this plant!")
            if fertilize_left <= 0:
                reminders.append("🌾 Time to FERTILIZE this plant!")
            if harvest_left <= 0:
                reminders.append("🧺 Time to HARVEST this plant!")
            
            print("\n")

            for reminder in reminders:
                print(f"🔔 {reminder}")

            # Confirmation input
            if reminders:
                choice = input(f"✅ Have you completed the care for '{plant['name']}'? (y/n): ").strip().lower()
                if choice == "y":
                    # Reset times based on confirmation
                    if water_left <= 0:
                        plant["last_watered"] = current_time
                    if fertilize_left <= 0:
                        plant["last_fertilized"] = current_time
                    if harvest_left <= 0:
                        plant["last_harvested"] = current_time

        # Save updated plant data with new timestamps
        self.save_data(self.PLANT_DB, plants)
        print("\n✅ All reminders handled and plant care logs updated!")

    def show_plants(self):
        dashboard = PlantsDashboard("plantList.json")
        dashboard.display_menu()

        try:
            user_choice = int(input("\nEnter plant ID to view details (or 0 to exit): "))
            if user_choice != 0:
                dashboard.get_plant_details(user_choice)
        except ValueError:
            print("\n⚠ Invalid input! Please enter a number.\n")

    def menu(self):
        while True:
            print("\n🌿 Plant Care Management System 🌿")
            print("1. Add Plant")
            print("2. Remove Plant")
            print("3. View Added Plants")
            print("4. Check Plant Care Schedule")
            print("5. View Plants")
            print("6. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                os.system('cls')
                add_plant()
            elif choice == "2":
                os.system('cls')
                self.remove_plant()
            elif choice == "3":
                os.system('cls')
                self.show_added_plants()
            elif choice == "4":
                os.system('cls')
                self.check_plant_care()
            elif choice == "5":
                os.system('cls')
                self.show_plants()
            elif choice == "6":
                print("Logging out... 👋")
                return
            else:
                print("⚠️ Invalid choice! Please try again.")

    def first_panel(self):
        while True:
            print("\n🌱 Welcome to Plant Care System 🌱")
            print("1. Register")
            print("2. Login")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.register_user()
            elif choice == "2":
                if self.login():
                    os.system('cls')
                    self.menu()
            elif choice == "3":
                print("Goodbye! 👋")
                exit()
            else:
                print("⚠️ Invalid choice! Please try again.")

if __name__ == "__main__":
    app = PlantCareSystem()
    app.first_panel()