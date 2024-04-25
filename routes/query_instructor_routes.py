from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from database import db  # Ensure that 'db' is imported correctly
from models import Instructors, Sections  # Ensure that 'Instructors' and 'Sections' are imported correctly

query_instructor_routes = Blueprint('query_instructor_routes', __name__)

@query_instructor_routes.route('/query_instructor', methods=['GET'])
def query_form():
    instructor_names = db.session.query(Instructors.name).distinct().all()
    instructor_names = [name[0] for name in instructor_names]  
    return render_template('dataQueryPage/query_instructor.html', instructor_names=instructor_names)

@query_instructor_routes.route('/instructor_query', methods=['GET'])
def instructor_query():
    instructor_name = request.args.get('instructor_name')
    semester = request.args.get('semester')
    return redirect(url_for('query_instructor_routes.list_instructor_sections',
                            instructor_name=instructor_name, semester=semester))

@query_instructor_routes.route('/list_instructor_sections')
def list_instructor_sections():
    instructor_name = request.args.get('instructor_name')
    semester = request.args.get('semester')

    # Check if all required parameters are provided
    if not instructor_name or not semester:
        return jsonify({"error": "Missing instructor_name or semester"}), 400

    # Perform the query on the Sections table joined with Instructors
    sections = db.session.query(Sections).join(
    Instructors, Instructors.instructor_id == Sections.instructor_id
).filter(
    Instructors.name == instructor_name,
    Sections.semester == semester
).all()


    results = [
                {
                'section_id': section.section_id, 
                'course_id': section.course_id, 
                'year': section.year, 
                'semester': section.semester, 
                'enrollment_count': section.enrollment_count
                }for section in sections]
    # return jsonify(results)
    return render_template('dataQueryPage/list_instructor_sections.html', results=results, instructor_name=instructor_name, semester=semester)
