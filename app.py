from flask import Flask
from database import config_app
from routes import init_all_routes

app = Flask(__name__)
config_app(app)  #set up database
init_all_routes(app)  # initialize url

if __name__ == '__main__':
    app.run(debug=True)
