from flask import flash, jsonify, render_template, request, redirect, url_for
from models import Courses, Instructors, Sections
from database import db

def init_instructor_routes(app):
    @app.route('/instructors')
    def list_instructors():

        instructors = Instructors.query.all()

        return render_template('dataEntryPage/list_instructors.html', instructors=instructors)

    @app.route('/add_instructor', methods=['GET'])
    def add_instructor_form():

        return render_template('dataEntryPage/add_instructor.html')

    @app.route('/add_instructor', methods=['POST'])
    def add_instructor():

        instructor_id = request.form.get('instructorId', type=int)  # Ensure this is retrieving as int and matches the form input name
        name = request.form['name']
        
        # Optional: Check if an instructor with the given ID already exists
        existing_instructor = Instructors.query.get(instructor_id)
        if existing_instructor:
            # Handle the case where instructor already exists
            flash('An instructor with this ID already exists.', 'error')
            return redirect(url_for('add_instructor_form'))

        # Create new instructor object with ID
        new_instructor = Instructors(instructor_id=instructor_id, name=name)  # Use instructor_id, which is the correct model field
        db.session.add(new_instructor)
        db.session.commit()
        flash('Instructor added successfully!', 'success')
        # Redirect to the instructor list page
        return redirect(url_for('list_instructors'))

    @app.route('/delete_instructor/<int:instructor_id>', methods=['POST'])
    def delete_instructor(instructor_id):

        instructor = Instructors.query.get_or_404(instructor_id)

        db.session.delete(instructor)
        db.session.commit()

        return redirect(url_for('list_instructors'))

    @app.route('/edit_instructor/<int:instructor_id>', methods=['GET', 'POST'])
    def edit_instructor(instructor_id):
        instructor = Instructors.query.get_or_404(instructor_id)
        if request.method == 'POST':

            instructor.name = request.form['name']
            db.session.commit()
            return redirect(url_for('list_instructors'))

        return render_template('dataEntryPage/edit_instructor.html', instructor=instructor)

    @app.route('/sections_by_instructor', methods=['GET'])
    def sections_by_instructor():
        instructor_id = request.args.get('instructorId', type=int)
        if not instructor_id:
            return "No instructor ID provided", 400

        try:
            sections = db.session.query(
                Sections.section_id,
                Sections.year,
                Sections.semester,
                Sections.enrollment_count,
                Courses.course_id,
                Courses.name.label('course_name'),
                Instructors.name.label('instructor_name')
            ).join(Courses, Sections.course_id == Courses.course_id)\
            .join(Instructors, Sections.instructor_id == Instructors.instructor_id)\
            .filter(Sections.instructor_id == instructor_id)\
            .all()

            if not sections:
                return render_template('no_sections.html'), 404

            return render_template('sections_by_instructor.html', sections=sections)
        except Exception as e:
            return render_template('error.html', error=str(e)), 500
