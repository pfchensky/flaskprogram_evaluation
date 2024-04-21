# routes/__init__.py
from .home_routes import init_home_routes
from .course_routes import init_course_routes

def init_all_routes(app):
    init_home_routes(app)
    init_course_routes(app)
