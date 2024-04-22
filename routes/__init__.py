# routes/__init__.py
from routes.degree_routes import init_degree_routes
from routes.instructor_routes import init_instructor_routes
from routes.learningObject_routes import init_learning_objective_routes
from routes.section_routes import init_section_routes
from .home_routes import init_home_routes
from .course_routes import init_course_routes

def init_all_routes(app):
    init_home_routes(app)
    init_course_routes(app)
    init_degree_routes(app)
    init_instructor_routes(app)
    init_section_routes(app)
    init_learning_objective_routes(app)
