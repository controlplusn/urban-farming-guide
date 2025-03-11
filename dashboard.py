from os import name


class Dashboard:
    def __init__(self):
        self.name = name
    

    def main():
        while True:
            print("\n🌿 Plant Care Management System 🌿")
            print("1. Add Plant")
            print("2. Remove Plant")
            print("3. View Plants")
            print("4. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                # add_plant()
                continue
            elif choice == "2":
                # remove_plant()
                continue
            elif choice == "3":
                # show_plants()
                continue
            elif choice == "4":
                print("Logging out... 👋")
                return
            else:
                print("⚠️ Invalid choice! Please try again.")

if __name__ == "main":
    dashboard = Dashboard()
    dashboard.main()