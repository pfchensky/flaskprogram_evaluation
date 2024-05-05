from flask import app, jsonify, render_template, request, redirect, url_for
from flask import flash
from models import CourseObjectives, Courses, DegreeCourses, Degrees, Instructors, LearningObjectives, Sections
from database import db

def init_course_routes(app):
    @app.route('/courses')
    def list_courses():

        courses = Courses.query.all()

        return render_template('dataEntryPage/list_courses.html', courses=courses)

    @app.route('/add_course', methods=['GET'])
    def add_course_form():

        return render_template('dataEntryPage/add_course.html')

    @app.route('/add_course', methods=['POST'])
    def add_course():

        course_number = request.form['course_number']
        name = request.form['name']

        new_course = Courses(course_id=course_number, name=name)

        db.session.add(new_course)
        db.session.commit()

        return redirect(url_for('list_courses'))

    @app.route('/delete_course/<course_id>', methods=['POST'])
    def delete_course(course_id):

        course = Courses.query.filter_by(course_id=course_id).first()

        if course:
            db.session.delete(course)
            db.session.commit()

        return redirect(url_for('list_courses'))

    @app.route('/edit_course/<course_id>', methods=['GET', 'POST'])
    def edit_course(course_id):
        course = Courses.query.get_or_404(course_id)
        if request.method == 'POST':

            course.course_id = request.form['course_number']
            course.name = request.form['name']
            db.session.commit()
            return redirect(url_for('list_courses'))

        return render_template('dataEntryPage/edit_course.html', course=course)
    
    @app.route('/course_details/<course_id>', methods=['GET'])
    def course_details(course_id):

        course = Courses.query.get_or_404(course_id)


        associated_degrees = DegreeCourses.query.filter_by(course_number=course_id).all()
        degrees = [Degrees.query.filter_by(name=degree.degree_name, level=degree.degree_level).first() for degree in associated_degrees]


        course_objectives = CourseObjectives.query.filter_by(course_id=course_id).all()
        objectives = [LearningObjectives.query.get(obj.learningObjective_id) for obj in course_objectives]

        return render_template('dataEntryPage/course_details.html', course=course, degrees=degrees, objectives=objectives)
        
    @app.route('/add_learning_objective_for_course/<course_id>', methods=['GET', 'POST'])
    def add_learning_objective_for_course(course_id):
        if request.method == 'POST':

            learningObjective_id = request.form.get('learningObjective_id')
            title = request.form.get('title')
            description = request.form.get('description')


            new_objective = LearningObjectives(learningObjective_id=learningObjective_id, title=title, description=description)

            try:

                db.session.add(new_objective)
                db.session.commit()


                course_objective = CourseObjectives(course_id=course_id, learningObjective_id=new_objective.learningObjective_id)


                db.session.add(course_objective)
                db.session.commit()

                flash("Learning objective added successfully for the course!", 'success')


                return redirect(url_for('course_details', course_id=course_id))
            except Exception as e:
                flash(f"An error occurred while adding learning objective for the course: {str(e)}", 'error')
                db.session.rollback()

        course = Courses.query.get_or_404(course_id)
        course_name = course.name
        return render_template('dataEntryPage/add_learning_objective_for_course.html', course=course)
    
    
    @app.route('/select_learning_objective_for_course/<course_id>', methods=['GET', 'POST'])
    def select_learning_objective_for_course(course_id):
        course = Courses.query.get_or_404(course_id)
        if request.method == 'POST':
            learningObjective_id = request.form.get('learningObjective_id')
            
            # Check if the objective is already linked to the course
            existing_objective = CourseObjectives.query.filter_by(course_id=course_id, learningObjective_id=learningObjective_id).first()

            if existing_objective:
                flash("This learning objective is already linked to the course.", 'error')
                return redirect(url_for('select_learning_objective_for_course', course_id=course_id))

            # Create the course-objective link if it does not exist
            new_course_objective = CourseObjectives(course_id=course_id, learningObjective_id=learningObjective_id)
            db.session.add(new_course_objective)
            db.session.commit()
            flash("Learning objective successfully linked to the course!", 'success')
            return redirect(url_for('course_details', course_id=course_id))

        # Exclude already linked objectives
        linked_objectives_ids = {obj.learningObjective_id for obj in CourseObjectives.query.filter_by(course_id=course_id).all()}
        available_objectives = LearningObjectives.query.filter(LearningObjectives.learningObjective_id.notin_(linked_objectives_ids)).all()

        return render_template('dataEntryPage/select_learning_objective_for_course.html', course=course, objectives=available_objectives)
    

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
    


