import json
import os

class PlantCare:
    def __init__(self, plant):
        self.plant = plant
        self.plant_care_data = self.load_plant_care_data()

    def load_plant_care_data(self, filename="plant_care.json"):
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        return {item["plant_name"]: item for item in data}

    def display_plant_care(self):
        care_data = self.plant_care_data.get(self.plant.plant_name)

        if not care_data:
            print("\n⚠ No plant care details available for this plant.\n")
            return

        os.system('cls')
        print("\n🌿 " + "="*30 + f" 🌿\n     Plant Care Guide: {self.plant.plant_name}\n🌿 " + "="*30 + " 🌿")
        print(f"📌 Light Requirement: {care_data['light_requirement']}")
        print(f"💧 Watering: {care_data['watering']}")
        print(f"🌱 Soil Type: {care_data['soil_type']}")
        print(f"🌿 Fertilizer: {care_data['fertilizer']}")
        print(f"🪴 Suitable for Containers? {care_data['container_suitability']}")
        print(f"🐛 Common Pests: {care_data['common_pests']}")
        print(f"✅ Extra Care Tips: {care_data['extra_care']}")
        print("="*50 + "\n")

        input("\nPress Enter to return to the menu...")
