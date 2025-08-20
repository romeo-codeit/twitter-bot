# A temporary script to initialize the database without using the Flask CLI,
# to work around environment issues with `os.getcwd()`.

import os
import sys

# Add the project root to the Python path to allow for correct package imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend import create_app
from backend.database import init_db

def run_init_db():
    """Creates a Flask app and initializes the database within its context."""
    print("Creating Flask app for database initialization...")
    # We provide a minimal config to ensure the app can be created.
    # The DATABASE path is set in the factory by default.
    app = create_app({
        'TESTING': True,
    })

    with app.app_context():
        print("Application context created. Initializing database...")
        init_db()
        print("Database initialization complete.")

if __name__ == '__main__':
    run_init_db()
