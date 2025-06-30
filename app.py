from flask import Flask, render_template, request, jsonify
from nutrition_tracker.ingredient import Ingredient
from nutrition_tracker.database import IngredientDatabase

# Initialize Flask app
app = Flask(__name__)

# Configure the database filepath
# This should match the one used in main_cli.py if you want them to share data
DB_FILEPATH = "ingredient_database.json"
db = IngredientDatabase(filepath=DB_FILEPATH)

@app.route('/')
def index():
    # Serves the add_ingredient.html page
    return render_template('add_ingredient.html')

@app.route('/api/add_ingredient', methods=['POST'])
def add_ingredient_api():
    try:
        data = request.get_json()

        name = data.get('name')
        portion_size_g = float(data.get('portion_size', 100.0)) # g
        calories_input = float(data.get('calories'))
        protein_input = float(data.get('protein'))
        carbs_input = float(data.get('carbs'))
        fat_input = float(data.get('fat'))

        if not all([name, calories_input is not None, protein_input is not None, carbs_input is not None, fat_input is not None]):
            return jsonify({"success": False, "message": "Missing required fields."}), 400

        if portion_size_g <= 0:
            return jsonify({"success": False, "message": "Portion size must be greater than zero."}), 400

        # Normalize to per 100g
        # The Ingredient class expects all nutritional info to be per 100g
        factor = 100.0 / portion_size_g
        calories_100g = calories_input * factor
        protein_100g = protein_input * factor
        carbs_100g = carbs_input * factor
        fat_100g = fat_input * factor

        # Check if ingredient already exists
        if db.get_ingredient(name):
            return jsonify({"success": False, "message": f"Ingredient '{name}' already exists. To update, please remove it first via CLI or future update feature."}), 409 # 409 Conflict

        ingredient = Ingredient(name, calories_100g, protein_100g, carbs_100g, fat_100g)
        db.add_ingredient(ingredient)
        db.save_ingredients() # Persist to file

        return jsonify({"success": True, "message": f"Ingredient '{name}' added successfully."})

    except ValueError as e:
        # Handles potential errors from Ingredient class validation (e.g., negative values)
        # or float conversion errors if data is not numeric.
        app.logger.error(f"ValueError in add_ingredient_api: {e}")
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error in add_ingredient_api: {e}")
        return jsonify({"success": False, "message": "An unexpected error occurred."}), 500

if __name__ == '__main__':
    # Create the nutrition_tracker package directory and __init__.py if they don't exist
    # This ensures that 'from nutrition_tracker.ingredient import Ingredient' works
    # when running app.py directly for the first time in a clean environment.
    import os
    if not os.path.exists("nutrition_tracker"):
        os.makedirs("nutrition_tracker")
    if not os.path.exists("nutrition_tracker/__init__.py"):
        with open("nutrition_tracker/__init__.py", "w") as f:
            pass # Empty file is fine to make it a package

    app.run(debug=True)
