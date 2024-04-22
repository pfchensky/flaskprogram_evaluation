# routes/__init__.py
from .home_routes import init_home_routes
from .course_routes import init_course_routes
from .evaluation_routes import evaluation_routes

def init_all_routes(app):
    init_home_routes(app)
    init_course_routes(app)
    app.register_blueprint(evaluation_routes, url_prefix='/evaluation')  # 可以添加 url_prefix 作为路由前缀
