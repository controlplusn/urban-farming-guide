import json
from recipe import Recipe

class RecipeGuide:
    def __init__(self, recipe_db="recipes.json"):
        self.recipe_db = recipe_db
        self.recipes = self.load_data()

    def load_data(self):
        """Load recipes from JSON file."""
        try:
            with open(self.recipe_db, "r") as f:
                return [Recipe(
                    recipe_id=recipe.get("recipeID"),
                    name=recipe.get("recipe_name"),
                    ingredients=recipe.get("ingredients", []),
                    categories=recipe.get("plant_categories", []),
                    instructions=recipe.get("instructions", "")
                ) for recipe in json.load(f)]
        except (json.JSONDecodeError, IOError, FileNotFoundError):
            return []

    def save_data(self):
        """Save recipes to JSON file."""
        try:
            with open(self.recipe_db, "w") as f:
                json.dump([recipe.__dict__ for recipe in self.recipes], f, indent=4)
        except IOError:
            print("⚠️ Error saving data!")

    def generate_recipe_id(self):
        """Generate a unique recipe ID."""
        return max((recipe.recipe_id for recipe in self.recipes), default=0) + 1

    def get_user_input(self, prompt):
        """Helper function to get user input and strip whitespace."""
        return input(prompt).strip()

    def add_recipe(self):
        """Add a new recipe."""
        print("\n🆕 Adding a New Recipe")
        recipe_id = self.generate_recipe_id()
        
        name = self.get_user_input("Enter recipe name: ")
        ingredients = self.get_user_input("List ingredients (comma-separated): ").split(',')
        categories = self.get_user_input("Enter categories (comma-separated): ").split(',')
        instructions = self.get_user_input("Provide step-by-step instructions: ")

        if not all([name, ingredients, categories, instructions]):
            print("⚠️ All fields are required! Try again.")
            return

        new_recipe = Recipe(recipe_id, name, [i.strip() for i in ingredients], [c.strip().lower() for c in categories], instructions)
        self.recipes.append(new_recipe)
        self.save_data()
        print(f"✅ '{name}' has been added to your recipe collection!")

    def view_recipes(self):
        """Display all recipes and allow filtering by category."""
        if not self.recipes:
            print("⚠️ No recipes found!")
            return

        print("\n📜 Recipe Collection:")
        for recipe in self.recipes:
            print(f"🔹 {recipe.recipe_id}: {recipe.name}")
        
        choice = self.get_user_input("\n1. View by ID\n2. Search by Category\n3. Back to Menu\n👉 Choose an option: ")
        
        if choice == "1":
            self.view_recipe_by_id()
        elif choice == "2":
            self.filter_recipes()
        elif choice != "3":
            print("⚠️ Invalid option! Try again.")

    def view_recipe_by_id(self):
        """View a recipe by its ID."""
        recipe_id = self.get_user_input("\n🔍 Enter Recipe ID (or 'q' to cancel): ")
        if recipe_id.lower() == 'q':
            return
        
        try:
            recipe_id = int(recipe_id)
            recipe = next((r for r in self.recipes if r.recipe_id == recipe_id), None)
            recipe.display() if recipe else print("⚠️ Recipe not found.")
        except ValueError:
            print("⚠️ Invalid ID! Enter a number.")

    def filter_recipes(self):
        """Filter recipes by category."""
        categories = sorted({cat for recipe in self.recipes for cat in recipe.categories})
        if not categories:
            print("⚠️ No categories available.")
            return

        print("\n🔍 Available Categories:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")

        choice = self.get_user_input("\n👉 Select a category by number (or 'q' to cancel): ").lower()
        if choice == 'q':
            return

        if not choice.isdigit() or not (1 <= int(choice) <= len(categories)):
            print("⚠️ Invalid choice! Please enter a valid number.")
            return

        selected_category = categories[int(choice) - 1]
        filtered_recipes = [r for r in self.recipes if selected_category in r.categories]

        if filtered_recipes:
            print(f"\n📂 Recipes in '{selected_category}':")
            for recipe in filtered_recipes:
                recipe.display()
        else:
            print(f"⚠️ No recipes found under '{selected_category}'.")

    def recipe_menu(self):
        """Main menu for recipe guide."""
        while True:
            print("\n🍽️ Recipe Guide Menu")
            print("1️. Add a Recipe")
            print("2️. View/Search Recipes")
            print("3️. Exit")
            
            choice = self.get_user_input("👉 Choose an option: ")
            
            if choice == "1":
                self.add_recipe()
            elif choice == "2":
                self.view_recipes()
            elif choice == "3":
                print("👋 Exiting... Happy cooking!")
                break
            else:
                print("⚠️ Invalid choice! Try again.")

if __name__ == "__main__":
    RecipeGuide().recipe_menu()
