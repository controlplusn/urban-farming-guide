# plant_functions.py
import json
import os

PLANT_DB = "plants.json"

def load_data(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def generate_plant_id():
    plants = load_data(PLANT_DB)
    return max((plant["plant_id"] for plant in plants), default=0) + 1

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
