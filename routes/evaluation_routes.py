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

# @evaluation_routes.route('/list_evaluation', methods=['GET'])
# def list_evaluation():
#     degree_name = request.args.get('degree_name')
#     degree_level = request.args.get('degree_level')
#     semester = request.args.get('semester')
#     instructor_id = request.args.get('instructor_id')
#
#     evaluations = Evaluations.query \
#         .join(Sections, Sections.section_id == Evaluations.section_id) \
#         .join(DegreeCourses, DegreeCourses.course_number == Sections.course_id) \
#         .filter(Sections.instructor_id == instructor_id,
#                 Sections.semester == semester,
#                 DegreeCourses.degree_name == degree_name,
#                 DegreeCourses.degree_level == degree_level) \
#         .all()
#
#     if not evaluations:
#         print("No evaluations found")  # Debug statement
#
#     return render_template('evaluationPage/list_evaluation.html', evaluations=evaluations)
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


@evaluation_routes.route('/edit', methods=['POST'])
def edit_evaluation():
    data = request.json
    evaluation_id = data['evaluation_id']
    evaluation = Evaluations.query.get(evaluation_id)
    if evaluation:
        # Manually updating each field:
        evaluation.perform_A = data.get('perform_A', evaluation.perform_A)
        evaluation.perform_B = data.get('perform_B', evaluation.perform_B)
        evaluation.perform_C = data.get('perform_C', evaluation.perform_C)
        evaluation.perform_F = data.get('perform_B', evaluation.perform_F)
        # Add other fields as necessary
        db.session.commit()
        return jsonify({'message': 'Evaluation updated successfully'})
    return jsonify({'message': 'Evaluation not found'}), 404

@evaluation_routes.route('/delete', methods=['DELETE'])
def delete_evaluation():
    evaluation_id = request.args.get('evaluation_id')
    evaluation = Evaluations.query.get(evaluation_id)
    if evaluation:
        db.session.delete(evaluation)
        db.session.commit()
        return jsonify({'message': 'Evaluation deleted successfully'})
    return jsonify({'message': 'Evaluation not found'}), 404
