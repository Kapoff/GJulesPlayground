class Ingredient:
    """Represents an ingredient and its nutritional information per 100g."""

    def __init__(self, name: str, calories: float, protein: float, carbs: float, fat: float):
        """
        Initializes an Ingredient object.

        Args:
            name: The name of the ingredient.
            calories: Calories per 100g.
            protein: Protein in grams per 100g.
            carbs: Carbohydrates in grams per 100g.
            fat: Fat in grams per 100g.
        """
        if not isinstance(name, str) or not name:
            raise ValueError("Ingredient name must be a non-empty string.")
        if not isinstance(calories, (int, float)) or calories < 0:
            raise ValueError("Calories must be a non-negative number.")
        if not isinstance(protein, (int, float)) or protein < 0:
            raise ValueError("Protein must be a non-negative number.")
        if not isinstance(carbs, (int, float)) or carbs < 0:
            raise ValueError("Carbs must be a non-negative number.")
        if not isinstance(fat, (int, float)) or fat < 0:
            raise ValueError("Fat must be a non-negative number.")

        # Ensure that macros don't exceed the weight (assuming 1g protein/carb = 4 cal, 1g fat = 9 cal)
        # This is a rough validation and might need adjustment based on specific needs
        # Convert all to float before calculation to avoid potential type issues if int was passed
        float_protein = float(protein)
        float_carbs = float(carbs)
        float_fat = float(fat)
        float_calories = float(calories)

        calculated_calories_from_macros = (float_protein * 4) + (float_carbs * 4) + (float_fat * 9)
        # Allow some leeway for rounding differences, e.g., 10 calories or 10% of stated calories
        # Using a percentage might be better for very low/high calorie items.
        # For now, a fixed leeway.
        # We only care if calculated calories from macros SIGNIFICANTLY EXCEED stated calories.
        # Stated calories can be higher due to fiber, sugar alcohols, etc. that are part of carbs but have fewer calories,
        # or simply due to how official calorie counts are determined (bomb calorimeter vs. Atwater factors).
        # However, if protein + carbs + fat calories are much higher, it's suspicious.
        if calculated_calories_from_macros > float_calories + 10: # Allow 10 calorie leeway
             # print(f"Warning for ingredient {name}: Calculated calories from macros ({calculated_calories_from_macros}) is significantly higher than stated calories ({float_calories}).")
             # Not raising an error, but this could be logged or flagged in a more complex system.
             pass

        self.name = name
        self.calories = float_calories
        self.protein = float(protein)
        self.carbs = float(carbs)
        self.fat = float(fat)

    def __repr__(self) -> str:
        return (f"Ingredient(name='{self.name}', calories={self.calories}, "
                f"protein={self.protein}, carbs={self.carbs}, fat={self.fat})")

    def get_nutrition_for_weight(self, weight_grams: float) -> tuple[float, float, float, float]:
        """
        Calculates the nutritional values for a given weight of the ingredient.

        Args:
            weight_grams: The weight of the ingredient in grams.

        Returns:
            A tuple containing (calories, protein, carbs, fat) for the given weight.
        """
        if not isinstance(weight_grams, (int, float)) or weight_grams < 0:
            raise ValueError("Weight must be a non-negative number.")

        factor = weight_grams / 100.0
        return (
            self.calories * factor,
            self.protein * factor,
            self.carbs * factor,
            self.fat * factor
        )

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the ingredient."""
        return {
            "name": self.name,
            "calories": self.calories,
            "protein": self.protein,
            "carbs": self.carbs,
            "fat": self.fat,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Ingredient':
        """Creates an Ingredient object from a dictionary."""
        if not all(key in data for key in ["name", "calories", "protein", "carbs", "fat"]):
            raise ValueError("Dictionary is missing required keys for Ingredient.")
        return cls(
            name=data["name"],
            calories=data["calories"],
            protein=data["protein"],
            carbs=data["carbs"],
            fat=data["fat"],
        )
