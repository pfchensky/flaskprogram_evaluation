
from routes.degree_routes import init_degree_routes
from routes.instructor_routes import init_instructor_routes
from routes.learningObject_routes import init_learning_objective_routes
from routes.section_routes import init_section_routes
from routes.query_degree_routes import query_degree_routes
from routes.query_course_routes import query_course_routes
from .home_routes import init_home_routes
from .course_routes import init_course_routes
from .evaluation_routes import evaluation_routes
from .query_instructor_routes import query_instructor_routes
from .query_section_routes import query_section_routes
from .query_section_percentage_routes import query_section_percentage_routes

def init_all_routes(app):
    # Data Entry
    init_home_routes(app)
    init_course_routes(app)
    init_degree_routes(app)
    init_instructor_routes(app)
    init_section_routes(app)
    init_learning_objective_routes(app)

    # Enter Evaluation
    app.register_blueprint(evaluation_routes, url_prefix='/evaluation')

    # Query
    app.register_blueprint(query_degree_routes, url_prefix='/query')
    app.register_blueprint(query_course_routes, url_prefix='/query')
    app.register_blueprint(query_instructor_routes, url_prefix='/query')
    app.register_blueprint(query_section_routes, url_prefix='/query')
    app.register_blueprint(query_section_percentage_routes, url_prefix='/query')
