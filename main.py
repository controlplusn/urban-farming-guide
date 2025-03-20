import json
import os
import msvcrt  # For password masking (Windows only)

# File paths for each database
USER_DB = "users.json"
PLANT_DB = "plants.json"
REMINDER_DB = "reminders.json"
MAINTENANCE_DB = "maintenance.json"

# Function to load JSON data
def load_data(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# Function to save JSON data
def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# Password masking function
def get_password(prompt="Enter password: "):
    print(prompt, end="", flush=True)
    password = []
    while True:
        char = msvcrt.getch()
        if char == b"\r":  # Enter key
            print("")
            break
        elif char == b"\b":  # Backspace
            if password:
                password.pop()
                print("\b \b", end="", flush=True)
        else:
            password.append(char.decode("utf-8"))
            print("*", end="", flush=True)
    return "".join(password)

# Generate unique user ID
def generate_user_id():
    users = load_data(USER_DB)
    return max((user["user_id"] for user in users), default=0) + 1

# Register a new user
def register_user():
    users = load_data(USER_DB)
    user_id = generate_user_id()
    print(f"Generated User ID: {user_id}")  
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
    
    password = get_password("Enter password: ")
    if not password:
        print("⚠️ Password cannot be empty!")
        return
    
    users.append({"user_id": user_id, "name": name, "email": email, "password": password})
    save_data(USER_DB, users)
    print("✅ User registered successfully!")

# User login function
def login():
    users = load_data(USER_DB)
    email = input("Enter email: ").strip()
    password = get_password("Enter password: ")

    for user in users:
        if user["email"] == email and user["password"] == password:
            print(f"✅ Welcome back, {user['name']}!")
            return user  
    print("❌ Invalid email or password!")
    return None

# Generate unique plant ID
def generate_plant_id():
    plants = load_data(PLANT_DB)
    return max((plant["plant_id"] for plant in plants), default=0) + 1

# Add a plant
def add_plant():
    plants = load_data(PLANT_DB)
    plant_id = generate_plant_id()
    plant_name = input("Enter plant name: ").strip()
    water_schedule = input("Enter watering schedule: ").strip()

    if not plant_name or not water_schedule:
        print("⚠️ Plant name and watering schedule cannot be empty!")
        return

    plants.append({"plant_id": plant_id, "name": plant_name, "water_schedule": water_schedule})
    save_data(PLANT_DB, plants)
    print("✅ Plant added successfully!")

# Remove a plant
def remove_plant():
    plants = load_data(PLANT_DB)
    if not plants:
        print("⚠️ No plants available!")
        return

    print("📜 Plant List:")
    for plant in plants:
        print(f"{plant['plant_id']}. {plant['name']}")

    try:
        plant_id = int(input("Enter plant ID to remove: "))
        plants = [plant for plant in plants if plant["plant_id"] != plant_id]
        save_data(PLANT_DB, plants)
        print("✅ Plant removed successfully!")
    except ValueError:
        print("⚠️ Invalid input! Please enter a valid plant ID.")

# View users
def show_users():
    users = load_data(USER_DB)
    print("\n👥 Registered Users:")
    for user in users:
        print(f"ID: {user['user_id']} | Name: {user['name']} | Email: {user['email']}")

# View plants
def show_plants():
    plants = load_data(PLANT_DB)
    print("\n🌱 Plants List:")
    for plant in plants:
        print(f"ID: {plant['plant_id']} | Name: {plant['name']} | Water Schedule: {plant['water_schedule']}")

# Check plant maintenance
def check_plants():
    plants = load_data(PLANT_DB)
    print("\n🌱 Plants List:\n")
    for plant in plants:
        print(f"Name: {plant['name']}")
        print(f"💧 Water Time: left | 🌱 Fertilizer Time: left | 🧺 Harvest Time: left")
        print("\n")

# Menu function
def menu():
    while True:
        print("\n🌿 Plant Care Management System 🌿")
        print("1. Add Plant")
        print("2. Remove Plant")
        print("3. View Users")
        print("4. View Plants")
        print("5. Maintenance Reminder")
        print("0. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_plant()
        elif choice == "2":
            remove_plant()
        elif choice == "3":
            show_users()
        elif choice == "4":
            show_plants()
        elif choice == "5":
            check_plants()
        elif choice == "0":
            print("Logging out... 👋")
            return
        else:
            print("⚠️ Invalid choice! Please try again.")

# First panel for login or registration
def first_panel():
    while True:
        print("\n🌱 Welcome to Plant Care System 🌱")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            user = login()
            if user:
                menu()
        elif choice == "3":
            print("Goodbye! 👋")
            exit()
        else:
            print("⚠️ Invalid choice! Please try again.")

# Run the system
if __name__ == "__main__":
    first_panel()
    