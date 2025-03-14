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
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️ Error loading data: {e}")
            return []

    def save_data(self, data):
        """Save data to the JSON file."""
        try:
            with open(self.recipe_db, "w") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"⚠️ Error saving data: {e}")

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
        categories = input("📂 Enter recipe categories (comma-separated, e.g., food, herbal): ").strip()

        if not name or not ingredients or not categories:
            print("⚠️ Name, ingredients, and categories cannot be empty!")
            return

        recipes.append({
            "recipeID": recipe_id,
            "recipe_name": name,
            "ingredients": [ingredient.strip() for ingredient in ingredients.split(",")],
            "plant_categories": [category.strip().lower() for category in categories.split(",")]
        })
        self.save_data(recipes)
        print("✅ Recipe added successfully!")

    def view_recipes(self):
        """Display recipe names with IDs and show full recipe details on selection."""
        recipes = self.load_data()
        if not recipes:
            print("⚠️ No recipes found!")
            return

        print("\n📜 Recipe List:")
        print("=" * 60)
        print(f"{'ID':<6} {'Recipe Name':<30} {'Ingredients'}")
        print("-" * 60)
        
        # Loop through the recipes and print them in a table-like format
        for recipe in recipes:
            ingredients = ', '.join(recipe["ingredients"])  # Join ingredients into a single string
            print(f"{recipe['recipeID']:<6} {recipe['recipe_name']:<30} {ingredients}")

        try:
            recipe_id = int(input("\nEnter the recipe ID to view details (or 'q' to cancel): ").strip())
            selected_recipe = next((recipe for recipe in recipes if recipe["recipeID"] == recipe_id), None)

            if selected_recipe:
                # Display recipe details with aligned columns
                print(f"\n📖 Recipe Details for '{selected_recipe['recipe_name']}':")
                print("=" * 60)
                print(f"{'ID':<6}: {selected_recipe['recipeID']}")
                print(f"{'Name':<6}: {selected_recipe['recipe_name']}")
                print(f"{'Ingredients':<6}: {', '.join(selected_recipe['ingredients'])}")
                print(f"{'Categories':<6}: {', '.join(selected_recipe['plant_categories'])}")
                print(f"{'Instructions':<6}: {selected_recipe.get('instructions', 'No instructions available.')}")
                print("=" * 60)
            else:
                print("⚠️ Recipe ID not found.")
    
        except ValueError:
            print("⚠️ Invalid input! Please enter a valid recipe ID.")

    def filter_recipes(self):
        """Filter and display recipes by category."""
        recipes = self.load_data()

        # Extract unique categories from the recipes
        categories = set()
        for recipe in recipes:
            categories.update(recipe["plant_categories"])

        if not categories:
            print("⚠️ No categories found!")
            return

        # Sort categories for better readability
        sorted_categories = sorted(categories)

        # Display available categories
        print("\n🔍 Available Categories:")
        for i, category in enumerate(sorted_categories, 1):
            print(f"{i}. {category}")

        category_choice = input("\nEnter the category number to filter by (or 'q' to cancel): ").strip().lower()

        if category_choice == 'q':
            print("🔙 Returning to the menu...")
            return

        try:
            category_index = int(category_choice) - 1
            if category_index < 0 or category_index >= len(sorted_categories):
                print("⚠️ Invalid choice!")
                return
            category = sorted_categories[category_index]

            # Filter recipes by selected category
            filtered = [recipe for recipe in recipes if category in recipe["plant_categories"]]

            if not filtered:
                print(f"⚠️ No recipes found in the '{category}' category.")
                return

            # Display filtered recipes with clean formatting
            print(f"\n📂 Recipes in '{category}' category:")
            print("=" * 60)
            print(f"{'ID':<6} {'Recipe Name':<30} {'Ingredients'}")
            print("-" * 60)
            for recipe in filtered:
                # Join ingredients into a single string for a cleaner display
                ingredients = ', '.join(recipe["ingredients"])
                print(f"{recipe['recipeID']:<6} {recipe['recipe_name']:<30} {ingredients}")

        except ValueError:
            print("⚠️ Invalid input! Please enter a valid number.")

    def edit_recipe(self):
        """Edit an existing recipe."""
        recipes = self.load_data()
        try:
            recipe_id = int(input("✏️ Enter the ID of the recipe to edit: "))
            for recipe in recipes:
                if recipe["recipeID"] == recipe_id:
                    new_name = input("Enter new name (leave blank to keep current): ").strip() or recipe["recipe_name"]
                    new_ingredients = input("Enter new ingredients (comma-separated, leave blank to keep current): ").strip()
                    new_categories = input("Enter new categories (comma-separated, leave blank to keep current): ").strip() or ', '.join(recipe["plant_categories"])

                    if new_ingredients:
                        recipe["ingredients"] = [ingredient.strip() for ingredient in new_ingredients.split(",")]
                    recipe["recipe_name"] = new_name
                    recipe["plant_categories"] = [category.strip().lower() for category in new_categories.split(",")]

                    self.save_data(recipes)
                    print("✅ Recipe updated successfully!")
                    return
            print("⚠️ Recipe ID not found.")
        except ValueError:
            print("⚠️ Invalid input! Please enter a valid numeric ID.")

    def delete_recipe(self):
        """Delete a recipe by ID."""
        recipes = self.load_data()
        try:
            recipe_id = int(input("🗑️ Enter the ID of the recipe to delete: "))
            updated_recipes = [recipe for recipe in recipes if recipe["recipeID"] != recipe_id]

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
