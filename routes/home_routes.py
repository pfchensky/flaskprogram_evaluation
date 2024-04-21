from flask import render_template

def init_home_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html')
