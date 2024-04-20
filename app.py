from flask import Flask,render_template,request,redirect,url_for
from models import db, Courses, Degrees, Instructors, Sections, LearningObjectives, Evaluations, DegreeCourses, CourseObjectives
import os
from dotenv import load_dotenv


app = Flask(__name__)

# 加载 .env 文件中的环境变量
load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
dbname = os.getenv('DB_NAME')

# Format of SQLAlchemy database URI is:
# dialect+driver://username:password@host:port/database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:xiaobencpf205@localhost:3306/program_evaluation'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@localhost:3306/{dbname}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # to suppress a warning message

# Initialize db with app
db.init_app(app)
# 在数据库中创建这些表
from models import Degrees, Courses, Instructors, Sections, LearningObjectives, Evaluations, DegreeCourses, CourseObjectives



#home page with links
@app.route('/')
def home():  # put application's code here
    return render_template('home.html')
#list courses
@app.route('/courses')
def list_courses():
    courses = Courses.query.all()
    return render_template('list_courses.html',courses=courses)

#add course form display
@app.route('/add_course',methods=['GET'])
def add_course_form():
    return render_template('add_course.html')

@app.route('/add_course',methods=['POST'])
def add_course():
    course_number = request.form['course_number']
    name = request.form['name']
    new_course = Courses(course_id=course_number, name=name)
    db.session.add(new_course)
    db.session.commit()
    return redirect(url_for('list_courses'))
# Delete course
@app.route('/delete_course/<course_id>', methods=['POST'])
def delete_course(course_id):
    course = Courses.query.filter_by(course_id=course_id).first()
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('list_courses'))
@app.route('/edit_course/<course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    course = Courses.query.get_or_404(course_id)
    if request.method == 'POST':
        course.course_id = request.form['course_number']
        course.name = request.form['name']
        db.session.commit()
        return redirect(url_for('list_courses'))
    return render_template('edit_course.html', course=course)

if __name__ == '__main__':
    with app.app_context():
        # This will create the database tables for our data models
        db.create_all()
    app.run(debug=True)
