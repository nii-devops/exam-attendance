from flask_login import UserMixin, LoginManager
from app import db



##########################
# ###  Database models
#######################


user_session = db.Table('user_session',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('exam_session_id', db.Integer, db.ForeignKey('exam_session.id'), primary_key=True)
)

# Add the association table for the many-to-many relationship
session_venue = db.Table('session_venue',
    db.Column('exam_session_id', db.Integer, db.ForeignKey('exam_session.id'), primary_key=True),
    db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'), primary_key=True)
)

exam_venue = db.Table('exam_venue',
    db.Column('exam_id', db.Integer, db.ForeignKey('exam.id')),
    db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'))
)

exam_programme = db.Table('exam_programme',
    db.Column('exam_id', db.Integer, db.ForeignKey('exam.id')),
    db.Column('programme_id', db.Integer, db.ForeignKey('programme.id'))
)

# Add this new association table
day_examsession = db.Table('day_examsession',
    db.Column('day_id', db.Integer, db.ForeignKey('day.id')),
    db.Column('session_id', db.Integer, db.ForeignKey('exam_session.id'))
)

# Association table for Schedule and Staff (User)
schedule_staff = db.Table('schedule_staff',
    db.Column('schedule_id', db.Integer, db.ForeignKey('schedule.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

# Association table for Schedule and Staff (User)
attendance_staff = db.Table('attendance_staff',
    db.Column('attendance_id', db.Integer, db.ForeignKey('attendance.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


class Title(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title_id = db.Column(db.Integer, db.ForeignKey('title.id'), nullable=True)
    title = db.relationship('Title', foreign_keys=[title_id])
    surname = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(40), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', back_populates='users')
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    department = db.relationship('Department', back_populates='users')
    
    role = db.Column(db.String(30), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    session_count = db.Column(db.Integer, default=0)
    # One-directional relationship (no back_populates)
    sessions = db.relationship('ExamSession', secondary='user_session')

    @property
    def is_superuser(self):
        return self.id == 1 or self.is_admin


class ExamSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    academic_year_id = db.Column(db.Integer, db.ForeignKey('academic_year.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'), nullable=False)
    exam_type_id = db.Column(db.Integer, db.ForeignKey('exam_type.id'), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=False)

    # Relationships
    academic_year = db.relationship('AcademicYear', backref='sessions')
    semester = db.relationship('Semester', backref='sessions')
    exam_type = db.relationship('ExamType', backref='sessions')
    day = db.relationship('Day', back_populates='sessions')



class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    
    session_id = db.Column(db.Integer, db.ForeignKey('exam_session.id'))
    session = db.relationship('ExamSession', backref='exams')

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship('Course', backref='exams')

    programmes = db.relationship('Programme', secondary=exam_programme, 
                                lazy='subquery', backref=db.backref('exams', lazy=True))
    venues = db.relationship('Venue', secondary=exam_venue, 
                            lazy='subquery', backref=db.backref('exams', lazy=True))   
    @property
    def date(self):
        return self.session.date if self.session else None



class AcademicYear(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(20), nullable=False)


class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    semester = db.Column(db.String(20), nullable=False)
    

class ExamType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_type = db.Column(db.String(20), nullable=False)
    

class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=True)

    # One-directional relationship (no back_populates)
    sessions = db.relationship('ExamSession', secondary='session_venue')


class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    sessions = db.relationship('ExamSession', back_populates='day')


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    users = db.relationship('User', back_populates='department')


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    users = db.relationship('User', back_populates='category')



class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='attendances')

    exam_session_id = db.Column(db.Integer, db.ForeignKey('exam_session.id'), nullable=False)  # Fixed
    exam_session = db.relationship('ExamSession', backref='attendances')  # Fixed

    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    venue = db.relationship('Venue', backref='attendances') 
    
    timestamp = db.Column(db.DateTime, nullable=False)



class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(50), unique=True)
    title = db.Column(db.String(150))  



class Programme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    year_group = db.Column(db.Integer)
    number = db.Column(db.Integer, nullable=True)



class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    # Add relationship to the Exam model
    exam = db.relationship('Exam', backref=db.backref('schedules', lazy=True))
    # Define many-to-many relationship with User (for staff)
    staff = db.relationship('User', secondary=schedule_staff, lazy='subquery',
                            backref=db.backref('assigned_schedules', lazy=True))
   






