from flask import render_template, request, redirect, url_for
from models import CourseObjectives, Courses, DegreeCourses, Degrees, LearningObjectives
from database import db

def init_course_routes(app):
    @app.route('/courses')
    def list_courses():
        # 从数据库获取所有课程
        courses = Courses.query.all()
        # 渲染显示课程的页面
        return render_template('dataEntryPage/list_courses.html', courses=courses)

    @app.route('/add_course', methods=['GET'])
    def add_course_form():
        # 返回添加课程的表单页面
        return render_template('dataEntryPage/add_course.html')

    @app.route('/add_course', methods=['POST'])
    def add_course():
        # 从表单获取数据
        course_number = request.form['course_number']
        name = request.form['name']
        # 创建新课程对象
        new_course = Courses(course_id=course_number, name=name)
        # 添加课程到数据库
        db.session.add(new_course)
        db.session.commit()
        # 重定向到课程列表页面
        return redirect(url_for('list_courses'))

    @app.route('/delete_course/<course_id>', methods=['POST'])
    def delete_course(course_id):
        # 从数据库找到对应的课程
        course = Courses.query.filter_by(course_id=course_id).first()
        # 如果找到，删除该课程
        if course:
            db.session.delete(course)
            db.session.commit()
        # 重定向到课程列表页面
        return redirect(url_for('list_courses'))

    @app.route('/edit_course/<course_id>', methods=['GET', 'POST'])
    def edit_course(course_id):
        course = Courses.query.get_or_404(course_id)
        if request.method == 'POST':
            # 更新课程信息
            course.course_id = request.form['course_number']
            course.name = request.form['name']
            db.session.commit()
            return redirect(url_for('list_courses'))
        # 如果是GET请求，显示编辑表单
        return render_template('dataEntryPage/edit_course.html', course=course)
    
    @app.route('/course_details/<course_id>', methods=['GET'])
    def course_details(course_id):
        # Get the course by course_id
        course = Courses.query.get_or_404(course_id)
        # Find associated degrees with this course
        associated_degrees = DegreeCourses.query.filter_by(course_number=course_id).all()
        degrees = [Degrees.query.filter_by(name=degree.degree_name, level=degree.degree_level).first() for degree in associated_degrees]
        # Get all the learning objectives associated with this course
        course_objectives = CourseObjectives.query.filter_by(course_id=course_id).all()
        objectives = [LearningObjectives.query.get(obj.learningObjective_id) for obj in course_objectives]

        return render_template('dataEntryPage/course_details.html', course=course, degrees=degrees, 
objectives=objectives)

