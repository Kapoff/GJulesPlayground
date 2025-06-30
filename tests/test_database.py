import unittest
import os
import json
from nutrition_tracker.ingredient import Ingredient
from nutrition_tracker.database import IngredientDatabase

class TestIngredientDatabase(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.test_db_filepath = "test_db_file.json"
        # Ensure the test file does not exist before each test
        if os.path.exists(self.test_db_filepath):
            os.remove(self.test_db_filepath)
        self.db = IngredientDatabase(filepath=self.test_db_filepath)
        self.ing1 = Ingredient("Apple", 52, 0.3, 14, 0.2)
        self.ing2 = Ingredient("Banana", 89, 1.1, 23, 0.3)

    def tearDown(self):
        """Clean up after test methods."""
        if os.path.exists(self.test_db_filepath):
            os.remove(self.test_db_filepath)

    def test_initial_database_empty(self):
        """Test that a new database is initially empty if file doesn't exist."""
        self.assertEqual(len(self.db.list_ingredients()), 0)

    def test_add_ingredient_valid(self):
        """Test adding a valid ingredient."""
        self.db.add_ingredient(self.ing1)
        self.assertEqual(len(self.db.list_ingredients()), 1)
        self.assertIn("Apple", self.db.list_ingredients())
        retrieved_ing = self.db.get_ingredient("Apple")
        self.assertIsNotNone(retrieved_ing)
        if retrieved_ing: # For type checker
          self.assertEqual(retrieved_ing.name, "Apple")

    def test_add_ingredient_duplicate_name(self):
        """Test adding an ingredient with a duplicate name."""
        self.db.add_ingredient(self.ing1)
        with self.assertRaises(ValueError):
            self.db.add_ingredient(Ingredient("Apple", 100, 1, 1, 1))

    def test_add_ingredient_invalid_type(self):
        """Test adding an invalid type instead of an Ingredient object."""
        with self.assertRaises(TypeError):
            self.db.add_ingredient("not an ingredient") # type: ignore

    def test_get_ingredient_exists(self):
        """Test getting an existing ingredient."""
        self.db.add_ingredient(self.ing1)
        retrieved = self.db.get_ingredient("Apple")
        self.assertEqual(retrieved, self.ing1)

    def test_get_ingredient_not_exists(self):
        """Test getting a non-existent ingredient."""
        retrieved = self.db.get_ingredient("Orange")
        self.assertIsNone(retrieved)

    def test_list_ingredients(self):
        """Test listing ingredients."""
        self.assertEqual(self.db.list_ingredients(), [])
        self.db.add_ingredient(self.ing1)
        self.db.add_ingredient(self.ing2)
        self.assertCountEqual(self.db.list_ingredients(), ["Apple", "Banana"]) # Order doesn't matter

    def test_remove_ingredient_exists(self):
        """Test removing an existing ingredient."""
        self.db.add_ingredient(self.ing1)
        self.assertTrue(self.db.remove_ingredient("Apple"))
        self.assertEqual(len(self.db.list_ingredients()), 0)
        self.assertIsNone(self.db.get_ingredient("Apple"))

    def test_remove_ingredient_not_exists(self):
        """Test removing a non-existent ingredient."""
        self.assertFalse(self.db.remove_ingredient("Orange"))
        self.assertEqual(len(self.db.list_ingredients()), 0)

    def test_save_and_load_ingredients_empty(self):
        """Test saving and loading an empty database."""
        self.db.save_ingredients()
        new_db = IngredientDatabase(filepath=self.test_db_filepath)
        self.assertEqual(len(new_db.list_ingredients()), 0)

    def test_save_and_load_ingredients_with_data(self):
        """Test saving and loading a database with ingredients."""
        self.db.add_ingredient(self.ing1)
        self.db.add_ingredient(self.ing2)
        self.db.save_ingredients()

        new_db = IngredientDatabase(filepath=self.test_db_filepath)
        self.assertEqual(len(new_db.list_ingredients()), 2)
        retrieved_ing1 = new_db.get_ingredient("Apple")
        retrieved_ing2 = new_db.get_ingredient("Banana")

        self.assertIsNotNone(retrieved_ing1)
        self.assertIsNotNone(retrieved_ing2)

        if retrieved_ing1 and retrieved_ing2: # For type checker
            self.assertEqual(retrieved_ing1.name, self.ing1.name)
            self.assertEqual(retrieved_ing1.calories, self.ing1.calories)
            self.assertEqual(retrieved_ing2.name, self.ing2.name)
            self.assertEqual(retrieved_ing2.calories, self.ing2.calories)

    def test_load_ingredients_file_not_found(self):
        """Test loading when the database file does not exist."""
        # setUp ensures the file is deleted.
        # The __init__ of IngredientDatabase calls load_ingredients.
        # So, self.db should be empty.
        self.assertEqual(len(self.db.list_ingredients()), 0)
        # Check that no file was created if it wasn't found (it shouldn't be)
        self.assertFalse(os.path.exists(self.test_db_filepath))


    def test_load_ingredients_corrupted_json(self):
        """Test loading from a corrupted JSON file."""
        with open(self.test_db_filepath, 'w') as f:
            f.write("{'name': 'bad json',,}") # Invalid JSON format

        # Suppress print output during this test for cleaner test logs
        import sys
        from io import StringIO
        saved_stdout = sys.stdout
        try:
            sys.stdout = StringIO() # Redirect stdout
            db_corrupt = IngredientDatabase(filepath=self.test_db_filepath)
            self.assertEqual(len(db_corrupt.list_ingredients()), 0) # Should be empty
        finally:
            sys.stdout = saved_stdout # Restore stdout

    def test_load_ingredients_invalid_data_structure(self):
        """Test loading from a JSON file with valid JSON but invalid ingredient data structure."""
        # Data that Ingredient.from_dict would reject
        invalid_ingredient_data = {
            "item1": {"name": "Item1", "cal": 100} # "cal" instead of "calories"
        }
        with open(self.test_db_filepath, 'w') as f:
            json.dump(invalid_ingredient_data, f)

        # Suppress print output
        import sys
        from io import StringIO
        saved_stdout = sys.stdout
        try:
            sys.stdout = StringIO()
            db_invalid_structure = IngredientDatabase(filepath=self.test_db_filepath)
            # This should result in an empty database as Ingredient.from_dict will raise ValueError
            # which is caught in the load_ingredients method.
            self.assertEqual(len(db_invalid_structure.list_ingredients()), 0)
        finally:
            sys.stdout = saved_stdout

    def test_repr_method(self):
        """Test the __repr__ method of IngredientDatabase."""
        self.assertEqual(repr(self.db), f"<IngredientDatabase: 0 ingredients, file='{self.test_db_filepath}'>")
        self.db.add_ingredient(self.ing1)
        self.assertEqual(repr(self.db), f"<IngredientDatabase: 1 ingredients, file='{self.test_db_filepath}'>")


if __name__ == '__main__':
    unittest.main()
