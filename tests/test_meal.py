import unittest
from nutrition_tracker.ingredient import Ingredient
from nutrition_tracker.meal import Meal

class TestMeal(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.ing1 = Ingredient("Chicken Breast", 165, 31, 0, 3.6) # per 100g
        self.ing2 = Ingredient("Brown Rice", 111, 2.6, 23, 0.9)   # per 100g
        self.ing3 = Ingredient("Olive Oil", 884, 0, 0, 100)       # per 100g
        self.meal = Meal("Test Lunch")

    def test_meal_creation_valid(self):
        """Test valid meal creation."""
        self.assertEqual(self.meal.name, "Test Lunch")
        self.assertEqual(len(self.meal._ingredients), 0)
        self.assertEqual(self.meal.total_calories, 0)
        self.assertEqual(self.meal.total_protein, 0)
        self.assertEqual(self.meal.total_carbs, 0)
        self.assertEqual(self.meal.total_fat, 0)
        self.assertEqual(self.meal.total_weight_grams, 0)

    def test_meal_creation_invalid_name(self):
        """Test meal creation with invalid name."""
        with self.assertRaises(ValueError):
            Meal("") # Empty name
        with self.assertRaises(ValueError):
            Meal(None) # type: ignore

    def test_add_ingredient_valid(self):
        """Test adding a valid ingredient to the meal."""
        self.meal.add_ingredient(self.ing1, 200) # 200g of Chicken Breast

        self.assertEqual(len(self.meal._ingredients), 1)
        self.assertEqual(self.meal.total_weight_grams, 200)
        # Expected: cal=165*2, p=31*2, c=0*2, f=3.6*2
        self.assertAlmostEqual(self.meal.total_calories, 330)
        self.assertAlmostEqual(self.meal.total_protein, 62)
        self.assertAlmostEqual(self.meal.total_carbs, 0)
        self.assertAlmostEqual(self.meal.total_fat, 7.2)

        self.meal.add_ingredient(self.ing2, 150) # 150g of Brown Rice
        self.assertEqual(len(self.meal._ingredients), 2)
        self.assertEqual(self.meal.total_weight_grams, 200 + 150) # 350g
        # Chicken: cal=330, p=62, c=0, f=7.2
        # Rice (150g): cal=111*1.5=166.5, p=2.6*1.5=3.9, c=23*1.5=34.5, f=0.9*1.5=1.35
        # Total: cal=330+166.5=496.5, p=62+3.9=65.9, c=0+34.5=34.5, f=7.2+1.35=8.55
        self.assertAlmostEqual(self.meal.total_calories, 496.5)
        self.assertAlmostEqual(self.meal.total_protein, 65.9)
        self.assertAlmostEqual(self.meal.total_carbs, 34.5)
        self.assertAlmostEqual(self.meal.total_fat, 8.55)

    def test_add_ingredient_invalid_type(self):
        """Test adding an invalid type instead of an Ingredient object."""
        with self.assertRaises(TypeError):
            self.meal.add_ingredient("not an ingredient", 100) # type: ignore

    def test_add_ingredient_invalid_weight(self):
        """Test adding an ingredient with invalid weight."""
        with self.assertRaises(ValueError):
            self.meal.add_ingredient(self.ing1, -100) # Negative weight
        with self.assertRaises(ValueError):
            self.meal.add_ingredient(self.ing1, "invalid_weight") # type: ignore

    def test_add_ingredient_zero_weight(self):
        """Test adding an ingredient with zero weight."""
        self.meal.add_ingredient(self.ing1, 0)
        self.assertEqual(self.meal.total_weight_grams, 0)
        self.assertEqual(self.meal.total_calories, 0)
        # Ensure ingredient is still in the list for potential later display, even if 0 weight
        self.assertEqual(len(self.meal._ingredients), 1)


    def test_get_total_nutrition_empty_meal(self):
        """Test getting total nutrition for an empty meal."""
        totals = self.meal.get_total_nutrition()
        expected = {
            "total_calories": 0.0, "total_protein_g": 0.0,
            "total_carbs_g": 0.0, "total_fat_g": 0.0, "total_weight_g": 0.0
        }
        self.assertEqual(totals, expected)

    def test_get_total_nutrition_with_ingredients(self):
        """Test getting total nutrition for a meal with ingredients."""
        self.meal.add_ingredient(self.ing1, 200) # Chicken: 330 Cal, 62 P, 0 C, 7.2 F
        self.meal.add_ingredient(self.ing2, 150) # Rice: 166.5 Cal, 3.9 P, 34.5 C, 1.35 F
        totals = self.meal.get_total_nutrition()
        expected = {
            "total_calories": round(330 + 166.5, 2),
            "total_protein_g": round(62 + 3.9, 2),
            "total_carbs_g": round(0 + 34.5, 2),
            "total_fat_g": round(7.2 + 1.35, 2),
            "total_weight_g": round(200 + 150, 2)
        }
        self.assertEqual(totals, expected)

    def test_get_nutrition_per_100g_empty_meal(self):
        """Test getting nutrition per 100g for an empty meal."""
        per_100g = self.meal.get_nutrition_per_100g()
        expected = {
            "calories_per_100g": None, "protein_per_100g": None,
            "carbs_per_100g": None, "fat_per_100g": None
        }
        self.assertEqual(per_100g, expected)

    def test_get_nutrition_per_100g_with_ingredients(self):
        """Test getting nutrition per 100g for a meal with ingredients."""
        self.meal.add_ingredient(self.ing1, 100) # Chicken: 165 Cal, 31 P, 0 C, 3.6 F (weight 100g)
        self.meal.add_ingredient(self.ing2, 100) # Rice: 111 Cal, 2.6 P, 23 C, 0.9 F (weight 100g)
        # Total weight = 200g
        # Total Cal = 165 + 111 = 276
        # Total P = 31 + 2.6 = 33.6
        # Total C = 0 + 23 = 23
        # Total F = 3.6 + 0.9 = 4.5

        # Per 100g (totals / 2)
        # Cal_100 = 276 / 2 = 138
        # P_100 = 33.6 / 2 = 16.8
        # C_100 = 23 / 2 = 11.5
        # F_100 = 4.5 / 2 = 2.25

        per_100g = self.meal.get_nutrition_per_100g()
        expected = {
            "calories_per_100g": round(276 / 2, 2),
            "protein_per_100g": round(33.6 / 2, 2),
            "carbs_per_100g": round(23 / 2, 2),
            "fat_per_100g": round(4.5 / 2, 2)
        }
        self.assertEqual(per_100g, expected)

    def test_get_nutrition_per_100g_complex_weights(self):
        """Test nutrition per 100g with more complex weights."""
        self.meal.add_ingredient(self.ing1, 175) # Chicken
        self.meal.add_ingredient(self.ing2, 65)  # Rice
        self.meal.add_ingredient(self.ing3, 12)  # Olive Oil

        # Chicken (175g): 165*1.75=288.75 C, 31*1.75=54.25 P, 0 C, 3.6*1.75=6.3 F
        # Rice (65g): 111*0.65=72.15 C, 2.6*0.65=1.69 P, 23*0.65=14.95 C, 0.9*0.65=0.585 F
        # Olive Oil (12g): 884*0.12=106.08 C, 0 P, 0 C, 100*0.12=12 F

        total_w = 175 + 65 + 12 # 252g
        total_c = 288.75 + 72.15 + 106.08 # 467
        total_p = 54.25 + 1.69 + 0 # 55.94
        total_cb = 0 + 14.95 + 0 # 14.95
        total_f = 6.3 + 0.585 + 12 # 18.885

        per_100g = self.meal.get_nutrition_per_100g()
        factor = 100.0 / total_w
        expected = {
            "calories_per_100g": round(total_c * factor, 2),
            "protein_per_100g": round(total_p * factor, 2),
            "carbs_per_100g": round(total_cb * factor, 2),
            "fat_per_100g": round(total_f * factor, 2)
        }
        self.assertEqual(per_100g, expected)

    def test_get_ingredients_list_empty(self):
        """Test getting ingredients list for an empty meal."""
        self.assertEqual(self.meal.get_ingredients_list(), [])

    def test_get_ingredients_list_with_items(self):
        """Test getting ingredients list for a meal with items."""
        self.meal.add_ingredient(self.ing1, 100)
        self.meal.add_ingredient(self.ing2, 50)

        ing_list = self.meal.get_ingredients_list()
        self.assertEqual(len(ing_list), 2)

        # Check first ingredient (Chicken, 100g)
        self.assertEqual(ing_list[0]["name"], "Chicken Breast")
        self.assertEqual(ing_list[0]["weight_g"], 100)
        self.assertAlmostEqual(ing_list[0]["calories"], 165)
        self.assertAlmostEqual(ing_list[0]["protein_g"], 31)
        self.assertAlmostEqual(ing_list[0]["carbs_g"], 0)
        self.assertAlmostEqual(ing_list[0]["fat_g"], 3.6)

        # Check second ingredient (Brown Rice, 50g)
        self.assertEqual(ing_list[1]["name"], "Brown Rice")
        self.assertEqual(ing_list[1]["weight_g"], 50)
        self.assertAlmostEqual(ing_list[1]["calories"], 111 * 0.5)
        self.assertAlmostEqual(ing_list[1]["protein_g"], 2.6 * 0.5)
        self.assertAlmostEqual(ing_list[1]["carbs_g"], 23 * 0.5)
        self.assertAlmostEqual(ing_list[1]["fat_g"], 0.9 * 0.5)

    def test_repr_method(self):
        """Test the __repr__ method of Meal."""
        self.assertEqual(repr(self.meal), "<Meal name='Test Lunch', ingredients_count=0, total_weight=0.00g>")
        self.meal.add_ingredient(self.ing1, 100)
        self.assertEqual(repr(self.meal), "<Meal name='Test Lunch', ingredients_count=1, total_weight=100.00g>")
        self.meal.add_ingredient(self.ing2, 50)
        self.assertEqual(repr(self.meal), "<Meal name='Test Lunch', ingredients_count=2, total_weight=150.00g>")

if __name__ == '__main__':
    unittest.main()
