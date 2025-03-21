import json

class PlantMedicineUse:
    def __init__(self, plant, json_file="herbal_and_medicine_use.json"):
        self.plant = plant
        self.data = self.load_json_data(json_file)

        plant_name = self.plant.plant_name
        self.plant_data = next((item for item in self.data if item["plant"] == plant_name), None)
    
    def load_json_data(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"⚠ Error: The file {file_path} was not found.")
            return []
        except json.JSONDecodeError:
            print(f"⚠ Error: Could not decode JSON in {file_path}.")
            return []
        
    def display_plant_medicinal_uses(self):
        if self.plant_data:
            print(f"\n🌿 Medicinal Uses of {self.plant.plant_name} 🌿\n")
            for index, use in enumerate(self.plant_data["medicinal_uses"], start=1):
                print(f"{index}. {use}")
        else:
            print(f"\n⚠ No medicinal use data found for {self.plant.plant_name}.\n")

        input("\nPress Enter to return to the menu...")