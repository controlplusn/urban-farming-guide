import json
import os
import msvcrt  # For password masking (Windows only)

# File paths for each database
USER_DB = "users.json"
PLANT_DB = "plants.json"
REMINDER_DB = "reminders.json"
MAINTENANCE_DB = "maintenance.json"

# Function to load JSON data
# Load data from a specific database file
def load_data(db_file):
    if not os.path.exists(db_file):
        return []
    with open(db_file, "r") as file:
        users = json.load(file)
        return reassign_user_ids(users)  # Adjust IDs after loading

# Save data to a specific database file
def save_data(db_file, data):
    with open(db_file, "w") as file:
        json.dump(data, file, indent=4)

# Reassign user IDs to remove gaps
def reassign_user_ids(users):
    for index, user in enumerate(users):
        user["user_id"] = index + 1  # Reassign sequential IDs (1, 2, 3, ...)
    return users

# Secure password input with masking
def get_password(prompt):
    print(prompt, end="", flush=True)
    password = ""
    while True:
        char = msvcrt.getch()
        if char == b"\r" or char == b"\n":  # Enter key
            print("")
            return password.strip()  # Remove accidental spaces
        elif char == b"\b":  # Backspace
            if password:
                password = password[:-1]
                print("\b \b", end="", flush=True)
        else:
            password += char.decode("utf-8")
            print("*", end="", flush=True)

# Register a new user with ID adjustment
def register_user():
    users = load_data(USER_DB)  # Load and reassign IDs
    user_id = len(users) + 1  # Always assign the next available ID
    print(f"\n🔹 Generated User ID: {user_id}")  
    
    name = input("Enter name: ").strip()
    email = input("Enter email: ").strip().lower()  # Convert email to lowercase
    
    if not name or not email:
        print("⚠️ Name and email cannot be empty!")
        return
    
    if any(user["email"] == email for user in users):
        print("⚠️ Email already registered!")
        return
    
    if any(user["name"].lower() == name.lower() for user in users):
        print("⚠️ Username already taken!")
        return
    
    password = ""
    while not password:
        password = get_password("Enter password: ")
        if not password:
            print("⚠️ Password cannot be empty! Try again.")

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

# Menu function
def menu():
    while True:
        print("\n🌿 Plant Care Management System 🌿")
        print("1. Add Plant")
        print("2. Remove Plant")
        print("3. View Users")
        print("4. View Plants")
        print("5. Logout")

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
    