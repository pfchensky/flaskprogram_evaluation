# database.py
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Create SQLAlchemy object
db = SQLAlchemy()

# Load environment variables from .env file
load_dotenv()

def config_app(app):
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')
    dbname = os.getenv('DB_NAME')
    
    # Configure the SQLAlchemy database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@localhost:3306/{dbname}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

