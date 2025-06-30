from nutrition_tracker.ingredient import Ingredient
from nutrition_tracker.database import IngredientDatabase
from nutrition_tracker.meal import Meal

DB_FILEPATH = "ingredient_database.json"

def get_float_input(prompt: str) -> float:
    """Gets a non-negative float input from the user."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Value cannot be negative. Please try again.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_string_input(prompt: str) -> str:
    """Gets a non-empty string input from the user."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        else:
            print("Input cannot be empty. Please try again.")

def manage_ingredients(db: IngredientDatabase):
    """Handles UI for managing ingredients."""
    while True:
        print("\n--- Manage Ingredients ---")
        print("1. Add New Ingredient")
        print("2. View All Ingredients")
        print("3. Remove Ingredient")
        print("4. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("\n--- Add New Ingredient (values per 100g) ---")
            name = get_string_input("Ingredient name: ")
            if db.get_ingredient(name):
                print(f"Ingredient '{name}' already exists. To update, remove it first and then add again.")
                continue
            calories = get_float_input("Calories per 100g: ")
            protein = get_float_input("Protein (g) per 100g: ")
            carbs = get_float_input("Carbohydrates (g) per 100g: ")
            fat = get_float_input("Fat (g) per 100g: ")

            try:
                ingredient = Ingredient(name, calories, protein, carbs, fat)
                db.add_ingredient(ingredient)
                db.save_ingredients() # Save after each addition
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        elif choice == '2':
            print("\n--- All Ingredients ---")
            ingredients = db.list_ingredients()
            if not ingredients:
                print("No ingredients in the database.")
            else:
                for name in ingredients:
                    ing = db.get_ingredient(name)
                    if ing:
                        print(f"- {ing.name} (per 100g): {ing.calories} kcal, {ing.protein}g P, {ing.carbs}g C, {ing.fat}g F")

        elif choice == '3':
            print("\n--- Remove Ingredient ---")
            name = get_string_input("Enter name of ingredient to remove: ")
            if db.remove_ingredient(name):
                db.save_ingredients() # Save after removal
            else:
                print(f"Ingredient '{name}' not found.")

        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

def create_meal(db: IngredientDatabase):
    """Handles UI for creating a meal and calculating its nutrition."""
    print("\n--- Create New Meal ---")
    meal_name = get_string_input("Enter a name for your meal: ")
    meal = Meal(name=meal_name)

    while True:
        print("\nAvailable ingredients:")
        ingredients_list = db.list_ingredients()
        if not ingredients_list:
            print("No ingredients in database. Please add some first from the 'Manage Ingredients' menu.")
            return

        for i, name in enumerate(ingredients_list):
            print(f"{i + 1}. {name}")

        print(f"{len(ingredients_list) + 1}. Finish Adding Ingredients")

        try:
            choice_idx = int(input(f"Choose an ingredient to add (1-{len(ingredients_list) + 1}): ")) - 1

            if choice_idx == len(ingredients_list): # Finish adding
                break

            if 0 <= choice_idx < len(ingredients_list):
                ingredient_name = ingredients_list[choice_idx]
                ingredient_obj = db.get_ingredient(ingredient_name)
                if not ingredient_obj: # Should not happen if list is correct
                    print("Error: Ingredient not found.")
                    continue

                weight = get_float_input(f"Enter weight of {ingredient_name} in grams: ")
                meal.add_ingredient(ingredient_obj, weight)
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number for your choice.")

    if not meal._ingredients:
        print("Meal is empty. No nutrition to calculate.")
        return

    print(f"\n--- Nutrition for {meal.name} ---")

    print("\nIngredients in this meal:")
    for item in meal.get_ingredients_list():
        print(f"- {item['name']}: {item['weight_g']}g (Cals: {item['calories']:.1f}, P: {item['protein_g']:.1f}g, C: {item['carbs_g']:.1f}g, F: {item['fat_g']:.1f}g)")

    total_nutrition = meal.get_total_nutrition()
    print("\nTotal Meal Nutrition:")
    print(f"  Total Weight: {total_nutrition['total_weight_g']:.1f}g")
    print(f"  Total Calories: {total_nutrition['total_calories']:.1f} kcal")
    print(f"  Total Protein: {total_nutrition['total_protein_g']:.1f}g")
    print(f"  Total Carbs: {total_nutrition['total_carbs_g']:.1f}g")
    print(f"  Total Fat: {total_nutrition['total_fat_g']:.1f}g")

    nutrition_100g = meal.get_nutrition_per_100g()
    print("\nNutrition per 100g of Meal:")
    if nutrition_100g["calories_per_100g"] is not None:
        print(f"  Calories: {nutrition_100g['calories_per_100g']:.1f} kcal")
        print(f"  Protein: {nutrition_100g['protein_per_100g']:.1f}g")
        print(f"  Carbs: {nutrition_100g['carbs_per_100g']:.1f}g")
        print(f"  Fat: {nutrition_100g['fat_per_100g']:.1f}g")
    else:
        print("  Cannot calculate per 100g as meal weight is zero.")


def main():
    """Main function to run the CLI application."""
    db = IngredientDatabase(filepath=DB_FILEPATH)

    while True:
        print("\n========== Nutrition Tracker CLI ==========")
        print("1. Manage Ingredients")
        print("2. Create Meal & Calculate Nutrition")
        print("3. Exit")
        main_choice = input("Enter your choice: ")

        if main_choice == '1':
            manage_ingredients(db)
        elif main_choice == '2':
            create_meal(db)
        elif main_choice == '3':
            print("Exiting Nutrition Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Create the package structure if it doesn't exist
    import os
    if not os.path.exists("nutrition_tracker"):
        os.makedirs("nutrition_tracker")

    # Create an empty __init__.py if it doesn't exist to make nutrition_tracker a package
    if not os.path.exists("nutrition_tracker/__init__.py"):
        with open("nutrition_tracker/__init__.py", "w") as f:
            pass # Empty file is fine

    main()
