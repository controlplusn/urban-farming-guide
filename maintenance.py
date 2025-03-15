from datetime import datetime
from task_manager import TaskManager
from notifications import NotificationManager
from weather_manager import WeatherManager

class Maintenance:
    def __init__(self, maintenance_db):
        self.maintenance_db = maintenance_db
        self.task_manager = TaskManager(maintenance_db)
        self.notification_manager = NotificationManager(maintenance_db)

    def load_data(self):
        return self.task_manager.load_data()

    def save_data(self, data):
        self.task_manager.save_data(data)

    def add_maintenance_task(self):
        plant_name = input("Enter plant name: ").strip()
        maintenance_type = input("Enter maintenance type (e.g., Watering, Pruning): ").strip()
        due_date = input("Enter due date (YYYY-MM-DD): ").strip()
        notes = input("Enter additional notes (optional): ").strip()

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("⚠️ Invalid date format! Use YYYY-MM-DD.")
            return

        new_task = {
            "plant_name": plant_name,
            "maintenance_type": maintenance_type,
            "date": due_date,
            "notes": notes,
            "status": "Pending"
        }

        tasks = self.load_data()
        tasks.append(new_task)
        self.save_data(tasks)
        print(f"✅ Task added for {plant_name} on {due_date}!")

    def show_tasks(self):
        self.task_manager.show_upcoming_tasks()

    def filter_tasks(self):
        print("\nFilter by:")
        print("1. Specific Date")
        print("2. Date Range")
        print("3. Plant Name")
        print("4. Maintenance Type")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            date_filter = input("Enter date (YYYY-MM-DD): ").strip()
            self.task_manager.filter_tasks_by_date_range(date_filter, date_filter)

        elif choice == "2":
            start_date = input("Enter start date (YYYY-MM-DD): ").strip()
            end_date = input("Enter end date (YYYY-MM-DD): ").strip()
            self.task_manager.filter_tasks_by_date_range(start_date, end_date)

        elif choice == "3":
            plant_filter = input("Enter plant name: ").strip()
            tasks = self.load_data()
            filtered_tasks = [task for task in tasks if task["plant_name"].lower() == plant_filter.lower()]
            if filtered_tasks:
                for task in filtered_tasks:
                    print(f"- {task['plant_name']} ({task['maintenance_type']}) on {task['date']}")
            else:
                print("⚠️ No matching tasks found.")

        elif choice == "4":
            type_filter = input("Enter maintenance type (e.g., Watering, Pruning): ").strip()
            tasks = self.load_data()
            filtered_tasks = [task for task in tasks if task["maintenance_type"].lower() == type_filter.lower()]
            if filtered_tasks:
                for task in filtered_tasks:
                    print(f"- {task['plant_name']} ({task['maintenance_type']}) on {task['date']}")
            else:
                print("⚠️ No matching tasks found.")
        else:
            print("⚠️ Invalid choice!")

    def mark_task_completed(self):
        plant_name = input("Enter plant name: ").strip()
        maintenance_type = input("Enter maintenance type: ").strip()
        self.task_manager.mark_task_as_completed(plant_name, maintenance_type)

if __name__ == "__main__":
    weather_manager = WeatherManager(latitude=13.7565, longitude=121.0583)
    reminder = Maintenance("maintenance.json")

    # Get weather notification
    weather_notification = weather_manager.get_weather_notification()
    print(weather_notification)
    # Pass it to check_due_tasks()
    reminder.notification_manager.check_due_tasks()

    while True:
        print("\n🌿 Maintenance Reminder 🌿")
        print("1. Add Maintenance Task")
        print("2. View All Tasks")
        print("3. Filter Tasks")
        print("4. Mark Task as Completed")
        print("5. Exit")

        option = input("Enter your choice: ").strip()
        if option == "1":
            reminder.add_maintenance_task()
        elif option == "2":
            reminder.show_tasks()
        elif option == "3":
            reminder.filter_tasks()
        elif option == "4":
            reminder.mark_task_completed()
        elif option == "5":
            print("👋 Exiting...")
            break
        else:
            print("⚠️ Invalid choice! Try again.")
