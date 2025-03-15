import os
from plant_general_info import PlantGeneralInfo
from urban_farming import UrbanFarmingTechniques
from plantCare import PlantCare

class PlantDetails:
    def __init__(self, plant):
        self.plant = plant  
        
    def display_menu(self):
        while True:
            os.system('cls')
            print(f"\n🌿 {self.plant.plant_name} - Details Menu 🌿")
            print("1. Plant General Info")
            print("2. Urban Farming Techniques")
            print("3. Plant Care")
            print("4. Best Practices")
            print("5. Herbal and Medicine Use")
            print("6. Add a Plant") # Add plant function -> on main branch

            choice = input("\nEnter your choice: ")

            if choice == "1":
                os.system('cls')
                general_info = PlantGeneralInfo(self.plant)
                general_info.display_plant_info()
                input("\nPress Enter to return to the menu...") 
            elif choice == "2":
                os.system('cls')
                urban_farming_techniques = UrbanFarmingTechniques(self.plant)
                urban_farming_techniques.display_urban_farming_tips()
            elif choice == "3":
                os.system('cls')
                plant_care = PlantCare(self.plant)
                plant_care.display_plant_care()
            elif choice == "4":
                print("\nReturning to dashboard...\n")
                break
            else:
                print("\n⚠ Invalid choice! Please enter a valid option.\n")
