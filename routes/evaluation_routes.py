from flask import Blueprint, render_template, request, jsonify
from database import db
from models import DegreeCourses, Evaluations, Instructors, Sections, Courses

evaluation_routes = Blueprint('evaluation_routes', __name__)

from flask import render_template
from models import Degrees, Instructors, Sections
from database import db

@evaluation_routes.route('/query_evaluation', methods=['GET'])
def query_form():
    
    degree_names = db.session.query(Degrees.name).distinct().all()
    degree_levels = db.session.query(Degrees.level).distinct().all()
    instructors = Instructors.query.all()  # Fetches all instructors
    semesters = ["Spring", "Summer", "Fall"]  # Static list of semesters

    return render_template('query_evaluation.html', degree_names=degree_names, degree_levels=degree_levels, instructors=instructors, semesters=semesters)



@evaluation_routes.route('/edit', methods=['POST'])
def edit_evaluation():
    data = request.json
    evaluation_id = data['evaluation_id']
    evaluation = Evaluations.query.get(evaluation_id)
    if evaluation:
        evaluation.update(data)  # Assuming an update method that applies changes to model
        db.session.commit()
        return jsonify({'message': 'Evaluation updated successfully'})
    return jsonify({'message': 'Evaluation not found'}), 404

@evaluation_routes.route('/delete', methods=['DELETE'])
def delete_evaluation():
    evaluation_id = request.args.get('evaluation_id')
    evaluation = Evaluations.query.get(evaluation_id)
    if evaluation:
        db.session.delete(evaluation)
        db.session.commit()
        return jsonify({'message': 'Evaluation deleted successfully'})
    return jsonify({'message': 'Evaluation not found'}), 404

@evaluation_routes.route('/list', methods=['GET'])
def list_evaluation():
    instructor_id = request.args.get('instructor_id')
    evaluations = Evaluations.query.join(Sections).filter(Sections.instructor_id == instructor_id).all()
    return jsonify([eval.serialize() for eval in evaluations])  # Serialize each evaluation

# Add more routes as needed based on the exact requirements
