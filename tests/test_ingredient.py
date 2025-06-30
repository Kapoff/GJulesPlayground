import unittest
from nutrition_tracker.ingredient import Ingredient

class TestIngredient(unittest.TestCase):

    def test_ingredient_creation_valid(self):
        """Test valid ingredient creation."""
        ing = Ingredient("Apple", 52, 0.3, 14, 0.2)
        self.assertEqual(ing.name, "Apple")
        self.assertEqual(ing.calories, 52)
        self.assertEqual(ing.protein, 0.3)
        self.assertEqual(ing.carbs, 14)
        self.assertEqual(ing.fat, 0.2)

    def test_ingredient_creation_invalid_name(self):
        """Test ingredient creation with invalid name."""
        with self.assertRaises(ValueError):
            Ingredient("", 52, 0.3, 14, 0.2) # Empty name
        with self.assertRaises(ValueError):
            Ingredient(None, 52, 0.3, 14, 0.2) # type: ignore

    def test_ingredient_creation_invalid_calories(self):
        """Test ingredient creation with invalid calories."""
        with self.assertRaises(ValueError):
            Ingredient("Apple", -52, 0.3, 14, 0.2) # Negative calories
        with self.assertRaises(ValueError):
            Ingredient("Apple", "invalid", 0.3, 14, 0.2) # type: ignore

    def test_ingredient_creation_invalid_protein(self):
        """Test ingredient creation with invalid protein."""
        with self.assertRaises(ValueError):
            Ingredient("Apple", 52, -0.3, 14, 0.2) # Negative protein
        with self.assertRaises(ValueError):
            Ingredient("Apple", 52, "invalid", 14, 0.2) # type: ignore

    def test_ingredient_creation_invalid_carbs(self):
        """Test ingredient creation with invalid carbs."""
        with self.assertRaises(ValueError):
            Ingredient("Apple", 52, 0.3, -14, 0.2) # Negative carbs
        with self.assertRaises(ValueError):
            Ingredient("Apple", 52, 0.3, "invalid", 0.2) # type: ignore

    def test_ingredient_creation_invalid_fat(self):
        """Test ingredient creation with invalid fat."""
        with self.assertRaises(ValueError):
            Ingredient("Apple", 52, 0.3, 14, -0.2) # Negative fat
        with self.assertRaises(ValueError):
            Ingredient("Apple", 52, 0.3, 14, "invalid") # type: ignore

    def test_get_nutrition_for_weight_valid(self):
        """Test get_nutrition_for_weight with valid weight."""
        ing = Ingredient("Test Food", 200, 10, 20, 5) # per 100g

        # Test for 100g
        calories, protein, carbs, fat = ing.get_nutrition_for_weight(100)
        self.assertEqual(calories, 200)
        self.assertEqual(protein, 10)
        self.assertEqual(carbs, 20)
        self.assertEqual(fat, 5)

        # Test for 50g
        calories, protein, carbs, fat = ing.get_nutrition_for_weight(50)
        self.assertEqual(calories, 100)
        self.assertEqual(protein, 5)
        self.assertEqual(carbs, 10)
        self.assertEqual(fat, 2.5)

        # Test for 200g
        calories, protein, carbs, fat = ing.get_nutrition_for_weight(200)
        self.assertEqual(calories, 400)
        self.assertEqual(protein, 20)
        self.assertEqual(carbs, 40)
        self.assertEqual(fat, 10)

        # Test for 0g
        calories, protein, carbs, fat = ing.get_nutrition_for_weight(0)
        self.assertEqual(calories, 0)
        self.assertEqual(protein, 0)
        self.assertEqual(carbs, 0)
        self.assertEqual(fat, 0)

    def test_get_nutrition_for_weight_invalid_weight(self):
        """Test get_nutrition_for_weight with invalid weight."""
        ing = Ingredient("Test Food", 200, 10, 20, 5)
        with self.assertRaises(ValueError):
            ing.get_nutrition_for_weight(-100) # Negative weight
        with self.assertRaises(ValueError):
            ing.get_nutrition_for_weight("invalid") # type: ignore

    def test_to_dict(self):
        """Test serialization to dictionary."""
        ing = Ingredient("Apple", 52, 0.3, 14, 0.2)
        expected_dict = {
            "name": "Apple",
            "calories": 52.0,
            "protein": 0.3,
            "carbs": 14.0,
            "fat": 0.2
        }
        self.assertEqual(ing.to_dict(), expected_dict)

    def test_from_dict_valid(self):
        """Test deserialization from dictionary."""
        data = {
            "name": "Banana",
            "calories": 89,
            "protein": 1.1,
            "carbs": 23,
            "fat": 0.3
        }
        ing = Ingredient.from_dict(data)
        self.assertEqual(ing.name, "Banana")
        self.assertEqual(ing.calories, 89)
        self.assertEqual(ing.protein, 1.1)
        self.assertEqual(ing.carbs, 23)
        self.assertEqual(ing.fat, 0.3)

    def test_from_dict_missing_keys(self):
        """Test deserialization from dictionary with missing keys."""
        data = {"name": "Incomplete"}
        with self.assertRaises(ValueError): # Changed from KeyError to ValueError based on implementation
            Ingredient.from_dict(data)

    def test_from_dict_invalid_data_types(self):
        """Test deserialization from dictionary with invalid data types for nutritional values."""
        data = {
            "name": "Banana",
            "calories": "eighty-nine", # Invalid type
            "protein": 1.1,
            "carbs": 23,
            "fat": 0.3
        }
        with self.assertRaises(ValueError): # Catches during __init__
            Ingredient.from_dict(data)

    def test_repr(self):
        """Test __repr__ method."""
        ing = Ingredient("Apple", 52, 0.3, 14, 0.2)
        self.assertEqual(repr(ing), "Ingredient(name='Apple', calories=52.0, protein=0.3, carbs=14.0, fat=0.2)")

if __name__ == '__main__':
    unittest.main()
