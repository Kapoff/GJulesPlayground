import json
import os
import uuid
from datetime import datetime, timezone

class MealHistoryManager:
    def __init__(self, filepath="meal_history.json"):
        self.filepath = filepath
        self.history = self._load_history()

    def _load_history(self):
        """Loads meal history from the JSON file."""
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                # Could add data validation here if needed
                return data
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading meal history from {self.filepath}: {e}")
            return []

    def _save_history(self):
        """Saves the current meal history to the JSON file."""
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.history, f, indent=4)
        except IOError as e:
            print(f"Error saving meal history to {self.filepath}: {e}")

    def add_meal(self, meal_name, ingredients_used, total_nutrition, nutrition_per_100g):
        """
        Adds a new meal to the history.

        Args:
            meal_name (str): The name of the meal.
            ingredients_used (list): List of dicts, e.g., [{"name": "Chicken Breast", "weight_g": 150}, ...].
            total_nutrition (dict): Dictionary of total nutritional values for the meal.
            nutrition_per_100g (dict): Dictionary of nutritional values per 100g of the meal.

        Returns:
            dict: The newly added meal entry with its ID and timestamp.
        """
        new_meal_entry = {
            "id": str(uuid.uuid4()),
            "name": meal_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ingredients_used": ingredients_used,
            "total_nutrition": total_nutrition,
            "nutrition_per_100g": nutrition_per_100g
        }
        self.history.append(new_meal_entry)
        self._save_history()
        return new_meal_entry

    def get_all_meals_summary(self):
        """
        Returns a list of all meals with summary information, sorted by most recent first.
        Summary includes: id, name, timestamp, and total calories.
        """
        summaries = []
        for meal in sorted(self.history, key=lambda x: x.get("timestamp", ""), reverse=True):
            summary = {
                "id": meal.get("id"),
                "name": meal.get("name"),
                "timestamp": meal.get("timestamp"),
                # Extracting total calories for the preview
                "total_calories": meal.get("total_nutrition", {}).get("total_calories", 0)
            }
            summaries.append(summary)
        return summaries

    def get_meal_by_id(self, meal_id):
        """
        Retrieves a single meal by its ID.

        Args:
            meal_id (str): The unique ID of the meal.

        Returns:
            dict or None: The meal data if found, otherwise None.
        """
        for meal in self.history:
            if meal.get("id") == meal_id:
                return meal
        return None

    def delete_meal(self, meal_id):
        """
        Deletes a meal from the history by its ID.

        Args:
            meal_id (str): The unique ID of the meal to delete.

        Returns:
            bool: True if the meal was found and deleted, False otherwise.
        """
        initial_len = len(self.history)
        self.history = [meal for meal in self.history if meal.get("id") != meal_id]
        if len(self.history) < initial_len:
            self._save_history()
            return True
        return False

if __name__ == '__main__':
    # Example Usage (for testing the manager directly)
    hm = MealHistoryManager(filepath="test_meal_history.json")

    # Clear existing test file for a clean run
    if os.path.exists("test_meal_history.json"):
        os.remove("test_meal_history.json")

    hm = MealHistoryManager(filepath="test_meal_history.json") # Re-init after delete for empty history

    print("Initial history (should be empty):", hm.get_all_meals_summary())

    meal1_details = {
        "name": "Lunch Delight",
        "ingredients_used": [{"name": "Chicken", "weight_g": 100}, {"name": "Rice", "weight_g": 150}],
        "total_nutrition": {"total_calories": 500, "total_protein_g": 40},
        "nutrition_per_100g": {"calories_per_100g": 200}
    }
    added_meal1 = hm.add_meal(
        meal_name=meal1_details["name"],
        ingredients_used=meal1_details["ingredients_used"],
        total_nutrition=meal1_details["total_nutrition"],
        nutrition_per_100g=meal1_details["nutrition_per_100g"]
    )
    print("\nAdded meal 1:", added_meal1["id"])

    meal2_details = {
        "name": "Quick Snack",
        "ingredients_used": [{"name": "Apple", "weight_g": 150}],
        "total_nutrition": {"total_calories": 95, "total_protein_g": 0.5},
        "nutrition_per_100g": {"calories_per_100g": 63}
    }
    added_meal2 = hm.add_meal(
        meal_name=meal2_details["name"],
        ingredients_used=meal2_details["ingredients_used"],
        total_nutrition=meal2_details["total_nutrition"],
        nutrition_per_100g=meal2_details["nutrition_per_100g"]
    )
    print("Added meal 2:", added_meal2["id"])

    print("\nFull history summary:", hm.get_all_meals_summary())

    retrieved_meal = hm.get_meal_by_id(added_meal1["id"])
    print(f"\nRetrieved meal {added_meal1['id']}:", retrieved_meal is not None)

    retrieved_nonexistent = hm.get_meal_by_id("nonexistent-id")
    print("Retrieved nonexistent meal:", retrieved_nonexistent is None)

    deleted = hm.delete_meal(added_meal1["id"])
    print(f"\nDeleted meal {added_meal1['id']}:", deleted)

    deleted_again = hm.delete_meal(added_meal1["id"])
    print(f"Attempted to delete meal {added_meal1['id']} again:", not deleted_again)

    print("\nHistory after deletion:", hm.get_all_meals_summary())

    # Clean up test file
    if os.path.exists("test_meal_history.json"):
        os.remove("test_meal_history.json")
        print("\nCleaned up test_meal_history.json")

    # Test error handling for load (manual step: create a malformed test_meal_history.json)
    # with open("test_meal_history.json", "w") as f:
    #     f.write("this is not json")
    # hm_error = MealHistoryManager(filepath="test_meal_history.json")
    # print("\nHistory after loading malformed file:", hm_error.history) # Should be []
    # if os.path.exists("test_meal_history.json"):
    #     os.remove("test_meal_history.json")

    print("History manager test complete.")
