from sqlite3 import IntegrityError
from flask import flash, get_flashed_messages
from flask import render_template, request, redirect, url_for
from models import db, Sections, Courses, Instructors
from sqlalchemy.exc import SQLAlchemyError

def init_section_routes(app):
    @app.route('/sections')
    def list_sections():
        sections = Sections.query.all()
        return render_template('dataEntryPage/list_sections.html', sections=sections)

    @app.route('/add_section', methods=['GET', 'POST'])
    def add_section():
        courses = Courses.query.all()
        instructors = Instructors.query.all()
        if request.method == 'POST':
            try:
                section_id = int(request.form.get('section_id'))  # Explicit conversion to int
                course_id = request.form.get('course_id')
                year = int(request.form.get('year'))  # Already converting, added explicit cast
                semester = request.form.get('semester')
                instructor_id = int(request.form.get('instructor_id'))  # Explicit conversion to int
                enrollment_count = int(request.form.get('enrollment_count'))  # Explicit conversion to int

                # Validate year, semester, and enrollment count
                if not (1900 <= year <= 2100):
                    flash("Please enter a valid year.", 'error')
                elif semester not in ['Spring', 'Summer', 'Fall']:
                    flash("Please select a valid semester.", 'error')
                elif enrollment_count < 0:
                    flash("Enrollment count cannot be negative.", 'error')
                else:
                    new_section = Sections(
                        section_id=section_id,
                        course_id=course_id,
                        year=year,
                        semester=semester,
                        instructor_id=instructor_id,
                        enrollment_count=enrollment_count
                    )
                    db.session.add(new_section)
                    db.session.commit()
                    flash("Section added successfully!", 'success')
                    return redirect(url_for('list_sections'))  # Make sure 'list_sections' is correct

            except ValueError as e:
                flash("Please enter valid numeric values for Year, Instructor ID, and Enrollment Count. " + str(e), 'error')
            except SQLAlchemyError as e:
                flash(f"An error occurred while adding the section: {str(e)}", 'error')
                db.session.rollback()

        return render_template('dataEntryPage/add_section.html', courses=courses, instructors=instructors)

    @app.route('/delete_section/<int:section_id>/<course_id>', methods=['POST'])
    def delete_section(section_id, course_id):
        # Fetch using both parts of the composite primary key
        section = Sections.query.get_or_404((section_id, course_id))
        try:
            db.session.delete(section)
            db.session.commit()
            flash("Section deleted successfully.", 'success')
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error deleting section: {str(e)}", 'error')
        return redirect(url_for('list_sections'))

    @app.route('/edit_section/<int:section_id>/<course_id>', methods=['GET', 'POST'])
    def edit_section(section_id, course_id):
        # Fetch the section using both parts of the composite primary key
        section = Sections.query.get_or_404((section_id, course_id))

        courses = Courses.query.all()
        instructors = Instructors.query.all()

        if request.method == 'POST':
            try:
                # Assign form values to section properties
                section.course_id = request.form['course_id']
                section.year = int(request.form['year'])
                section.semester = request.form['semester']
                section.instructor_id = int(request.form['instructor_id'])
                section.enrollment_count = int(request.form['enrollment_count'])

                # Validate the inputs
                if not (1900 <= section.year <= 2100):
                    flash("Please enter a valid year.", 'error')
                    return render_template('dataEntryPage/edit_section.html', section=section, courses=courses, instructors=instructors)

                if section.semester not in ['Spring', 'Summer', 'Fall']:
                    flash("Please select a valid semester.", 'error')
                    return render_template('dataEntryPage/edit_section.html', section=section, courses=courses, instructors=instructors)

                if section.enrollment_count < 0:
                    flash("Enrollment count cannot be negative.", 'error')
                    return render_template('dataEntryPage/edit_section.html', section=section, courses=courses, instructors=instructors)

                db.session.commit()
                flash("Section updated successfully!", 'success')
                return redirect(url_for('list_sections'))

            except ValueError:
                flash("Please enter valid numeric values for Year, Instructor ID, and Enrollment Count.", 'error')
            except IntegrityError:
                db.session.rollback()
                flash("Section ID and Course ID combination must be unique.", 'error')
            except SQLAlchemyError as e:
                db.session.rollback()
                flash(f"An error occurred while updating the section: {str(e)}", 'error')

            return render_template('dataEntryPage/edit_section.html', section=section, courses=courses, instructors=instructors)

        # GET request handling
        return render_template('dataEntryPage/edit_section.html', section=section, courses=courses, instructors=instructors)


    @app.route('/sections/<int:instructor_id>')
    def list_sections_by_instructor(instructor_id):
        sections = Sections.query.filter_by(instructor_id=instructor_id).all()
        return render_template('dataEntryPage/list_sections_by_instructor.html', sections=sections, instructor_id=instructor_id)