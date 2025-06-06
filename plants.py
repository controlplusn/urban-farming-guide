import os
import json
from plantDetailsMenu import PlantDetails

class Plant:
    def __init__(self, plant_data):
        self.plantID = plant_data["plantID"]
        self.plant_name = plant_data["plant_name"]
        self.growth_time = plant_data["growth_time"]
        self.water_requirement = plant_data["water_requirement"]
        self.soil_type = plant_data["soil_type"]
        self.sunlight = plant_data["sunlight"]
        self.herbal_uses = plant_data["herbal_uses"]
        self.plant_category = plant_data["plant_category"]
        self.fun_fact = plant_data["fun_fact"]

class PlantsDashboard:
    def __init__(self, json_file):
        
        self.plants = self.load_plants(json_file)

    def load_plants(self, json_file):
        with open(json_file, "r") as file:
            data = json.load(file)
        return {plant["plantID"]: Plant(plant) for plant in data}

    def display_menu(self):
        print("☘ Plants and Crops Dashboard ☘")
        print("Select a plant by entering its ID:")
        for plant_id, plant in self.plants.items():
            print(f"{plant_id}. {plant.plant_name}")

    def get_plant_details(self, plant_id):
        plant = self.plants.get(plant_id)
        if plant:
            details = PlantDetails(plant)
            details.display_menu()
        else:
            print("\n⚠ Plant not found! Please enter a valid ID.\n")


if __name__ == "__main__":
    dashboard = PlantsDashboard("plantList.json")

    while True:
        os.system('cls')    
        dashboard.display_menu()
        try:
            user_choice = int(input("\nEnter plant ID (or 0 to exit): "))

            if user_choice == 0:
                print("\nExiting program...\n")
                break
            dashboard.get_plant_details(user_choice)
        except ValueError:
            print("\n⚠ Invalid input! Please enter a number.\n")
