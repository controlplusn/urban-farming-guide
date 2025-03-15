import json
import os
from datetime import datetime

class NotificationManager:
    def __init__(self, maintenance_db):
        self.maintenance_db = maintenance_db

    def load_data(self):
        if not os.path.exists(self.maintenance_db):
            return []
        with open(self.maintenance_db, "r") as file:
            return json.load(file)

    def check_due_tasks(self, weather_notification=None):
        maintenance_log = self.load_data()
        today = datetime.now().strftime("%Y-%m-%d")
        overdue_tasks = []
        due_today_tasks = []
        
        for task in maintenance_log:
            if task['date'] == today and task.get('status', 'Pending') == 'Pending':
                due_today_tasks.append(task)
            elif task['date'] < today and task.get('status', 'Pending') == 'Pending':
                overdue_tasks.append(task)

        if weather_notification:
            print(f"\n🌤️ Weather Notification: {weather_notification}")

        if due_today_tasks:
            print("\n⚠️ Tasks Due Today:")
            for task in due_today_tasks:
                print(f"- {task['plant_name']} ({task['maintenance_type']})")
        
        if overdue_tasks:
            print("\n❌ Overdue Tasks:")
            for task in overdue_tasks:
                print(f"- {task['plant_name']} ({task['maintenance_type']}) was due on {task['date']}")

        if not due_today_tasks and not overdue_tasks:
            print("✅ No pending tasks due today or overdue!")
