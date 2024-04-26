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

from flask import jsonify

@evaluation_routes.route('/list_evaluation', methods=['GET'])
def list_evaluation():
    degree_name = request.args.get('degree_name')
    degree_level = request.args.get('degree_level')
    semester = request.args.get('semester')
    instructor_id = request.args.get('instructor_id')

    # 参数验证
    if not (degree_name and degree_level and semester and instructor_id):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        evaluations = Evaluations.query \
            .join(Sections, Sections.section_id == Evaluations.section_id) \
            .join(Instructors, Instructors.instructor_id == Sections.instructor_id) \
            .join(DegreeCourses, DegreeCourses.course_number == Sections.course_id) \
            .filter(Sections.instructor_id == instructor_id,
                    Sections.semester == semester,
                    DegreeCourses.degree_name == degree_name,
                    DegreeCourses.degree_level == degree_level) \
            .all()

        if not evaluations:
            # 通过模板显示无评估数据的信息
            return render_template('evaluationPage/no_evaluations.html'), 404

        # 使用模板渲染评估数据
        return render_template('evaluationPage/list_evaluation.html', evaluations=evaluations)
    except Exception as e:
        # 在异常情况下，使用模板来显示错误信息
        return render_template('evaluationPage/error.html', error=str(e)), 500

# @evaluation_routes.route('/list_evaluation', methods=['GET'])
# def list_evaluation():
#     degree_name = request.args.get('degree_name')
#     degree_level = request.args.get('degree_level')
#     semester = request.args.get('semester')
#     instructor_id = request.args.get('instructor_id')
#
#     # 参数验证（示例）
#     if not (degree_name and degree_level and semester and instructor_id):
#         return jsonify({"error": "Missing required parameters"}), 400
#
#     try:
#         evaluations = Evaluations.query \
#             .join(Sections, Sections.section_id == Evaluations.section_id) \
#             .join(Instructors, Instructors.instructor_id == Sections.instructor_id) \
#             .join(DegreeCourses, DegreeCourses.course_number == Sections.course_id) \
#             .filter(Sections.instructor_id == instructor_id,
#                     Sections.semester == semester,
#                     DegreeCourses.degree_name == degree_name,
#                     DegreeCourses.degree_level == degree_level) \
#             .all()
#
#         if not evaluations:
#             return jsonify({"error": "No evaluations found"}), 404
#
#         evaluations_list = [{
#             'evaluation_id': evaluation.evaluation_id,
#             'section_id': evaluation.section_id,
#             # Include other fields as necessary
#             'degree_name': evaluation.degree_name,  # 确保字段正确
#             'degree_level': evaluation.degree_level,
#             'assess_method': evaluation.assess_method,
#             'perform_A': evaluation.perform_A,
#             'perform_B': evaluation.perform_B,
#             'perform_C': evaluation.perform_C,
#             'perform_F': evaluation.perform_F,
#             'improve_sugs': evaluation.improve_sugs
#         } for evaluation in evaluations]
#
#         return jsonify(evaluations_list)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


@evaluation_routes.route('/edit_evaluation/<int:evaluation_id>')
def edit_evaluation(evaluation_id):
    evaluation = Evaluations.query.get(evaluation_id)
    if evaluation:
        return render_template('evaluationPage/edit_evaluation.html', evaluation=evaluation)
    else:
        return 'Evaluation not found', 404


@evaluation_routes.route('/update_evaluation/<int:evaluation_id>', methods=['POST'])
def update_evaluation(evaluation_id):
    evaluation = Evaluations.query.get(evaluation_id)
    if evaluation:
        # 更新所有可能的字段
        evaluation.degree_name = request.form['degree_name']
        evaluation.degree_level = request.form['degree_level']
        evaluation.assess_method = request.form['assess_method']
        evaluation.perform_A = request.form['perform_A']
        evaluation.perform_B = request.form['perform_B']
        evaluation.perform_C = request.form['perform_C']
        evaluation.perform_F = request.form['perform_F']
        evaluation.improve_sugs = request.form['improve_sugs']

        db.session.commit()
        # 重定向到更新成功页面
        return render_template('evaluationPage/update_success.html')
    else:
        return 'Evaluation not found', 404
