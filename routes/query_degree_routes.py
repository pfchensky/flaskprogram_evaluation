from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import db, Degrees, Instructors, Sections, Evaluations, DegreeCourses, Courses, CourseObjectives, LearningObjectives
from database import db
query_routes = Blueprint('query_routes', __name__)


@query_routes.route('/query_degree', methods=['GET'])
def query_form():
    print("Route is being called")
    degree_names = db.session.query(Degrees.name).distinct().all()
    degree_levels = db.session.query(Degrees.level).distinct().all()
    return render_template('dataQueryPage/query_degree.html', degree_names=degree_names, degree_levels=degree_levels)

@query_routes.route('/degree_query', methods=['GET'])
def degree_query():

    degree_name = request.args.get('degree_name')
    degree_level = request.args.get('degree_level')
    return redirect(url_for('query_routes.list_degree_courses',
                            degree_name=degree_name,
                            degree_level=degree_level,))
from flask import jsonify

@query_routes.route('/list_degree_courses')
def list_degree_courses():
    # Assuming you want to filter by degree name and level
    degree_name = request.args.get('degree_name')
    degree_level = request.args.get('degree_level')

    if not degree_name or not degree_level:
        return jsonify({"error": "Missing degree name or level"}), 400

    # Perform the join based on the course_id and filter for the given degree
    query = db.session.query(Sections, Courses, DegreeCourses, CourseObjectives, LearningObjectives). \
        join(Courses, Sections.course_id == Courses.course_id). \
        join(DegreeCourses, Courses.course_id == DegreeCourses.course_number). \
        join(CourseObjectives, Courses.course_id == CourseObjectives.course_id). \
        join(LearningObjectives, LearningObjectives.learningObjective_id == CourseObjectives.learningObjective_id). \
        filter(DegreeCourses.degree_name == degree_name, DegreeCourses.degree_level == degree_level). \
        all()

    # Serialize the results into a format suitable for HTML rendering
    results = [
        {
            'section_id': section.section_id,
            'course_id': course.course_id,
            'course_name': course.name,
            'year': section.year,
            'semester': section.semester,
            'instructor_id': section.instructor_id,
            'enrollment_count': section.enrollment_count,
            'degree_name': degree_course.degree_name,
            'degree_level': degree_course.degree_level,
            #'course_number': degree_course.course_number,
            'is_core': degree_course.is_core,
            'objective_id': course_objective.learningObjective_id,
            'objective_title': learning_objective.title,
            'objective_description': learning_objective.description
        }
        for section, course, degree_course, course_objective, learning_objective in query
    ]

    #return jsonify(results)
    return render_template('dataQueryPage/list_degree_courses.html', results=results)
