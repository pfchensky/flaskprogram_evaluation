from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import db, Degrees, Instructors, Sections, Evaluations, DegreeCourses
from database import db

evaluation_routes = Blueprint('evaluation_routes', __name__)

@evaluation_routes.route('/query_evaluation', methods=['GET'])
def query_form():
    print("Route is being called")
    degree_names = db.session.query(Degrees.name).distinct().all()
    degree_levels = db.session.query(Degrees.level).distinct().all()
    instructors = Instructors.query.all()
    semesters = ["Spring", "Summer", "Fall"]
    return render_template('evaluationPage/query_evaluation.html', degree_names=degree_names, degree_levels=degree_levels, instructors=instructors, semesters=semesters)

@evaluation_routes.route('/process_query', methods=['GET'])
def process_query():
    
    degree_name = request.args.get('degree_name')
    degree_level = request.args.get('degree_level')
    semester = request.args.get('semester')
    instructor_id = request.args.get('instructor_id')
    return redirect(url_for('evaluation_routes.list_evaluation',
                            degree_name=degree_name,
                            degree_level=degree_level,
                            semester=semester,
                            instructor_id=instructor_id))

@evaluation_routes.route('/list_evaluation', methods=['GET'])
def list_evaluation():
    degree_name = request.args.get('degree_name')
    degree_level = request.args.get('degree_level')
    semester = request.args.get('semester')
    instructor_id = request.args.get('instructor_id')

    evaluations = Evaluations.query \
        .join(Sections, Sections.section_id == Evaluations.section_id) \
        .join(DegreeCourses, DegreeCourses.course_number == Sections.course_id) \
        .filter(Sections.instructor_id == instructor_id,
                Sections.semester == semester,
                DegreeCourses.degree_name == degree_name,
                DegreeCourses.degree_level == degree_level) \
        .all()

    if not evaluations:
        print("No evaluations found")  # Debug statement

    return render_template('evaluationPage/list_evaluation.html', evaluations=evaluations)

@evaluation_routes.route('/edit', methods=['POST'])
def edit_evaluation():
    data = request.json
    evaluation_id = data['evaluation_id']
    evaluation = Evaluations.query.get(evaluation_id)
    if evaluation:
        # Manually updating each field:
        evaluation.perform_A = data.get('perform_A', evaluation.perform_A)
        evaluation.perform_B = data.get('perform_B', evaluation.perform_B)
        evaluation.perform_C = data.get('perform_C', evaluation.perform_C)
        evaluation.perform_F = data.get('perform_B', evaluation.perform_F)
        # Add other fields as necessary
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
