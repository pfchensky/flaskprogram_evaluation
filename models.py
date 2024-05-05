from flask_sqlalchemy import SQLAlchemy

from database import db, config_app 


class Degrees(db.Model):
    __tablename__ = 'Degrees'
    name = db.Column(db.String(255), primary_key=True)
    level = db.Column(db.String(255), primary_key=True)


class Courses(db.Model):
    __tablename__ = 'Courses'
    course_id = db.Column(db.String(7), primary_key=True)
    name = db.Column(db.String(255), unique=True)


class Instructors(db.Model):
    __tablename__ = 'Instructors'
    instructor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Sections(db.Model):
    __tablename__ = 'Sections'
    section_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(7), db.ForeignKey('Courses.course_id'), primary_key=True)
    year = db.Column(db.Integer)
    semester = db.Column(db.Enum('Spring', 'Summer', 'Fall'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('Instructors.instructor_id'))
    enrollment_count = db.Column(db.Integer)


class LearningObjectives(db.Model):
    __tablename__ = 'LearningObjectives'
    learningObjective_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    description = db.Column(db.Text)


class Evaluations(db.Model):
    __tablename__ = 'Evaluations'
    evaluation_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('Sections.section_id'))
    course_id = db.Column(db.String(7), db.ForeignKey('Sections.course_id'))  
    learningObjective_id = db.Column(db.Integer, db.ForeignKey('LearningObjectives.learningObjective_id'))
    degree_name = db.Column(db.String(255))
    degree_level = db.Column(db.String(255))
    assess_method = db.Column(db.Enum('Homework', 'Project', 'Quiz', 'Oral Presentation', 'Report', 'Mid-term', 'Final Exam', 'others'))
    perform_A = db.Column(db.Integer)
    perform_B = db.Column(db.Integer)
    perform_C = db.Column(db.Integer)
    perform_F = db.Column(db.Integer)
    improve_sugs = db.Column(db.Text)


class DegreeCourses(db.Model):
    __tablename__ = 'DegreeCourses'
    degree_name = db.Column(db.String(255), primary_key=True)
    degree_level = db.Column(db.String(255), primary_key=True)
    course_number = db.Column(db.String(7), db.ForeignKey('Courses.course_id'), primary_key=True)
    is_core = db.Column(db.Boolean)


class CourseObjectives(db.Model):
    __tablename__ = 'CourseObjectives'
    course_id = db.Column(db.String(7), db.ForeignKey('Courses.course_id'), primary_key=True)
    learningObjective_id = db.Column(db.Integer, db.ForeignKey('LearningObjectives.learningObjective_id'), primary_key=True)
