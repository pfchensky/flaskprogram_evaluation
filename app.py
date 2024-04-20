from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Format of SQLAlchemy database URI is:
# dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:xiaobencpf205@localhost:3306/program_evaluation'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # to suppress a warning message

db = SQLAlchemy(app)

# 定义 Degrees 模型
class Degrees(db.Model):
    __tablename__ = 'Degrees'
    name = db.Column(db.String(255), primary_key=True)
    level = db.Column(db.String(255), primary_key=True)

# 定义 Courses 模型
class Courses(db.Model):
    __tablename__ = 'Courses'
    course_id = db.Column(db.String(7), primary_key=True)
    name = db.Column(db.String(255), unique=True)

# 定义 Instructors 模型
class Instructors(db.Model):
    __tablename__ = 'Instructors'
    instructor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

# 定义 Sections 模型
class Sections(db.Model):
    __tablename__ = 'Sections'
    section_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(7), db.ForeignKey('Courses.course_id'))
    year = db.Column(db.Integer)
    semester = db.Column(db.Enum('Spring', 'Summer', 'Fall'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('Instructors.instructor_id'))
    enrollment_count = db.Column(db.Integer)

# 定义 LearningObjectives 模型
class LearningObjectives(db.Model):
    __tablename__ = 'LearningObjectives'
    learningObjective_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    description = db.Column(db.Text)

# 定义 Evaluations 模型
class Evaluations(db.Model):
    __tablename__ = 'Evaluations'
    evaluation_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('Sections.section_id'))
    learningObjective_id = db.Column(db.Integer, db.ForeignKey('LearningObjectives.learningObjective_id'))
    degree_name = db.Column(db.String(255))
    degree_level = db.Column(db.String(255))
    assess_method = db.Column(db.Enum('Homework', 'Project', 'Quiz', 'Oral Presentation', 'Report', 'Mid-term', 'Final Exam', 'others'))
    perform_A = db.Column(db.Integer)
    perform_B = db.Column(db.Integer)
    perform_C = db.Column(db.Integer)
    perform_F = db.Column(db.Integer)
    improve_sugs = db.Column(db.Text)

# 定义 DegreeCourses 模型
class DegreeCourses(db.Model):
    __tablename__ = 'DegreeCourses'
    degree_name = db.Column(db.String(255), primary_key=True)
    degree_level = db.Column(db.String(255), primary_key=True)
    course_number = db.Column(db.String(7), db.ForeignKey('Courses.course_id'), primary_key=True)
    is_core = db.Column(db.Boolean)

# 定义 CourseObjectives 模型
class CourseObjectives(db.Model):
    __tablename__ = 'CourseObjectives'
    degree_name = db.Column(db.String(255), primary_key=True)
    degree_level = db.Column(db.String(255), primary_key=True)
    learningObjective_id = db.Column(db.Integer, db.ForeignKey('LearningObjectives.learningObjective_id'), primary_key=True)

# 在数据库中创建这些表
with app.app_context():
    # This will create the database tables for our data models
    db.create_all()




@app.route('/')
def hello_world():  # put application's code here
    return '徐昊!'


if __name__ == '__main__':
    app.run()
