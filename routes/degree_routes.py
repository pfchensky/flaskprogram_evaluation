from flask import flash
from flask import render_template, request, redirect, url_for
from pymysql import IntegrityError
from models import Courses, DegreeCourses, Degrees
from database import db

def init_degree_routes(app):
    @app.route('/degrees')
    def list_degrees():
        # 从数据库获取所有学位
        degrees = Degrees.query.all()
        # 渲染显示学位的页面
        return render_template('dataEntryPage/list_degrees.html', degrees=degrees)

    @app.route('/add_degree', methods=['GET'])
    def add_degree_form():
        # 返回添加学位的表单页面
        return render_template('dataEntryPage/add_degree.html')

    @app.route('/add_degree', methods=['POST'])
    def add_degree():
        # 从表单获取数据
        name = request.form['name']
        level = request.form['level']
        # 创建新学位对象
        new_degree = Degrees(name=name, level=level)
        # 添加学位到数据库
        db.session.add(new_degree)
        db.session.commit()
        # 重定向到学位列表页面
        return redirect(url_for('list_degrees'))

    @app.route('/delete_degree/<name>/<level>', methods=['POST'])
    def delete_degree(name, level):
        # 从数据库找到对应的学位
        degree = Degrees.query.filter_by(name=name, level=level).first()
        # 如果找到，删除该学位
        if degree:
            db.session.delete(degree)
            db.session.commit()
        # 重定向到学位列表页面
        return redirect(url_for('list_degrees'))

    @app.route('/edit_degree/<name>/<level>', methods=['GET', 'POST'])
    def edit_degree(name, level):
        degree = Degrees.query.filter_by(name=name, level=level).first_or_404()
        if request.method == 'POST':
            # 更新学位信息
            degree.name = request.form['name']
            degree.level = request.form['level']
            db.session.commit()
            return redirect(url_for('list_degrees'))
        # 如果是GET请求，显示编辑表单
        return render_template('dataEntryPage/edit_degree.html', degree=degree)
    
    @app.route('/view_degree_details/<string:name>/<string:level>')
    def view_degree_details(name, level):
        degree = Degrees.query.filter_by(name=name, level=level).first_or_404()
        # Ensure to join DegreeCourses with Courses to fetch course details
        degree_courses = (DegreeCourses.query
                        .join(Courses, DegreeCourses.course_number == Courses.course_id)
                        .filter(DegreeCourses.degree_name == name, DegreeCourses.degree_level == level)
                        .add_columns(Courses.course_id, Courses.name, DegreeCourses.is_core)
                        .all())
        return render_template('dataEntryPage/degree_details.html', degree=degree, degree_courses=degree_courses)
    
   
    @app.route('/add_course_to_degree/<string:name>/<string:level>', methods=['GET', 'POST'])
    def add_course_to_degree(name, level):
        if request.method == 'POST':
            course_number = request.form['course_number']
            is_core = request.form['is_core'] == 'true'

            # Instantiate and save the new degree course
            new_degree_course = DegreeCourses(degree_name=name, degree_level=level, course_number=course_number, is_core=is_core)
            db.session.add(new_degree_course)
            db.session.commit()
            flash('Course added successfully!', 'success')
            return redirect(url_for('view_degree_details', name=name, level=level))
        
        # Handle GET request
        # 获取所有课程
        all_courses = Courses.query.all()
        return render_template('dataEntryPage/add_course_to_degree.html', name=name, level=level, courses=all_courses)