import json

class UrbanFarmingTechniques:
    def __init__(self, plant, json_file="urban_farming_techniques.json"):
        self.plant = plant
        self.data = self.load_json_data(json_file)

        plant_name = self.plant.plant_name
        self.plant_data = self.data.get(plant_name, {})

    def load_json_data(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"⚠ Error: The file {file_path} was not found.")
            return {}
        except json.JSONDecodeError:
            print(f"⚠ Error: Could not decode JSON in {file_path}.")
            return {}

    def get_value(self, category, key, default="N/A"):
        category_data = self.plant_data.get(category, {})
        if key is None:
            return category_data  # Return the whole dictionary if no key is provided
        return category_data.get(key, default)
    

    def display_urban_farming_tips(self):
        print(f"\n╔══════════════════════════════════════╗")
        print(f"║ 🌿 Urban Farming Techniques - {self.plant.plant_name}  ║")
        print(f"╠══════════════════════════════════════╣")
        print(f"║ 📌 Best Growing Setup                 ║")
        print(f"║ - Container: {self.get_value('best_growing_setup', 'container_type')} ║")
        print(f"║ - Ideal Size: {self.get_value('best_growing_setup', 'ideal_size')} ║")
        print(f"║ - Indoor/Outdoor: {self.get_value('best_growing_setup', 'indoor_vs_outdoor_suitability')} ║")
        print(f"╠══════════════════════════════════════╣")
        print(f"║ ☀️ Light Requirements                  ║")
        print(f"║ - Needs {self.get_value('light_requirements', 'sunlight_hours')} of sunlight ║")
        print(f"║ - Artificial Light: {self.get_value('light_requirements', 'artificial_light')} ║")
        print(f"╠══════════════════════════════════════╣")
        print(f"║ 💧 Watering Strategy                   ║")
        print(f"║ - Frequency: {self.get_value('watering_strategy', 'frequency')} ║")
        print(f"║ - Precaution: {self.get_value('watering_strategy', 'precaution')} ║")
        print(f"╠══════════════════════════════════════╣")
        print(f"║ 🌱 Soil & Fertilizer Needs             ║")
        print(f"║ - Soil Type: {self.get_value('soil_and_fertilizer_needs', 'soil_type')} ║")
        print(f"║ - Fertilizer: {self.get_value('soil_and_fertilizer_needs', 'fertilizer')} ║")
        print(f"╠══════════════════════════════════════╣")
        print(f"║ 🌍 Space-Saving Tips                   ║")
        print(f"║ - Vertical Growing: {self.get_value('space_saving_tips', 'vertical_growing')} ║")
        print(f"║ - Companion Planting: {self.get_value('space_saving_tips', 'companion_planting')} ║")
        print(f"╠══════════════════════════════════════╣")
        print(f"║ 🐜 Pest & Disease Prevention           ║")
        print(f"║ - Common Pests: {', '.join(self.get_value('pest_and_disease_prevention', 'common_pests', []))} ║")
        print(f"║ - Prevention: {', '.join(self.get_value('pest_and_disease_prevention', 'prevention_methods', []))} ║")
        print(f"╠══════════════════════════════════════╣")
        print(f"║ ✅ Urban Farming Challenges & Solutions║")
        challenges = self.plant_data.get('urban_farming_challenges_and_solutions', {})
        for challenge, solution in challenges.items():

            print(f"║ - {challenge.capitalize()}: {solution} ║")
        print(f"╚══════════════════════════════════════╝")  

        input("\nPress enter to return to the dashboard...")