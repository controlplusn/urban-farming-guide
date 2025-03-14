import json
import os
import msvcrt  # For password masking (Windows only)

# File paths for each database
USER_DB = "users.json"
PLANT_DB = "plantList.json"
MAINTENANCE_DB = "maintenance.json"

# Load data from a specific database file
def load_data(db_file):
    if not os.path.exists(db_file):
        return []
    with open(db_file, "r") as file:
        return json.load(file)

# Save data to a specific database file
def save_data(db_file, data):
    with open(db_file, "w") as file:
        json.dump(data, file, indent=4)

# Reassign user IDs if there's a manual deletion
def reassign_user_ids(users):
    for index, user in enumerate(users):
        user["user_id"] = index + 1  # Sequential numbering
    return users

# Secure password input with masking
def get_password(prompt):
    print(prompt, end="", flush=True)
    password = ""
    while True:
        char = msvcrt.getch()
        if char in [b"\r", b"\n"]:  # Enter key
            print("")
            return password.strip()
        elif char == b"\b":  # Backspace
            if password:
                password = password[:-1]
                print("\b \b", end="", flush=True)
        else:
            password += char.decode("utf-8")
            print("*", end="", flush=True)

# Register a new user with ID adjustment
def register_user():
    users = load_data(USER_DB)
    users = reassign_user_ids(users)  # Ensure no gaps in IDs
    user_id = len(users) + 1
    print(f"\n🔹 Generated User ID: {user_id}")

    name = input("Enter name: ").strip()
    email = input("Enter email: ").strip().lower()

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
    email = input("Enter email: ").strip().lower()
    password = get_password("Enter password: ")

    for user in users:
        if user["email"] == email and user["password"] == password:
            print(f"✅ Welcome back, {user['name']}!")
            return user
    print("❌ Invalid email or password!")
    return None

# Reassign plant IDs to prevent gaps
def reassign_plant_ids(plants):
    for index, plant in enumerate(plants):
        plant["plantID"] = index + 1  # ✅ Fix key from "plant_id" to "plantID"
    return plants

def log_maintenance():
    plants = load_data(PLANT_DB)
    if not plants:
        print("⚠️ No plants available for maintenance!")
        return

    print("\n🌱 Select a plant for maintenance:")
    for plant in plants:
        print(f"{plant['plantID']}. {plant['plant_name']}")

    try:
        plant_id = int(input("Enter plant ID: "))
        selected_plant = next((plant for plant in plants if plant["plantID"] == plant_id), None)

        if not selected_plant:
            print("⚠️ Invalid plant ID!")
            return

        maintenance_type = input("Enter maintenance type (Watering/Fertilizing): ").strip().capitalize()
        if maintenance_type not in ["Watering", "Fertilizing"]:
            print("⚠️ Invalid maintenance type! Use 'Watering' or 'Fertilizing'.")
            return

        date = input("Enter date (YYYY-MM-DD): ").strip()
        notes = input("Add any notes (optional): ").strip()

        maintenance_logs = load_data(MAINTENANCE_DB)

        maintenance_logs.append({
            "plantID": plant_id,
            "plant_name": selected_plant["plant_name"],
            "maintenance_type": maintenance_type,
            "date": date,
            "notes": notes
        })

        save_data(MAINTENANCE_DB, maintenance_logs)
        print("✅ Maintenance record added successfully!")

    except ValueError:
        print("⚠️ Invalid input! Please enter a valid plant ID.")

# Show maintenance log
def show_maintenance_log():
    logs = load_data(MAINTENANCE_DB)
    print("\n📋 Plant Maintenance Logs:")

    if not logs:
        print("⚠️ No maintenance records found.")
        return

    for log in logs:
        print(f"🌿 {log['plant_name']} | {log['maintenance_type']} | Date: {log['date']} | Notes: {log['notes']}")
# Generate unique plant ID
def generate_plant_id():
    plants = load_data(PLANT_DB)
    plants = reassign_plant_ids(plants)
    return len(plants) + 1

# Add a plant
def add_plant():
    plants = load_data(PLANT_DB)
    plants = reassign_plant_ids(plants)  # Fix IDs if needed
    plant_id = len(plants) + 1

    plant_name = input("Enter plant name: ").strip()
    growth_time = input("Enter growth time: ").strip()
    water_requirement = input("Enter water requirement: ").strip()
    soil_type = input("Enter soil type: ").strip()
    herbal_uses = input("Enter herbal uses: ").strip()
    plant_category = input("Enter plant category: ").strip()

    if not plant_name or not water_requirement:
        print("⚠️ Plant name and water requirement cannot be empty!")
        return

    if any(plant["plant_name"].lower() == plant_name.lower() for plant in plants):
        print("⚠️ This plant already exists in the database!")
        return

    plants.append({
        "plantID": plant_id,
        "plant_name": plant_name,
        "growth_time": growth_time,
        "water_requirement": water_requirement,
        "soil_type": soil_type,
        "herbal_uses": herbal_uses,
        "plant_category": plant_category
    })

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
        print(f"{plant['plantID']}. {plant['plant_name']}")

    try:
        plant_id = int(input("Enter plant ID to remove: "))
        plants = [plant for plant in plants if plant["plantID"] != plant_id]
        plants = reassign_plant_ids(plants)  # Fix IDs after deletion
        save_data(PLANT_DB, plants)
        print("✅ Plant removed successfully!")
    except ValueError:
        print("⚠️ Invalid input! Please enter a valid plant ID.")

# View users
def show_users():
    users = load_data(USER_DB)
    print("\n👥 Registered Users:")
    if not users:
        print("⚠️ No users found.")
        return
    for user in users:
        print(f"ID: {user['user_id']} | Name: {user['name']} | Email: {user['email']}")

# View plants
def show_plants():
    plants = load_data(PLANT_DB)
    print("\n🌱 Plants List:")
    
    if not plants:
        print("⚠️ No plants found.")
        return

    for plant in plants:
        print(f"ID: {plant.get('plantID', 'Unknown ID')} | Name: {plant.get('plant_name', 'Unknown')} | Water Requirement: {plant.get('water_requirement', 'Unknown')}")

# Menu function
def menu():
    while True:
        print("\n🌿 Plant Care Management System 🌿")
        print("1. Add Plant")
        print("2. Remove Plant")
        print("3. View Users")
        print("4. View Plants")
        print("5. Log Plant Maintenance")
        print("6. View Maintenance Log")
        print("7. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_plant()
        elif choice == "2":
            remove_plant()
        elif choice == "3":
            show_users()
        elif choice == "4":
            show_plants()
        elif choice == "5":
            log_maintenance()
        elif choice == "6":
            show_maintenance_log()
        elif choice == "7":
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

        choice = input("Enter your choice: ").strip()

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
