from flask import app, jsonify, render_template, request, redirect, url_for
from flask import flash
from models import CourseObjectives, Courses, DegreeCourses, Degrees, Instructors, LearningObjectives, Sections
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
        # 获取课程信息
        course = Courses.query.get_or_404(course_id)

        # 查找与此课程关联的学位
        associated_degrees = DegreeCourses.query.filter_by(course_number=course_id).all()
        degrees = [Degrees.query.filter_by(name=degree.degree_name, level=degree.degree_level).first() for degree in associated_degrees]

        # 获取与此课程关联的所有学习目标
        course_objectives = CourseObjectives.query.filter_by(course_id=course_id).all()
        objectives = [LearningObjectives.query.get(obj.learningObjective_id) for obj in course_objectives]

        return render_template('dataEntryPage/course_details.html', course=course, degrees=degrees, objectives=objectives)
        
    @app.route('/add_learning_objective_for_course/<course_id>', methods=['GET', 'POST'])
    def add_learning_objective_for_course(course_id):
        if request.method == 'POST':
            # 获取表单数据
            learningObjective_id = request.form.get('learningObjective_id')
            title = request.form.get('title')
            description = request.form.get('description')

            # 创建学习目标对象，手动设置ID
            new_objective = LearningObjectives(learningObjective_id=learningObjective_id, title=title, description=description)

            try:
                # 添加学习目标到数据库
                db.session.add(new_objective)
                db.session.commit()

                # 创建课程目标关联对象
                course_objective = CourseObjectives(course_id=course_id, learningObjective_id=new_objective.learningObjective_id)

                # 添加课程目标关联到数据库
                db.session.add(course_objective)
                db.session.commit()

                flash("Learning objective added successfully for the course!", 'success')

                # 成功添加后重定向到课程详情页面
                return redirect(url_for('course_details', course_id=course_id))
            except Exception as e:
                flash(f"An error occurred while adding learning objective for the course: {str(e)}", 'error')
                db.session.rollback()

        course = Courses.query.get_or_404(course_id)
        course_name = course.name
        return render_template('dataEntryPage/add_learning_objective_for_course.html', course=course)
    

    @app.route('/course_sections/<string:course_id>', methods=['GET'])
    def course_sections(course_id):
        try:
            # Properly performing a join before filtering
            sections = db.session.query(
                Sections.section_id,
                Sections.course_id,
                Sections.year,
                Sections.semester,
                Sections.instructor_id,
                Sections.enrollment_count,
                Courses.name.label('course_name'),  
                Instructors.name.label('instructor_name')
            ).join(Courses, Sections.course_id == Courses.course_id)\
            .join(Instructors, Sections.instructor_id == Instructors.instructor_id)\
            .filter(Sections.course_id == course_id)\
            .all()

            sections_data = [{
                'section_id': section.section_id,
                'course_id': section.course_id,
                'year': section.year,
                'semester': section.semester.name if hasattr(section.semester, 'name') else section.semester,  # Handling enum if present
                'instructor_id': section.instructor_id,
                'enrollment_count': section.enrollment_count,
                'course_name': section.course_name,  # Adding course_name to the output
                'instrutor_name': section.instructor_name
                
            } for section in sections]

            return jsonify(sections_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

