from flask import Flask, render_template, request, jsonify
from nutrition_tracker.ingredient import Ingredient
from nutrition_tracker.database import IngredientDatabase
from nutrition_tracker.meal import Meal
from nutrition_tracker.history_manager import MealHistoryManager # Added MealHistoryManager import

# Initialize Flask app
app = Flask(__name__)

# Configure database filepaths
DB_FILEPATH = "ingredient_database.json"
MEAL_HISTORY_FILEPATH = "meal_history.json"

# Initialize managers
db = IngredientDatabase(filepath=DB_FILEPATH)
history_manager = MealHistoryManager(filepath=MEAL_HISTORY_FILEPATH)

@app.route('/')
def index():
    # Serves the main landing page
    return render_template('index.html')

@app.route('/add_ingredient')
def add_ingredient_page():
    # Serves the add_ingredient.html page
    return render_template('add_ingredient.html')

@app.route('/shutdown-server', methods=['GET'])
def shutdown_server():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        # This might happen if not running with Werkzeug's dev server
        # (e.g., when deployed with Gunicorn, uWSGI)
        # For simplicity in a dev environment, we'll assume Werkzeug.
        app.logger.warning("Shutdown function not found in request environment. Server may not shut down.")
        return "Error: Could not shut down server. Shutdown function not available. Please close the terminal/script manually.", 500

    try:
        app.logger.info("Server shutdown requested via /shutdown-server endpoint.")
        shutdown_func()
        return "Server is shutting down... You can close this page. Please also close the CLI window if it's still open."
    except Exception as e:
        app.logger.error(f"Error during server shutdown: {e}")
        return f"Error during server shutdown: {e}. Please close the terminal/script manually.", 500

@app.route('/track_meal')
def track_meal_page():
    # Serves the track_meal.html page
    return render_template('track_meal.html')

@app.route('/api/get_ingredients', methods=['GET'])
def get_ingredients_api():
    ingredients = db.list_ingredients()
    ingredient_details = []
    for name in ingredients:
        ing = db.get_ingredient(name)
        if ing:
            ingredient_details.append(ing.to_dict())
    return jsonify(ingredient_details)

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

@app.route('/api/calculate_meal', methods=['POST'])
def calculate_meal_api():
    try:
        data = request.get_json()
        meal_name = data.get('name', 'My Meal')
        ingredient_inputs = data.get('ingredients') # Expected: list of {'name': str, 'weight': float}

        if not ingredient_inputs:
            return jsonify({"success": False, "message": "No ingredients provided for the meal."}), 400

        meal = Meal(name=meal_name)
        missing_ingredients = []

        for item in ingredient_inputs:
            ingredient_name = item.get('name')
            weight = item.get('weight')

            if not ingredient_name or weight is None:
                return jsonify({"success": False, "message": "Invalid ingredient data: name and weight are required."}), 400

            try:
                weight_float = float(weight)
                if weight_float < 0:
                     return jsonify({"success": False, "message": f"Weight for {ingredient_name} cannot be negative."}), 400
            except ValueError:
                return jsonify({"success": False, "message": f"Invalid weight format for {ingredient_name}."}), 400


            ingredient_obj = db.get_ingredient(ingredient_name)
            if not ingredient_obj:
                missing_ingredients.append(ingredient_name)
            else:
                meal.add_ingredient(ingredient_obj, weight_float)

        if missing_ingredients:
            return jsonify({"success": False, "message": f"The following ingredients were not found in the database: {', '.join(missing_ingredients)}. Please add them first."}), 404

        if not meal._ingredients: # Accessing protected member, but Meal class uses it
             return jsonify({"success": False, "message": "Meal is empty or contains only missing ingredients."}), 400


        total_nutrition = meal.get_total_nutrition()
        nutrition_per_100g = meal.get_nutrition_per_100g()
        ingredients_list_details = meal.get_ingredients_list() # Detailed list with calculated nutrition for each ingredient

        # Save to history if requested
        should_save_meal = data.get('save_meal', False) # Expect a boolean in the request
        if should_save_meal:
            # We need the ingredient list as {name, weight} for history, not the detailed one
            ingredients_for_history = [{"name": item.get('name'), "weight_g": item.get('weight')} for item in ingredient_inputs]
            history_manager.add_meal(
                meal_name=meal.name,
                ingredients_used=ingredients_for_history,
                total_nutrition=total_nutrition,
                nutrition_per_100g=nutrition_per_100g
            )

        return jsonify({
            "success": True,
            "meal_name": meal.name,
            "total_nutrition": total_nutrition,
            "nutrition_per_100g": nutrition_per_100g,
            "ingredients_list": ingredients_list_details
        })

    except ValueError as e:
        app.logger.error(f"ValueError in calculate_meal_api: {e}")
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error in calculate_meal_api: {e}")
        return jsonify({"success": False, "message": "An unexpected error occurred during meal calculation."}), 500


# --- Meal History API Endpoints ---

@app.route('/api/get_meal_history', methods=['GET'])
def get_meal_history_api():
    try:
        meal_summaries = history_manager.get_all_meals_summary()
        return jsonify({"success": True, "history": meal_summaries})
    except Exception as e:
        app.logger.error(f"Error in get_meal_history_api: {e}")
        return jsonify({"success": False, "message": "Failed to retrieve meal history."}), 500

@app.route('/api/get_meal_detail/<meal_id>', methods=['GET'])
def get_meal_detail_api(meal_id):
    try:
        meal_detail = history_manager.get_meal_by_id(meal_id)
        if meal_detail:
            return jsonify({"success": True, "meal": meal_detail})
        else:
            return jsonify({"success": False, "message": "Meal not found."}), 404
    except Exception as e:
        app.logger.error(f"Error in get_meal_detail_api for meal_id {meal_id}: {e}")
        return jsonify({"success": False, "message": "Failed to retrieve meal details."}), 500

@app.route('/api/delete_meal/<meal_id>', methods=['DELETE'])
def delete_meal_api(meal_id):
    try:
        if history_manager.delete_meal(meal_id):
            return jsonify({"success": True, "message": "Meal deleted successfully."})
        else:
            # This could mean meal not found, or delete operation failed for other reasons
            # history_manager.delete_meal returns False if meal_id not found.
            return jsonify({"success": False, "message": "Meal not found or could not be deleted."}), 404
    except Exception as e:
        app.logger.error(f"Error in delete_meal_api for meal_id {meal_id}: {e}")
        return jsonify({"success": False, "message": "Failed to delete meal."}), 500


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
