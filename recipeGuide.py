import json
import textwrap

class RecipeManager:
    def __init__(self, recipe_db="recipes.json"):
        self.recipe_db = recipe_db

    def load_data(self):
        """Load data from the JSON file."""
        try:
            with open(self.recipe_db, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def save_data(self, data):
        """Save data to the JSON file."""
        try:
            with open(self.recipe_db, "w") as f:
                json.dump(data, f, indent=4)
        except IOError:
            print("⚠️ Error saving data!")

    def generate_recipe_id(self):
        """Generate a new unique recipe ID."""
        recipes = self.load_data()
        return max((recipe["recipeID"] for recipe in recipes), default=0) + 1

    def add_recipe(self):
        """Add a new recipe to the database."""
        recipes = self.load_data()
        recipe_id = self.generate_recipe_id()

        name = input("🍽️ Enter recipe name: ").strip()
        ingredients = input("🌿 Enter ingredients (comma-separated): ").strip()
        categories = input("📂 Enter recipe categories (comma-separated): ").strip()
        instructions = input("📝 Enter instructions: ").strip()

        if not name or not ingredients or not categories or not instructions:
            print("⚠️ All fields are required!")
            return

        recipes.append({
            "recipeID": recipe_id,
            "recipe_name": name,
            "ingredients": [i.strip() for i in ingredients.split(",")],
            "plant_categories": [c.strip().lower() for c in categories.split(",")],
            "instructions": instructions
        })
        self.save_data(recipes)
        print("✅ Recipe added successfully!")

    def view_recipes(self):
        """Display recipe names with IDs and show full recipe details on selection."""
        recipes = self.load_data()
        if not recipes:
            print("⚠️ No recipes found!")
            return

        print("\n📜 Available Recipes:")
        for recipe in recipes:
            print(f"🔹 {recipe['recipeID']}: {recipe['recipe_name']}")

        while True:
            recipe_id = input("\n🔍 Enter a Recipe ID to view details (or 'q' to go back): ").strip().lower()
            if recipe_id == 'q':
                return

            if not recipe_id.isdigit():
                print("⚠️ Invalid input! Please enter a numeric ID.")
                continue

            recipe_id = int(recipe_id)
            selected_recipe = next((r for r in recipes if r["recipeID"] == recipe_id), None)

            if selected_recipe:
                print("\n📖 Recipe Details:")
                print("=" * 40)
                print(f"📌 ID: {selected_recipe['recipeID']}")
                print(f"🍽️ Name: {selected_recipe['recipe_name']}")
                print(f"📂 Category: {', '.join(selected_recipe['plant_categories'])}")
                print(f"🌿 Ingredients: {', '.join(selected_recipe['ingredients'])}")

                instructions = selected_recipe.get("instructions", "No instructions provided.")
                if isinstance(instructions, list):
                    instructions = "\n".join(instructions)

                print("\n📝 Instructions:")
                print(textwrap.fill(instructions, width=100))
            else:
                print("⚠️ Recipe ID not found. Try again.")

    def filter_recipes(self):
        """Filter and display recipes by category with full details."""
        recipes = self.load_data()
        categories = sorted({cat for recipe in recipes for cat in recipe["plant_categories"]})

        if not categories:
            print("⚠️ No categories found!")
            return

        print("\n🔍 Available Categories:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")

        choice = input("\nEnter category number (or 'q' to cancel): ").strip().lower()
        if choice == 'q':
            return

        if not choice.isdigit() or not (1 <= int(choice) <= len(categories)):
            print("⚠️ Invalid choice!")
            return

        category = categories[int(choice) - 1]
        filtered = [r for r in recipes if category in r["plant_categories"]]

        if not filtered:
            print(f"⚠️ No recipes found in '{category}'.")
            return

        print(f"\n📂 Recipes in '{category}' category:")
        print("=" * 40)

        for recipe in filtered:
            print(f"📌 ID: {recipe['recipeID']}")
            print(f"🍽️ Name: {recipe['recipe_name']}")
            print(f"🌿 Ingredients: {', '.join(recipe['ingredients'])}")
            print(f"📂 Categories: {', '.join(recipe['plant_categories'])}")

            instructions = recipe.get("instructions", "No instructions provided.")
            if isinstance(instructions, list):
                instructions = "\n".join(instructions)

            print("\n📝 Instructions:")
            print(textwrap.fill(instructions, width=100))
            print("=" * 40)

    def edit_recipe(self):
        """Edit an existing recipe."""
        recipes = self.load_data()
        try:
            recipe_id = int(input("✏️ Enter the ID of the recipe to edit: "))
            recipe = next((r for r in recipes if r["recipeID"] == recipe_id), None)

            if recipe:
                recipe["recipe_name"] = input("Enter new name (leave blank to keep current): ").strip() or recipe["recipe_name"]
                new_ingredients = input("Enter new ingredients (comma-separated, leave blank to keep current): ").strip()
                new_categories = input("Enter new categories (comma-separated, leave blank to keep current): ").strip()
                new_instructions = input("Enter new instructions (leave blank to keep current): ").strip()

                if new_ingredients:
                    recipe["ingredients"] = [i.strip() for i in new_ingredients.split(",")]
                if new_categories:
                    recipe["plant_categories"] = [c.strip().lower() for c in new_categories.split(",")]
                if new_instructions:
                    recipe["instructions"] = new_instructions

                self.save_data(recipes)
                print("✅ Recipe updated successfully!")
            else:
                print("⚠️ Recipe ID not found.")
        except ValueError:
            print("⚠️ Invalid input! Please enter a valid numeric ID.")

    def delete_recipe(self):
        """Delete a recipe by ID."""
        recipes = self.load_data()
        try:
            recipe_id = int(input("🗑️ Enter the ID of the recipe to delete: "))
            updated_recipes = [r for r in recipes if r["recipeID"] != recipe_id]

            if len(updated_recipes) == len(recipes):
                print("⚠️ Recipe ID not found.")
            else:
                self.save_data(updated_recipes)
                print("✅ Recipe deleted successfully!")
        except ValueError:
            print("⚠️ Invalid input! Please enter a valid numeric ID.")

    def recipe_menu(self):
        """Display the recipe management menu and handle user input."""
        while True:
            print("\n🍽️ Recipe Management Menu 🍽️")
            print("1. Add Recipe")
            print("2. View All Recipes")
            print("3. Filter Recipes by Category")
            print("4. Edit Recipe")
            print("5. Delete Recipe")
            print("6. Back to Main Menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_recipe()
            elif choice == "2":
                self.view_recipes()
            elif choice == "3":
                self.filter_recipes()
            elif choice == "4":
                self.edit_recipe()
            elif choice == "5":
                self.delete_recipe()
            elif choice == "6":
                print("🔙 Returning to main menu...")
                break
            else:
                print("⚠️ Invalid choice! Please try again.")

if __name__ == "__main__":
    manager = RecipeManager()
    manager.recipe_menu()
