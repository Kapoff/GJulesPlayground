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

### Simplified Launch (Recommended)

After completing the installation steps (including creating the virtual environment and installing dependencies), you can use the provided launch scripts for a one-click experience:

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

These scripts will:
1.  Activate the virtual environment.
2.  Start the Flask web server (for adding ingredients) in the background. You can access it at `http://127.0.0.1:5000/` (or specifically the `/add_ingredient` page). The web interface includes a "Shutdown Server" button which will stop the web server.
3.  Start the main CLI application in the current terminal window.
4.  When you exit the CLI (e.g., by using the 'exit' option in the CLI or pressing Ctrl+C), the script will attempt to stop the Flask server (if it's still running) and deactivate the virtual environment. If you've used the "Shutdown Server" button in the web UI, the Flask server will already be stopped.

### Manual Launch (Alternative)

If you prefer to run the components separately:

#### Running the Web Interface (for adding ingredients)

1.  **Ensure your virtual environment is activated (see Installation).**
2.  **Run the Flask application:**
    ```bash
    python app.py
    ```
3.  Open your web browser and go to: `http://127.0.0.1:5000/`
    You can fill in the form to add new ingredients to the `ingredient_database.json` file.

#### Running the Command-Line Interface (CLI)

1.  **Ensure your virtual environment is activated (see Installation).**
2.  **Run the CLI application (in a separate terminal if the web interface is running):**
    ```bash
    python main_cli.py
    ```
    The CLI will provide options to manage ingredients and create meals. The CLI and the web interface share the same `ingredient_database.json` file, so ingredients added via the web UI will be available in the CLI and vice-versa.

## Data Storage

Ingredient data is stored in a JSON file named `ingredient_database.json` in the root of the project directory.
