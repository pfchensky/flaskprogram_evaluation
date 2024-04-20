from flask import Flask
from models import db


app = Flask(__name__)

# Format of SQLAlchemy database URI is:
# dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:xiaobencpf205@localhost:3306/program_evaluation'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # to suppress a warning message

# Initialize db with app
db.init_app(app)
# 在数据库中创建这些表
from models import Degrees, Courses, Instructors, Sections, LearningObjectives, Evaluations, DegreeCourses, CourseObjectives




@app.route('/')
def hello_world():  # put application's code here
    return 'hello group3!'



if __name__ == '__main__':
    with app.app_context():
        # This will create the database tables for our data models
        db.create_all()
    app.run()
