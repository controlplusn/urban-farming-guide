import json
import os
import msvcrt

class Authentication:
    USER_DB = "users.json"

    def __init__(self):
        self.current_user = None

    def load_data(self, file):
        if not os.path.exists(file):
            return []
        with open(file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def save_data(self, file, data):
        with open(file, "w") as f:
            json.dump(data, f, indent=4)

    def get_password(self, prompt="Enter password: "):
        print(prompt, end="", flush=True)
        password = []
        while True:
            char = msvcrt.getch()
            if char == b"\r":
                print("")
                break
            elif char == b"\b":
                if password:
                    password.pop()
                    print("\b \b", end="", flush=True)
            else:
                password.append(char.decode("utf-8"))
                print("*", end="", flush=True)
        return "".join(password)

    def generate_user_id(self):
        users = self.load_data(self.USER_DB)
        return max((user["user_id"] for user in users), default=0) + 1

    def register_user(self):
        users = self.load_data(self.USER_DB)
        user_id = self.generate_user_id()
        name = input("Enter name: ").strip()
        email = input("Enter email: ").strip()
        
        if not name or not email:
            print("⚠️ Name and email cannot be empty!")
            return
        
        if any(user["email"] == email for user in users):
            print("⚠️ Email already registered!")
            return
        
        if any(user["name"].lower() == name.lower() for user in users):
            print("⚠️ Username already taken!")
            return
        
        _password = self.get_password("Enter password: ")
        if not _password:
            print("⚠️ Password cannot be empty!")
            return
        
        users.append({"user_id": user_id, "name": name, "email": email, "password": _password})
        self.save_data(self.USER_DB, users)
        print("✅ User registered successfully!")

    def login(self):
        users = self.load_data(self.USER_DB)
        email = input("Enter email: ").strip()
        _password = self.get_password("Enter password: ")

        for user in users:
            if user["email"] == email and user["password"] == _password:
                print(f"✅ Welcome back, {user['name']}!")
                self.current_user = user
                return True
        print("❌ Invalid email or password!")
        return False
