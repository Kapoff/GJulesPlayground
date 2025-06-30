from .ingredient import Ingredient
from typing import List, Tuple, Dict

class Meal:
    """Represents a meal composed of various ingredients and their weights."""

    def __init__(self, name: str = "My Meal"):
        """
        Initializes a Meal object.

        Args:
            name: The name of the meal.
        """
        if not isinstance(name, str) or not name:
            raise ValueError("Meal name must be a non-empty string.")
        self.name = name
        self._ingredients: List[Tuple[Ingredient, float]] = [] # List of (Ingredient, weight_grams)
        self.total_calories: float = 0.0
        self.total_protein: float = 0.0
        self.total_carbs: float = 0.0
        self.total_fat: float = 0.0
        self.total_weight_grams: float = 0.0

    def add_ingredient(self, ingredient: Ingredient, weight_grams: float) -> None:
        """
        Adds an ingredient with its weight to the meal and updates totals.

        Args:
            ingredient: The Ingredient object.
            weight_grams: The weight of the ingredient in grams.

        Raises:
            ValueError: If weight_grams is negative.
            TypeError: If ingredient is not an Ingredient instance.
        """
        if not isinstance(ingredient, Ingredient):
            raise TypeError("Item added must be an Ingredient object.")
        if not isinstance(weight_grams, (int, float)) or weight_grams < 0:
            raise ValueError("Weight must be a non-negative number.")

        self._ingredients.append((ingredient, weight_grams))

        # Update totals
        calories, protein, carbs, fat = ingredient.get_nutrition_for_weight(weight_grams)
        self.total_calories += calories
        self.total_protein += protein
        self.total_carbs += carbs
        self.total_fat += fat
        self.total_weight_grams += weight_grams
        print(f"Added {weight_grams}g of {ingredient.name} to {self.name}.")

    def get_total_nutrition(self) -> Dict[str, float]:
        """
        Returns the total nutritional information for the entire meal.

        Returns:
            A dictionary with total calories, protein, carbs, fat, and weight.
        """
        return {
            "total_calories": round(self.total_calories, 2),
            "total_protein_g": round(self.total_protein, 2),
            "total_carbs_g": round(self.total_carbs, 2),
            "total_fat_g": round(self.total_fat, 2),
            "total_weight_g": round(self.total_weight_grams, 2),
        }

    def get_nutrition_per_100g(self) -> Dict[str, float | None]:
        """
        Calculates and returns the nutritional information per 100g of the meal.

        Returns:
            A dictionary with calories, protein, carbs, and fat per 100g.
            Returns None for values if total weight is zero to avoid division by zero.
        """
        if self.total_weight_grams == 0:
            return {
                "calories_per_100g": None,
                "protein_per_100g": None,
                "carbs_per_100g": None,
                "fat_per_100g": None,
            }

        factor = 100.0 / self.total_weight_grams
        return {
            "calories_per_100g": round(self.total_calories * factor, 2),
            "protein_per_100g": round(self.total_protein * factor, 2),
            "carbs_per_100g": round(self.total_carbs * factor, 2),
            "fat_per_100g": round(self.total_fat * factor, 2),
        }

    def get_ingredients_list(self) -> List[Dict[str, any]]:
        """Returns a list of ingredients in the meal with their details."""
        ingredients_details = []
        for ingredient, weight in self._ingredients:
            c, p, cb, f = ingredient.get_nutrition_for_weight(weight)
            ingredients_details.append({
                "name": ingredient.name,
                "weight_g": weight,
                "calories": round(c,2),
                "protein_g": round(p,2),
                "carbs_g": round(cb,2),
                "fat_g": round(f,2)
            })
        return ingredients_details

    def __repr__(self) -> str:
        return (f"<Meal name='{self.name}', ingredients_count={len(self._ingredients)}, "
                f"total_weight={self.total_weight_grams:.2f}g>")

