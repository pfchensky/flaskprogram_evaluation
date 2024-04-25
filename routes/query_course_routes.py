from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import db, Degrees, Instructors, Sections, Evaluations, DegreeCourses, Courses, CourseObjectives, LearningObjectives
from database import db

query_course_routes = Blueprint('query_course_routes', __name__)

@query_course_routes.route('/query_course', methods=['GET'])
def query_form():
    print("Route is being called")
    courses = db.session.query(Courses.course_id, Courses.name).distinct().all()
    # Query distinct years and semesters from Sections
    years = db.session.query(Sections.year).distinct().order_by(Sections.year).all()
    semesters = db.session.query(Sections.semester).distinct().all()
    return render_template('dataQueryPage/query_course.html', courses=courses, years=years, semesters=semesters)


@query_course_routes.route('/course_query', methods=['GET'],)
def course_query():

    course_id = request.args.get('course_id')
    semester = request.args.get('semester')
    year = request.args.get('year')
    return redirect(url_for('query_course_routes.list_course_sections',
                            course_id=course_id,
                            semester=semester,
                            year=year,))


@query_course_routes.route('/list_course_sections')
def list_course_sections():
    # Assuming you want to filter by degree name and level
    course_id = request.args.get('course_id')
    semester = request.args.get('semester')
    year = request.args.get('year')

    # Check if all required parameters are provided
    if not course_id or not semester or not year:
        return jsonify({"error": "Missing course_id, semester, or year"}), 400

    # Convert year to integer for the database query
    try:
        year = int(year)
    except ValueError:
        return jsonify({"error": "Invalid year format"}), 400

    # Perform the query on the Sections table only
    sections = db.session.query(Sections, Courses.name).join(
        Courses, Sections.course_id == Courses.course_id
    ).filter(
        Sections.course_id == course_id,
        Sections.semester == semester,
        Sections.year == year
    ).all()

    # Serialize the results into a format suitable for HTML rendering
    results = [
        {
            'section_id': section.section_id,
            'course_id': section.course_id,
            'course_name': name,  # Here 'name' is the course name from the Courses table
            'year': section.year,
            'semester': section.semester,
            'instructor_id': section.instructor_id,
            'enrollment_count': section.enrollment_count
        }
        for section, name in sections  # Unpacking each result tuple
    ]

    # Return the results as JSON or pass them to the template
    #return jsonify(results)
    return render_template('dataQueryPage/list_course_sections.html', results=results)
