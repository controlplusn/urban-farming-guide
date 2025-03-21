class PlantGeneralInfo:
    def __init__(self, plant):
        self.plant = plant
    
    def display_plant_info(self):
        print("=" * 80)
        print(f"🌱  PLANT GENERAL INFO: {self.plant.plant_name}  🌱")
        print("=" * 80)
        print(f"📌 Category       : {self.plant.plant_category}")
        print(f"📌 Growth Time    : {self.plant.growth_time}")
        print(f"📌 Water Needs    : {self.plant.water_requirement}")
        print(f"📌 Soil Type      : {self.plant.soil_type}")
        print(f"📌 Sunlight       : {getattr(self.plant, 'sunlight', 'N/A')}")  # Handle missing keys
        print(f"📌 Uses          : {self.plant.herbal_uses}")
        print(f"\n📖 FUN FACT: {getattr(self.plant, 'fun_fact', 'No fun fact available.')}")
        print("=" * 80)