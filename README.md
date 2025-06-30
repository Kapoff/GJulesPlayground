# Nutrition Tracker

This project is a simple nutrition tracker with a command-line interface (CLI) and a web interface for managing ingredients.

## Features

*   Add, view, and remove ingredients (name, calories, protein, carbs, fat per 100g) via CLI.
*   Create meals and calculate their total nutritional value using ingredients from the database via CLI.
*   Add new ingredients via a web interface.

## Project Structure

```
.
├── app.py                    # Flask web application
├── main_cli.py               # Command-line interface application
├── nutrition_tracker/        # Core logic for nutrition tracking
│   ├── __init__.py
│   ├── database.py           # Manages the ingredient database (JSON file)
│   ├── ingredient.py         # Defines the Ingredient class
│   └── meal.py               # Defines the Meal class
├── static/                   # Static files for the web interface
│   └── style.css             # CSS for the web page
├── templates/                # HTML templates for the web interface
│   └── add_ingredient.html   # HTML page for adding ingredients
├── ingredient_database.json  # Default database file (created on first run if not present)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Setup and Running

### Prerequisites

*   Python 3.7+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository (if applicable) or download the files.**

2.  **Navigate to the project directory:**
    ```bash
    cd path/to/your/project-folder
    ```

3.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    *   On Windows:
        ```bash
        venv\Scripts\activate
        ```
    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Web Interface (for adding ingredients)

1.  **Ensure your virtual environment is activated.**
2.  **Run the Flask application:**
    ```bash
    python app.py
    ```
3.  Open your web browser and go to: `http://127.0.0.1:5000/`

    You should see the "Add New Ingredient" page. You can fill in the form to add new ingredients to the `ingredient_database.json` file.

### Running the Command-Line Interface (CLI)

1.  **Ensure your virtual environment is activated.**
2.  **Run the CLI application:**
    ```bash
    python main_cli.py
    ```
    The CLI will provide options to manage ingredients and create meals. The CLI and the web interface share the same `ingredient_database.json` file, so ingredients added via the web UI will be available in the CLI and vice-versa.

## Data Storage

Ingredient data is stored in a JSON file named `ingredient_database.json` in the root of the project directory.
