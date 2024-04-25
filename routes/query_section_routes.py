# query_semester_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Sections, Evaluations

query_section_routes = Blueprint('query_section_routes', __name__)

@query_section_routes.route('/select_semester', methods=['GET'])
def select_term():
    # Extract distinct years and semesters from the database
    years = db.session.query(Sections.year).distinct().all()
    semesters = db.session.query(Sections.semester).distinct().all()
    years = [year[0] for year in years]
    semesters = [semester[0] for semester in semesters]
    return render_template('dataQueryPage/query_section.html', years=years, semesters=semesters)

@query_section_routes.route('/list_sections', methods=['GET'])
def list_sections_for_term():
    selected_year = request.args.get('year')
    selected_semester = request.args.get('semester')
    if selected_year and selected_semester:
        return redirect(url_for('query_section_routes.show_sections', year=selected_year, semester=selected_semester))
    return redirect(url_for('query_section_routes.select_term'))

@query_section_routes.route('/show_sections/<int:year>/<semester>', methods=['GET'])
def show_sections(year, semester):
    # Query for sections for the given year and semester
    sections = Sections.query.filter_by(year=year, semester=semester).all()

    # Determine the evaluation status for each section
    sections_evaluation = []
    for section in sections:
        evaluations = Evaluations.query.filter_by(section_id=section.section_id).all()

        # Default status if no evaluations are present
        evaluation_status = 'Not Entered'

        # If evaluations exist, determine their completeness
        if evaluations:
            eval_status = [
                'Partially Entered' if (
                    eval.assess_method is None or 
                    eval.perform_A is None or 
                    eval.perform_B is None or 
                    eval.perform_C is None or 
                    eval.perform_F is None
                ) else 'Entered' 
                for eval in evaluations
            ]

            # Check if any improvements have been suggested
            improvement_entered = any(eval.improve_sugs for eval in evaluations)

            # Determine final evaluation status
            if 'Partially Entered' in eval_status:
                evaluation_status = 'Partially Entered'
            elif improvement_entered:
                evaluation_status = 'Entered with Improvement'
            else:
                evaluation_status = 'Entered'
        
        # Append section and its evaluation status to the list
        sections_evaluation.append({
            'section': section,
            'evaluation_status': evaluation_status
        })

    return render_template('dataQueryPage/list_section_evaluation.html', sections_evaluation=sections_evaluation, year=year, semester=semester)