# Example usage (optional, can be removed or moved to a main script)
if __name__ == '__main__':
    try:
        # Create some dummy ingredients for testing
        chicken_breast = Ingredient(name="Chicken Breast", calories=165, protein=31, carbs=0, fat=3.6)
        rice = Ingredient(name="Cooked Rice", calories=130, protein=2.7, carbs=28, fat=0.3)
        olive_oil = Ingredient(name="Olive Oil", calories=884, protein=0, carbs=0, fat=100)

        # Create a meal
        my_dinner = Meal(name="Chicken and Rice Dinner")
        print(my_dinner)

        # Add ingredients
        my_dinner.add_ingredient(chicken_breast, 200) # 200g of chicken
        my_dinner.add_ingredient(rice, 150)          # 150g of cooked rice
        my_dinner.add_ingredient(olive_oil, 10)      # 10g of olive oil

        print("\n--- Meal Composition ---")
        for item in my_dinner.get_ingredients_list():
            print(f"- {item['name']}: {item['weight_g']}g (Cals: {item['calories']}, P: {item['protein_g']}g, C: {item['carbs_g']}g, F: {item['fat_g']}g)")


        print("\n--- Total Meal Nutrition ---")
        total_nutrition = my_dinner.get_total_nutrition()
        for key, value in total_nutrition.items():
            print(f"{key.replace('_', ' ').capitalize()}: {value}")

        # Expected total values:
        # Chicken (200g): Cal: 330, P: 62, C: 0, F: 7.2
        # Rice (150g): Cal: 195, P: 4.05, C: 42, F: 0.45
        # Olive Oil (10g): Cal: 88.4, P: 0, C: 0, F: 10
        # Total Cal: 330 + 195 + 88.4 = 613.4
        # Total P: 62 + 4.05 = 66.05
        # Total C: 0 + 42 = 42
        # Total F: 7.2 + 0.45 + 10 = 17.65
        # Total Weight: 200 + 150 + 10 = 360g
        assert abs(total_nutrition["total_calories"] - 613.4) < 0.01
        assert abs(total_nutrition["total_protein_g"] - 66.05) < 0.01
        assert abs(total_nutrition["total_carbs_g"] - 42.0) < 0.01
        assert abs(total_nutrition["total_fat_g"] - 17.65) < 0.01
        assert abs(total_nutrition["total_weight_g"] - 360) < 0.01


        print("\n--- Nutrition Per 100g ---")
        nutrition_per_100g = my_dinner.get_nutrition_per_100g()
        for key, value in nutrition_per_100g.items():
            print(f"{key.replace('_', ' ').capitalize()}: {value}")

        # Expected per 100g (Total / 3.60):
        # Cal: 613.4 / 3.60 = 170.39
        # P: 66.05 / 3.60 = 18.35
        # C: 42 / 3.60 = 11.67
        # F: 17.65 / 3.60 = 4.90
        assert nutrition_per_100g is not None
        if nutrition_per_100g: # Check to satisfy type checker
            assert abs(nutrition_per_100g["calories_per_100g"] - (613.4 / 3.60)) < 0.01
            assert abs(nutrition_per_100g["protein_per_100g"] - (66.05 / 3.60)) < 0.01
            assert abs(nutrition_per_100g["carbs_per_100g"] - (42.0 / 3.60)) < 0.01
            assert abs(nutrition_per_100g["fat_per_100g"] - (17.65 / 3.60)) < 0.01

        print("\nMeal class tests passed (basic).")

        # Test empty meal
        empty_meal = Meal("Empty Plate")
        print("\n--- Empty Meal Nutrition ---")
        print(empty_meal.get_total_nutrition())
        print(empty_meal.get_nutrition_per_100g())
        assert empty_meal.get_total_nutrition()["total_calories"] == 0
        assert empty_meal.get_nutrition_per_100g()["calories_per_100g"] is None
        print("Empty meal test passed.")

        # Test adding ingredient with zero weight
        meal_zero_weight = Meal("Zero Weight Test")
        meal_zero_weight.add_ingredient(chicken_breast, 0)
        print("\n--- Meal with Zero Weight Ingredient ---")
        print(meal_zero_weight.get_total_nutrition())
        assert meal_zero_weight.get_total_nutrition()["total_calories"] == 0
        assert meal_zero_weight.get_total_nutrition()["total_weight_g"] == 0
        print("Zero weight ingredient test passed.")

        # Test error handling
        try:
            my_dinner.add_ingredient(chicken_breast, -100)
        except ValueError as e:
            print(f"\nCorrectly caught error for negative weight: {e}")

        try:
            my_dinner.add_ingredient("not an ingredient", 100) # type: ignore
        except TypeError as e:
            print(f"Correctly caught error for invalid ingredient type: {e}")

        print("\nAll Meal class example usage/tests complete.")

    except Exception as e:
        print(f"An error occurred during Meal example: {e}")
