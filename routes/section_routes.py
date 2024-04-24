from flask import render_template, request, redirect, url_for
from models import db, Sections, Courses, Instructors

def init_section_routes(app):
    @app.route('/sections')
    def list_sections():
        sections = Sections.query.all()
        return render_template('dataEntryPage/list_sections.html', sections=sections)

    @app.route('/add_section', methods=['GET', 'POST'])
    def add_section():
        if request.method == 'POST':
            course_id = request.form['course_id']
            year = request.form['year']
            semester = request.form['semester']
            instructor_id = request.form['instructor_id']
            enrollment_count = request.form['enrollment_count']

            new_section = Sections(
                course_id=course_id,
                year=year,
                semester=semester,
                instructor_id=instructor_id,
                enrollment_count=enrollment_count
            )
            db.session.add(new_section)
            db.session.commit()
            return redirect(url_for('list_sections'))

        courses = Courses.query.all()
        instructors = Instructors.query.all()
        return render_template('dataEntryPage/add_section.html', courses=courses, instructors=instructors)

    @app.route('/delete_section/<int:section_id>', methods=['POST'])
    def delete_section(section_id):
        section = Sections.query.get_or_404(section_id)
        db.session.delete(section)
        db.session.commit()
        return redirect(url_for('list_sections'))

    @app.route('/edit_section/<int:section_id>', methods=['GET', 'POST'])
    def edit_section(section_id):
        section = Sections.query.get_or_404(section_id)
        if request.method == 'POST':
            section.course_id = request.form['course_id']
            section.year = request.form['year']
            section.semester = request.form['semester']
            section.instructor_id = request.form['instructor_id']
            section.enrollment_count = request.form['enrollment_count']
            db.session.commit()
            return redirect(url_for('list_sections'))

        courses = Courses.query.all()
        instructors = Instructors.query.all()
        return render_template('dataEntryPage/edit_section.html', section=section, courses=courses, instructors=instructors)

    @app.route('/sections/<int:instructor_id>')
    def list_sections_by_instructor(instructor_id):
        # This is where we define sections
        sections = Sections.query.filter_by(instructor_id=instructor_id).all()
        return render_template('dataEntryPage/list_sections_by_instructor.html', sections=sections, instructor_id=instructor_id)