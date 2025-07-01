# Nutrition Tracker

This project is a simple nutrition tracker with a web interface for managing ingredients and calculating meals calories and macros. It is mostly meant to help with meal prep and calculating calorie and macro values for a portion size. 

## Features

*   Add, view, and remove ingredients (name, calories, protein, carbs, fat per 100g).
*   Create meals and calculate their total and per portion nutritional value using ingredients from the database.
*   Add new ingredients to your database.

**Web Interface Features:**
*   **Landing Page (`/`):** Provides an overview of the application and navigation to other sections.
*   **Add Ingredients Page (`/add_ingredient`):** Allows users to easily add new ingredients to the shared database.
*   **Track Meal Page (`/track_meal`):** Enables users to:
    *   Select ingredients from the database.
    *   Specify the weight of each ingredient in a meal.
    *   Calculate and display the nutritional values (calories, protein, carbs, fat) for a 100g portion of the prepared meal.
    *   Calculate and display the total nutritional values for the entire meal.

## Project Structure

```
.
├── .gitignore                # Specifies intentionally untracked files that Git should ignore
├── app.py                    # Flask web application for the UI
├── main_cli.py               # Command-line interface application
├── nutrition_tracker/        # Core logic for nutrition tracking
│   ├── __init__.py           # Makes Python treat the directory as a package
│   ├── database.py           # Manages the ingredient database (JSON file)
│   ├── ingredient.py         # Defines the Ingredient class
│   └── meal.py               # Defines the Meal class
├── static/                   # Static files (CSS, JS, images) for the web interface
│   └── style.css             # CSS styles for the web pages
├── templates/                # HTML templates for the web interface
│   ├── add_ingredient.html   # Web page for adding new ingredients to the database
│   ├── index.html            # Landing page for the web application
│   ├── track_meal.html       # Web page for creating a meal and calculating its nutrition
├── tests/                    # Directory for automated tests
│   ├── __init__.py           # Makes Python treat the directory as a package
│   ├── test_database.py      # Tests for the database module
│   ├── test_ingredient.py    # Tests for the ingredient module
│   └── test_meal.py          # Tests for the meal module
├── ingredient_database.json  # Default database file (created on first run if not present)
├── requirements.txt          # Python dependencies for the project
├── start_app.bat             # Batch script to start the application on Windows
├── start_app.sh              # Shell script to start the application on macOS/Linux
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

### Simplified Launch (Recommended)

After completing the installation steps (including creating the virtual environment and installing dependencies), you can use the provided launch scripts for a streamlined experience:

*   **On Windows:**
    1.  Navigate to the project directory in File Explorer.
    2.  Double-click `start_app.bat`.
*   **On macOS and Linux:**
    1.  Open your terminal and navigate to the project directory.
    2.  Make the script executable (only needs to be done once):
        ```bash
        chmod +x start_app.sh
        ```
    3.  Run the script:
        ```bash
        ./start_app.sh
        ```

These scripts will typically:
1.  Activate the virtual environment.
2.  Start the Flask web server (for adding ingredients) in the background. You can access it at `http://127.0.0.1:5000/` . The web interface includes a "Shutdown Server" button on the top right which will stop the web server.
    *   Landing Page: `http://127.0.0.1:5000/`
    *   Add Ingredient Page: `http://127.0.0.1:5000/add_ingredient`
    *   Track Meal Page: `http://127.0.0.1:5000/track_meal`
3.  Start the main CLI application in the current terminal window.
4.  When you exit the CLI (e.g., by using the 'exit' option in the CLI or pressing Ctrl+C), the script will attempt to stop the Flask server (if it's still running and not shut down via the UI) and deactivate the virtual environment.

### Manual Launch (Alternative)

If you prefer to run the components separately:

#### Running the Web Interface

1.  **Ensure your virtual environment is activated (see Installation).**
2.  **Run the Flask application:**
    ```bash
    python app.py
    ```
3.  Open your web browser and navigate to the desired page:
    *   Landing Page: `http://127.0.0.1:5000/`
    *   Add Ingredient Page: `http://127.0.0.1:5000/add_ingredient`
    *   Track Meal Page: `http://127.0.0.1:5000/track_meal`

#### Running the Command-Line Interface (CLI)

1.  **Ensure your virtual environment is activated (see Installation).**
2.  **Run the CLI application (in a separate terminal if the web interface is running):**
    ```bash
    python main_cli.py
    ```
    The CLI will provide options to manage ingredients and create meals. The CLI and the web interface share the same `ingredient_database.json` file, so ingredients added via the web UI will be available in the CLI and vice-versa.

## Web Interface Details

The web interface provides a user-friendly way to interact with some of the application's features:

*   **Landing Page (`/` or `index.html`)**
    *   **Purpose:** Serves as the main entry point for the web application.
    *   **Functionality:** Provides a brief introduction to the Nutrition Tracker and links to the "Add Ingredient" and "Track Meal" pages.

*   **Add Ingredient Page (`/add_ingredient`)**
    *   **Purpose:** Allows users to add new ingredients to the central `ingredient_database.json`.
    *   **Functionality:** Users can input the ingredient's name, calories, protein, carbohydrates, and fat content (all per 100g). Upon submission, the ingredient is saved to the database. This page also features a "Shutdown Server" button to stop the Flask web server.

*   **Track Meal Page (`/track_meal`)**
    *   **Purpose:** Enables users to compose a meal from existing ingredients and view its nutritional breakdown.
    *   **Functionality:**
        *   Users can select multiple ingredients from a list populated from the `ingredient_database.json`.
        *   For each selected ingredient, users specify the amount (in grams) used in the meal.
        *   The application then calculates and displays:
            *   The nutritional information (calories, protein, carbs, fat) for a 100g portion of the *total meal mixture*.
            *   The total nutritional information for the *entire meal* based on the specified ingredient weights.

## Data Storage

Ingredient data is stored in a JSON file named `ingredient_database.json` in the root of the project directory. This file is shared between the CLI and the web interface.
