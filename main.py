import json
import os
import msvcrt  # For password masking (Windows only)

# File paths for each database
USER_DB = "users.json"
PLANT_DB = "plantList.json"
MAINTENANCE_DB = "maintenance.json"
FARM_DB = "personal_farm.json"  # New: Stores user's personal farm plants

# Load data from a database file
def load_data(db_file):
    if not os.path.exists(db_file):
        return []
    with open(db_file, "r") as file:
        return json.load(file)

# Save data to a database file
def save_data(db_file, data):
    with open(db_file, "w") as file:
        json.dump(data, file, indent=4)

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

# User Registration
def register_user():
    users = load_data(USER_DB)
    user_id = len(users) + 1
    print(f"\n🔹 Generated User ID: {user_id}")

    name = input("Enter name: ").strip()
    email = input("Enter email: ").strip().lower()

    if not name or not email or any(user["email"] == email for user in users):
        print("⚠️ Invalid or duplicate email!")
        return

    password = get_password("Enter password: ")
    users.append({"user_id": user_id, "name": name, "email": email, "password": password})
    save_data(USER_DB, users)
    print("✅ User registered successfully!")

# User Login
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

# Display Main Dashboard
def dashboard():
    while True:
        print("\n📋 **Dashboard**")
        print("1. 📖 Plants and Crops Database")
        print("2. 🌿 Personalized Farming Guide")
        print("3. 🍽️ Recipe Guide")
        print("4. 🛠️ Maintenance Reminder")
        print("5. 🚜 My Personal Farm")
        print("6. 🚪 Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            plants_and_crops_database()
        elif choice == "2":
            print("🔧 Personalized Farming Guide (Coming Soon!)")
        elif choice == "3":
            print("🍽️ Recipe Guide (Coming Soon!)")
        elif choice == "4":
            show_maintenance_log()
        elif choice == "5":
            view_personal_farm()
        elif choice == "6":
            print("👋 Logging out...")
            return
        else:
            print("⚠️ Invalid choice! Try again.")

# Search and Select Plant from Database
def plants_and_crops_database():
    plants = load_data(PLANT_DB)
    if not plants:
        print("⚠️ No plants found in the database.")
        return

    search_query = input("🔎 Search for a plant (or press Enter to view all): ").strip().lower()
    filtered_plants = [p for p in plants if search_query in p["plant_name"].lower()] if search_query else plants

    if not filtered_plants:
        print("❌ No matching plants found!")
        return

    print("\n🌱 Available Plants:")
    for plant in filtered_plants:
        print(f"{plant['plantID']}. {plant['plant_name']}")

    try:
        plant_id = int(input("Enter plant ID to view details: "))
        selected_plant = next((p for p in plants if p["plantID"] == plant_id), None)

        if selected_plant:
            plant_details(selected_plant)
        else:
            print("⚠️ Invalid Plant ID!")

    except ValueError:
        print("⚠️ Invalid input! Please enter a valid plant ID.")

# Display Plant Details and Options
def plant_details(plant):
    while True:
        print(f"\n🌿 {plant['plant_name']} Details:")
        print("1. Overview")
        print("2. Urban Farming Technique")
        print("3. Plant Care")
        print("4. Best Practices")
        print("5. Herbal & Medicinal Uses")
        print("6. ➕ Add to Personal Farm")
        print("7. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            print(f"🌱 Growth Time: {plant.get('growth_time', 'No data')}")
        elif choice == "2":
            print(f"🏡 Urban Farming Techniques: {plant.get('urban_farming', 'No data')}")
        elif choice == "3":
            print(f"🪴 Plant Care: {plant.get('water_requirement', 'No data')}")
        elif choice == "4":
            print(f"✅ Best Practices: {plant.get('best_practices', 'No data')}")
        elif choice == "5":
            print(f"💊 Herbal & Medicinal Uses: {plant.get('herbal_uses', 'No data')}")
        elif choice == "6":
            add_to_personal_farm(plant)
        elif choice == "7":
            break
        else:
            print("⚠️ Invalid choice! Try again.")

# Add Plant to Personal Farm
def add_to_personal_farm(plant):
    farm = load_data(FARM_DB)
    farm.append(plant)
    save_data(FARM_DB, farm)
    print(f"✅ {plant['plant_name']} added to your personal farm!")

# View Personal Farm
def view_personal_farm():
    farm = load_data(FARM_DB)
    print("\n🚜 **My Personal Farm:**")
    
    if not farm:
        print("⚠️ Your farm is empty.")
        return

    for plant in farm:
        print(f"🌿 {plant['plant_name']} | Water Requirement: {plant.get('water_requirement', 'No data')}")

# Show Maintenance Log
def show_maintenance_log():
    logs = load_data(MAINTENANCE_DB)
    print("\n📋 **Plant Maintenance Logs:**")

    if not logs:
        print("⚠️ No maintenance records found.")
        return

    for log in logs:
        print(f"🌿 {log['plant_name']} | {log['maintenance_type']} | Date: {log['date']} | Notes: {log['notes']}")

# First Panel for Login or Registration
def first_panel():
    while True:
        print("\n🌱 **Welcome to Smart Farming System** 🌱")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            user = login()
            if user:
                dashboard()
        elif choice == "3":
            print("👋 Goodbye!")
            exit()
        else:
            print("⚠️ Invalid choice! Try again.")

# Run the system
if __name__ == "__main__":
    first_panel()
