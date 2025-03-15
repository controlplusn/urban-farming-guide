import textwrap

class Recipe:
    def __init__(self, recipe_id, name, ingredients, categories, instructions):
        self.recipe_id = recipe_id
        self.name = name
        self.ingredients = ingredients
        self.categories = categories
        self.instructions = "\n".join(instructions) if isinstance(instructions, list) else instructions

    def display(self):
        """Display recipe details in a structured format."""
        print("\n📖 Recipe Details:")
        print("=" * 100)
        print(f"📌 ID: {self.recipe_id}")
        print(f"🍽️ Name: {self.name}")
        print(f"📂 Categories: {', '.join(self.categories)}")
        print(f"🌿 Ingredients: {', '.join(self.ingredients)}")
        print("📝 Instructions:")
        print(textwrap.fill(self.instructions, width=100))  # Auto-wrap long text for better readability
        print("=" * 100)
