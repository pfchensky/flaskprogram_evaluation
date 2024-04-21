from flask import Flask, render_template, request, redirect, url_for
from models import Courses
from database import db, config_app 

app = Flask(__name__)
config_app(app)  


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
