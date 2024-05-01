from flask import flash, render_template, request, redirect, url_for
from pymysql import IntegrityError
from models import LearningObjectives
from database import db

def init_learning_objective_routes(app):
    @app.route('/learning_objectives')
    def list_learning_objectives():
        objectives = LearningObjectives.query.all()
        return render_template('dataEntryPage/list_learning_objectives.html', objectives=objectives)

    @app.route('/add_learning_objective', methods=['GET', 'POST'])
    def add_learning_objective():
        if request.method == 'POST':
            # 获取表单中的字段
            learningObjective_id = request.form['learningObjective_id']
            title = request.form['title']
            description = request.form['description']
            # 使用手动输入的ID创建新的LearningObjective对象
            new_objective = LearningObjectives(learningObjective_id=learningObjective_id, title=title, description=description)
            db.session.add(new_objective)
            db.session.commit()
            return redirect(url_for('list_learning_objectives'))
        # 提供一个空的LearningObjective对象作为默认值
        objective = LearningObjectives()
        return render_template('dataEntryPage/add_learning_objective.html', objective=objective)

    @app.route('/delete_learning_objective/<int:learningObjective_id>', methods=['POST'])
    def delete_learning_objective(learningObjective_id):
        try:
            objective = LearningObjectives.query.get_or_404(learningObjective_id)
            db.session.delete(objective)
            db.session.commit()
            flash("Learning objective successfully deleted.", 'success')
        except IntegrityError:
            db.session.rollback()
            flash("Cannot delete learning objective because it is currently used in courses.", 'error')
        except Exception as e:
            db.session.rollback()
            flash("Failed to delete learning objective, it is currently used in courses.", 'error')

        return redirect(url_for('list_learning_objectives'))

    @app.route('/edit_learning_objective/<int:learningObjective_id>', methods=['GET', 'POST'])
    def edit_learning_objective(learningObjective_id):
        objective = LearningObjectives.query.get_or_404(learningObjective_id)
        if request.method == 'POST':
            objective.learningObjective_id = request.form['learningObjective_id']
            objective.title = request.form['title']
            objective.description = request.form['description']
            db.session.commit()
            return redirect(url_for('list_learning_objectives'))

        return render_template('dataEntryPage/edit_learning_objective.html', objective=objective)
