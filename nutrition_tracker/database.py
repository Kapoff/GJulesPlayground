import json
from .ingredient import Ingredient

class IngredientDatabase:
    """Manages a collection of Ingredient objects."""

    def __init__(self, filepath: str = "ingredients.json"):
        """
        Initializes the IngredientDatabase.

        Args:
            filepath: Path to the JSON file for storing ingredients.
                      Defaults to "ingredients.json".
        """
        self.filepath = filepath
        self._ingredients: dict[str, Ingredient] = {} # Store ingredients by name for quick lookup
        self.load_ingredients()

    def add_ingredient(self, ingredient: Ingredient) -> None:
        """
        Adds a new ingredient to the database.

        Args:
            ingredient: The Ingredient object to add.

        Raises:
            ValueError: If an ingredient with the same name already exists.
        """
        if not isinstance(ingredient, Ingredient):
            raise TypeError("Can only add Ingredient objects to the database.")
        if ingredient.name in self._ingredients:
            raise ValueError(f"Ingredient with name '{ingredient.name}' already exists.")
        self._ingredients[ingredient.name] = ingredient
        print(f"Ingredient '{ingredient.name}' added to database.") # For CLI feedback

    def get_ingredient(self, name: str) -> Ingredient | None:
        """
        Retrieves an ingredient by its name.

        Args:
            name: The name of the ingredient to retrieve.

        Returns:
            The Ingredient object if found, otherwise None.
        """
        return self._ingredients.get(name)

    def list_ingredients(self) -> list[str]:
        """Returns a list of names of all ingredients in the database."""
        return list(self._ingredients.keys())

    def remove_ingredient(self, name: str) -> bool:
        """
        Removes an ingredient from the database by its name.

        Args:
            name: The name of the ingredient to remove.

        Returns:
            True if the ingredient was removed, False if not found.
        """
        if name in self._ingredients:
            del self._ingredients[name]
            print(f"Ingredient '{name}' removed from database.") # For CLI feedback
            return True
        print(f"Ingredient '{name}' not found in database.") # For CLI feedback
        return False

    def save_ingredients(self) -> None:
        """Saves the current ingredient database to the JSON file."""
        try:
            data_to_save = {name: ing.to_dict() for name, ing in self._ingredients.items()}
            with open(self.filepath, 'w') as f:
                json.dump(data_to_save, f, indent=4)
            print(f"Ingredients saved to {self.filepath}")
        except IOError as e:
            print(f"Error saving ingredients to {self.filepath}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while saving ingredients: {e}")


    def load_ingredients(self) -> None:
        """Loads ingredients from the JSON file into the database."""
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                self._ingredients = {
                    name: Ingredient.from_dict(ing_data)
                    for name, ing_data in data.items()
                }
            print(f"Ingredients loaded from {self.filepath}")
        except FileNotFoundError:
            print(f"Database file {self.filepath} not found. Starting with an empty database.")
            self._ingredients = {} # Ensure it's empty if file doesn't exist
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {self.filepath}: {e}. Starting with an empty database.")
            self._ingredients = {} # Ensure it's empty if file is corrupt
        except Exception as e: # Catch other potential errors during loading (e.g., permission issues)
            print(f"An unexpected error occurred while loading ingredients from {self.filepath}: {e}. Starting with an empty database.")
            self._ingredients = {}


    def __repr__(self) -> str:
        return f"<IngredientDatabase: {len(self._ingredients)} ingredients, file='{self.filepath}'>"

