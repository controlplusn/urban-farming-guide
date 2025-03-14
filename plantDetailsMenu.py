class PlantDetails:
    def __init__(self, plant):
        self.plant = plant  
        
    def display_menu(self):
        while True:
            print(f"\n🌿 {self.plant.plant_name} - Details Menu 🌿")
            print("1. View General Info")
            print("2. View Herbal Uses")
            print("3. View Growth Requirements")
            print("4. Back to Dashboard")

            choice = input("\nEnter your choice: ")

            if choice == "1":
                self.plant.display_info()
            elif choice == "2":
                print(f"\n🌿 Herbal Uses: {self.plant.herbal_uses}\n")
            elif choice == "3":
                print(f"\n🌱 Growth Requirements:")
                print(f"   - Growth Time: {self.plant.growth_time}")
                print(f"   - Water Requirement: {self.plant.water_requirement}")
                print(f"   - Soil Type: {self.plant.soil_type}\n")
            elif choice == "4":
                print("\nReturning to dashboard...\n")
                break
            else:
                print("\n⚠ Invalid choice! Please enter a valid option.\n")
