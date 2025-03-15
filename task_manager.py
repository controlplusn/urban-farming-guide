import json
import os
from datetime import datetime

class TaskManager:
    def __init__(self, maintenance_db):
        self.maintenance_db = maintenance_db
    
    def load_data(self):
        if not os.path.exists(self.maintenance_db):
            return []
        with open(self.maintenance_db, "r") as file:
            return json.load(file)
    
    def save_data(self, data):
        with open(self.maintenance_db, "w") as file:
            json.dump(data, file, indent=4)
    
    def show_upcoming_tasks(self):
        maintenance_log = self.load_data()
        upcoming_tasks = [task for task in maintenance_log if datetime.strptime(task['date'], "%Y-%m-%d") >= datetime.now()]
        
        print("\n📅 Upcoming Plant Care Tasks 📅")
        if not upcoming_tasks:
            print("✅ No upcoming tasks!")
            return
        
    def filter_tasks_by_date_range(self, start_date, end_date):
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            print("⚠️ Invalid date format! Use YYYY-MM-DD.")
            return

        maintenance_log = self.load_data()
        filtered_tasks = [
            task for task in maintenance_log 
            if start <= datetime.strptime(task['date'], "%Y-%m-%d") <= end
        ]

        print("\n📅 Filtered Plant Care Tasks 📅")
        if not filtered_tasks:
            print("✅ No tasks found in the selected date range!")
            return

        print("+----------------+-------------------+------------+--------------------------------+-------------+")
        print("| Plant Name     | Maintenance Type  | Date       | Notes                          | Status      |")
        print("+----------------+-------------------+------------+--------------------------------+-------------+")
        for task in filtered_tasks:
            status = task.get('status', 'Pending')
            print(f"| {task['plant_name']:<14} | {task['maintenance_type']:<17} | {task['date']} | {task['notes']:<30} | {status:<11} |")
        print("+----------------+-------------------+------------+--------------------------------+-------------+")

    def mark_task_as_completed(self, plant_name, maintenance_type):
        maintenance_log = self.load_data()
        for task in maintenance_log:
            if task['plant_name'] == plant_name and task['maintenance_type'] == maintenance_type:
                task['status'] = "Completed"
                self.save_data(maintenance_log)
                print(f"✅ Task '{maintenance_type}' for {plant_name} marked as completed!")
                return
        print("⚠️ Task not found!")

        