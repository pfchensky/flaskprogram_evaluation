from flask import flash, render_template, request, redirect, url_for
from models import Degrees
from database import db

def init_degree_routes(app):
    @app.route('/degrees')
    def list_degrees():
        degrees = Degrees.query.all()
        return render_template('list_degrees.html', degrees=degrees)

    @app.route('/add_degree', methods=['GET', 'POST'])
    def add_degree():
        if request.method == 'POST':
            name = request.form['name']
            level = request.form['level']
            # Check if the combination of name and level already exists
            existing_degree = Degrees.query.filter_by(name=name, level=level).first()
            if existing_degree:
                flash('A degree with the same name and level already exists.', 'error')
                return redirect(url_for('add_degree'))
            new_degree = Degrees(name=name, level=level)
            db.session.add(new_degree)
            db.session.commit()
            flash('New degree added successfully.', 'success')
            return redirect(url_for('list_degrees'))
        return render_template('add_degree.html')

    @app.route('/delete_degree/<name>/<level>', methods=['POST'])
    def delete_degree(name, level):
        degree = Degrees.query.filter_by(name=name, level=level).first()
        if degree:
            db.session.delete(degree)
            db.session.commit()
            flash('Degree deleted successfully.', 'success')
        else:
            flash('Degree not found.', 'error')
        return redirect(url_for('list_degrees'))

    @app.route('/edit_degree/<name>/<level>', methods=['GET', 'POST'])
    def edit_degree(name, level):
        degree = Degrees.query.filter_by(name=name, level=level).first_or_404()
        if request.method == 'POST':
            new_name = request.form['name']
            new_level = request.form['level']
            # Check if updated to a new unique combination
            if (new_name != name or new_level != level) and Degrees.query.filter_by(name=new_name, level=new_level).first():
                flash('Another degree with the same name and level already exists.', 'error')
                return redirect(url_for('edit_degree', name=name, level=level))
            degree.name = new_name
            degree.level = new_level
            db.session.commit()
            flash('Degree updated successfully.', 'success')
            return redirect(url_for('list_degrees'))
        return render_template('edit_degree.html', degree=degree)