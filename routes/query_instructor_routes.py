from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import db, Instructors
from database import db

query_instructor_routes = Blueprint('query_instructor_routes', __name__)

@query_instructor_routes.route('/query_instructor', methods=['GET'])
def query_form():
    print("Route is being called")
    instructor_names = db.session.query(Instructors.name).distinct().all()
    instructor_names = [name[0] for name in instructor_names]  
    return render_template('dataQueryPage/query_instructor.html', instructors_names=instructor_names)
