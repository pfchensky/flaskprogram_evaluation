from flask import Blueprint, request, redirect, url_for, render_template
from models import db, Sections, Evaluations 

query_section_percentage_routes = Blueprint('query_section_percentage_routes', __name__)

@query_section_percentage_routes.route('/query_section_percentage', methods=['GET', 'POST'])
def query_form():
    if request.method == 'GET':
        print("Route is being called")
        # Assuming you want to extract years and semesters for the query form
        years = Sections.query.with_entities(Sections.year).distinct().order_by(Sections.year.desc()).all()
        semesters = Sections.query.with_entities(Sections.semester).distinct().all()
        years = [year[0] for year in years]
        semesters = [semester[0] for semester in semesters]
        return render_template('dataQueryPage/query_section_percentage.html', years=years, semesters=semesters)
    elif request.method == 'POST':
        year = request.form.get('year')
        semester = request.form.get('semester')
        percentage = request.form.get('percentage')
        if year and semester and percentage:
            # Redirect to another route that handles displaying sections based on the year, semester, and percentage
            return redirect(url_for('query_section_percentage_routes.show_sections_percentage', year=year, semester=semester, percentage=percentage))
    # Redirect back if parameters are missing or if the request method is not POST
    return redirect(url_for('query_section_percentage_routes.query_form'))

@query_section_percentage_routes.route('/show_sections_percentage/<int:year>/<semester>/<float:percentage>', methods=['GET'])
def show_sections_percentage(year, semester, percentage):
    # Query for sections based on the given year and semester
    sections = Sections.query.filter_by(year=year, semester=semester).all()
    sections_evaluation = []
    for section in sections:
        evaluations = Evaluations.query.filter_by(section_id=section.section_id).all()
        if not evaluations:
            evaluation_status = 'Not Entered'
        else:
            # Calculate the percentage of students who did not get the 'F' grade
            total_students = sum(eval.perform_A + eval.perform_B + eval.perform_C + eval.perform_F for eval in evaluations)
            students_with_f = sum(eval.perform_F for eval in evaluations)
            percentage_no_f = ((total_students - students_with_f) / total_students) * 100
            if percentage_no_f >= percentage:
                evaluation_status = f'Reached {percentage}%'
            else:
                evaluation_status = f'Not Reached {percentage}%'
        sections_evaluation.append({'section': section, 'evaluation_status': evaluation_status,'total_students': total_students,'students_with_f':students_with_f})
    return render_template('dataQueryPage/list_section_percentage.html', sections_evaluation=sections_evaluation, year=year, semester=semester, percentage=percentage)