# Example usage (optional, can be removed or moved to a main script)
if __name__ == '__main__':
    # Create a dummy ingredient for testing
    try:
        db = IngredientDatabase(filepath="test_ingredients.json") # Use a test file

        # Clean up test file if it exists from previous runs
        import os
        if os.path.exists("test_ingredients.json"):
            os.remove("test_ingredients.json")

        db.load_ingredients() # Should indicate file not found and start empty

        print("Initial ingredients:", db.list_ingredients())

        apple = Ingredient(name="Apple", calories=52, protein=0.3, carbs=14, fat=0.2)
        banana = Ingredient(name="Banana", calories=89, protein=1.1, carbs=23, fat=0.3)

        db.add_ingredient(apple)
        db.add_ingredient(banana)

        print("Ingredients after adding:", db.list_ingredients())

        retrieved_apple = db.get_ingredient("Apple")
        print("Retrieved Apple:", retrieved_apple)

        db.save_ingredients() # Save to test_ingredients.json

        # Create a new database instance to test loading
        db2 = IngredientDatabase(filepath="test_ingredients.json")
        print("Ingredients in new DB instance (loaded from file):", db2.list_ingredients())
        retrieved_banana_db2 = db2.get_ingredient("Banana")
        print("Retrieved Banana from db2:", retrieved_banana_db2)
        assert retrieved_banana_db2 is not None
        assert retrieved_banana_db2.calories == 89

        # Test removing an ingredient
        db2.remove_ingredient("Apple")
        print("Ingredients after removing Apple:", db2.list_ingredients())
        assert db2.get_ingredient("Apple") is None
        db2.save_ingredients() # Save changes

        # Test loading again to see if removal persisted
        db3 = IngredientDatabase(filepath="test_ingredients.json")
        print("Ingredients in db3 (after removal and reload):", db3.list_ingredients())
        assert db3.get_ingredient("Apple") is None
        assert db3.get_ingredient("Banana") is not None

        print("IngredientDatabase tests passed (basic).")

        # Clean up the test file
        if os.path.exists("test_ingredients.json"):
            os.remove("test_ingredients.json")
            print("Cleaned up test_ingredients.json")

    except Exception as e:
        print(f"An error occurred during IngredientDatabase example: {e}")
        # Clean up in case of error
        if os.path.exists("test_ingredients.json"):
            os.remove("test_ingredients.json")

    # Test error handling for adding duplicate
    try:
        db_test_duplicate = IngredientDatabase(filepath="dup_test.json")
        if os.path.exists("dup_test.json"): os.remove("dup_test.json") # Clean start
        ing1 = Ingredient("TestIng", 100,10,10,2)
        db_test_duplicate.add_ingredient(ing1)
        db_test_duplicate.add_ingredient(ing1) # Should raise ValueError
    except ValueError as e:
        print(f"Correctly caught error: {e}")
    finally:
        if os.path.exists("dup_test.json"): os.remove("dup_test.json")

    # Test error handling for bad ingredient type
    try:
        db_test_type = IngredientDatabase(filepath="type_test.json")
        if os.path.exists("type_test.json"): os.remove("type_test.json") # Clean start
        db_test_type.add_ingredient("not an ingredient") # Should raise TypeError
    except TypeError as e:
        print(f"Correctly caught error: {e}")
    finally:
        if os.path.exists("type_test.json"): os.remove("type_test.json")

    # Test loading corrupted JSON
    corrupt_file = "corrupt_ingredients.json"
    with open(corrupt_file, "w") as f:
        f.write("{'name': 'bad json',,}") # Invalid JSON
    db_corrupt = IngredientDatabase(filepath=corrupt_file) # load_ingredients is called in init
    assert len(db_corrupt.list_ingredients()) == 0 # Should start empty
    print("Corrupted JSON load test passed.")
    if os.path.exists(corrupt_file): os.remove(corrupt_file)

    # Test loading file with good data but not matching Ingredient structure
    invalid_data_file = "invalid_data_ingredients.json"
    with open(invalid_data_file, "w") as f:
        json.dump({"item1": {"name": "Item1", "cal": 100}}, f) # "cal" instead of "calories"
    db_invalid_data = IngredientDatabase(filepath=invalid_data_file)
    # This will currently raise a ValueError inside Ingredient.from_dict, which is caught by the general Exception in load_ingredients
    # and the database will be empty. This is acceptable for now.
    assert len(db_invalid_data.list_ingredients()) == 0
    print("Invalid data structure in JSON load test passed.")
    if os.path.exists(invalid_data_file): os.remove(invalid_data_file)

    print("All IngredientDatabase example usage/tests complete.")
