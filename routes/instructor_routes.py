from flask import render_template, request, redirect, url_for
from models import Instructors
from database import db

def init_instructor_routes(app):
    @app.route('/instructors')
    def list_instructors():
        # 从数据库获取所有教师信息
        instructors = Instructors.query.all()
        # 渲染显示教师的页面
        return render_template('dataEntryPage/list_instructors.html', instructors=instructors)

    @app.route('/add_instructor', methods=['GET'])
    def add_instructor_form():
        # 返回添加教师的表单页面
        return render_template('dataEntryPage/add_instructor.html')

    @app.route('/add_instructor', methods=['POST'])
    def add_instructor():
        # 从表单获取数据
        name = request.form['name']
        # 创建新教师对象
        new_instructor = Instructors(name=name)
        # 添加教师到数据库
        db.session.add(new_instructor)
        db.session.commit()
        # 重定向到教师列表页面
        return redirect(url_for('list_instructors'))

    @app.route('/delete_instructor/<int:instructor_id>', methods=['POST'])
    def delete_instructor(instructor_id):
        # 从数据库找到对应的教师
        instructor = Instructors.query.get_or_404(instructor_id)
        # 如果找到，删除该教师
        db.session.delete(instructor)
        db.session.commit()
        # 重定向到教师列表页面
        return redirect(url_for('list_instructors'))

    @app.route('/edit_instructor/<int:instructor_id>', methods=['GET', 'POST'])
    def edit_instructor(instructor_id):
        instructor = Instructors.query.get_or_404(instructor_id)
        if request.method == 'POST':
            # 更新教师信息
            instructor.name = request.form['name']
            db.session.commit()
            return redirect(url_for('list_instructors'))
        # 如果是GET请求，显示编辑表单
        return render_template('dataEntryPage/edit_instructor.html', instructor=instructor)