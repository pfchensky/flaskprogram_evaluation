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

            learningObjective_id = request.form.get('learningObjective_id', type=int)
            title = request.form['title']
            description = request.form['description']

            if learningObjective_id is None:
                flash('Invalid Learning Objective ID. Please enter a numeric ID.', 'error')
                return render_template('dataEntryPage/add_learning_objective.html', objective=request.form)


            existing_objective = LearningObjectives.query.get(learningObjective_id)
            if existing_objective:
                flash('A learning objective with this ID already exists.', 'error')
                return render_template('dataEntryPage/add_learning_objective.html', objective=request.form)

            try:

                new_objective = LearningObjectives(
                    learningObjective_id=learningObjective_id, title=title, description=description)
                db.session.add(new_objective)
                db.session.commit()
                flash('Learning objective added successfully.', 'success')
                return redirect(url_for('list_learning_objectives'))
            except SQLAlchemyError as e: # type: ignore
                db.session.rollback()
                flash(f'An error occurred while adding the learning objective: {str(e)}', 'error')


        return render_template('dataEntryPage/add_learning_objective.html', objective=LearningObjectives())

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
