# database.py
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# 创建 SQLAlchemy 对象
db = SQLAlchemy()

# 加载 .env 文件中的环境变量
load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
dbname = os.getenv('DB_NAME')

def config_app(app):
    # Format of SQLAlchemy database URI is:
    # dialect+driver://username:password@host:port/database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@localhost:3306/{dbname}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # to suppress a warning message
    db.init_app(app)

    with app.app_context():
        # This will create the database tables for our data models, if they don't already exist
        db.create_all()
