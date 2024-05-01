from flask import Flask
from database import db, config_app
from routes import init_all_routes


def create_app():
    # Create the Flask application instance
    app = Flask(__name__)
    
    # Set a secret key for session management and security.
    # Make sure to generate a secure key and keep it secret.
    app.secret_key = '123456'

    # Configure the application with the database and any other configurations.
    config_app(app)
    

    # Initialize all routes (URLs) that the application will respond to
    init_all_routes(app)

    return app

if __name__ == '__main__':
    # Only run if the script is executed directly (not imported)
    app = create_app()  # Create the Flask application
    app.run(debug=True)  # Start the application with debugging enabled
