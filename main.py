import hashlib
import os
import random
import msvcrt

class User:
    def __init__(self, username, email, password):
        self._user_id = self._generate_user_id()  
        self.username = username  
        self._email = email  
        self._salt = os.urandom(16).hex()  
        self.__password = self._hash_password(password)

    def _generate_user_id(self):
        return random.randint(10000, 99999)

    def _hash_password(self, password):
        return hashlib.sha256((password + self._salt).encode()).hexdigest()

    def verify_password(self, password):
        return self._hash_password(password) == self.__password

    def login(self, password):
        return self.verify_password(password)  

    def logout(self):
        print("\nLogged out successfully.")  

class Dashboard:
    def __init__(self, user):
        self.user = user

    def show(self):
        print("\n[Dashboard]")

# For masked password input
def input_password(prompt="Enter Password: "):
    print(prompt, end="", flush=True)
    password = ""

    while True:
        char = msvcrt.getch()
        if char in {b"\r", b"\n"}:
            break
        elif char == b"\b":
            if password:
                password = password[:-1]
                print("\b \b", end="", flush=True)
        else:
            password += char.decode("utf-8")
            print("*", end="", flush=True)

    print()
    return password

def register():
    print("\nRegister:")
    username = input("Enter Username: ")
    email = input("Enter Email: ")
    password = input_password()

    user = User(username, email, password)
    print(f"\nWelcome, {username}! Your account has been created successfully.")
    return user

def login(user):
    if not user:
        print("\nNo registered user. Please register first.")
        return False

    while True:
        print("\nLogin:")
        email_input = input("Enter Email: ")
        password_input = input_password()

        if user._email == email_input and user.login(password_input): 
            print(f"\n=== Welcome Back, {user.username}! You have logged in successfully. ===")
            return True
        else:
            print("\nInvalid credentials. Try again.")

def main():
    user = None
    while True:
        print("\n=== Welcome to Urban Farming Guide ===")
        print("1. Register")
        print("2. Log in")
        print("3. Log out")

        choice = input("\nChoose an option: ")

        if choice == "1":
            user = register()
        elif choice == "2":
            if user and login(user):
                dashboard = Dashboard(user)
                dashboard.show()
        elif choice == "3":
            if user:
                user.logout()
                user = None
            else:
                print("\nYou are not logged in.")
        else:
            print("\nInvalid choice. Try again.")

if __name__ == "__main__":
    main()
