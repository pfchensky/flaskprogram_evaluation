from flask import render_template, request, redirect, url_for
from models import LearningObjectives
from database import db

def init_learning_objective_routes(app):
    @app.route('/learning_objectives')
    def list_learning_objectives():
        objectives = LearningObjectives.query.all()
        return render_template('list_learning_objectives.html', objectives=objectives)

    @app.route('/add_learning_objective', methods=['GET', 'POST'])
    def add_learning_objective():
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            new_objective = LearningObjectives(title=title, description=description)
            db.session.add(new_objective)
            db.session.commit()
            return redirect(url_for('list_learning_objectives'))

        return render_template('add_learning_objective.html')

    @app.route('/delete_learning_objective/<int:learningObjective_id>', methods=['POST'])
    def delete_learning_objective(learningObjective_id):
        objective = LearningObjectives.query.get_or_404(learningObjective_id)
        db.session.delete(objective)
        db.session.commit()
        return redirect(url_for('list_learning_objectives'))

    @app.route('/edit_learning_objective/<int:learningObjective_id>', methods=['GET', 'POST'])
    def edit_learning_objective(learningObjective_id):
        objective = LearningObjectives.query.get_or_404(learningObjective_id)
        if request.method == 'POST':
            objective.title = request.form['title']
            objective.description = request.form['description']
            db.session.commit()
            return redirect(url_for('list_learning_objectives'))

        return render_template('edit_learning_objective.html', objective=objective)
