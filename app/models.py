from flask_login import UserMixin, LoginManager
from app import db


##########################
# ###  Database models
###########################

# Association Tables

user_session = db.Table('user_session',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('session_id', db.Integer, db.ForeignKey('session.id'), primary_key=True)
)

session_venue = db.Table('session_venue',
    db.Column('session_id', db.Integer, db.ForeignKey('session.id'), primary_key=True),
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

schedule_staff = db.Table('schedule_staff',
    db.Column('schedule_id', db.Integer, db.ForeignKey('schedule.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

biometric_staff = db.Table('biometric_staff',
    db.Column('biometric_id', db.Integer, db.ForeignKey('biometric.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

attendance_staff = db.Table('attendance_staff',
    db.Column('attendance_id', db.Integer, db.ForeignKey('attendance.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

programme_level = db.Table('programme_level',
    db.Column('programme_id', db.Integer, db.ForeignKey('programme.id'), primary_key=True),
    db.Column('level_id', db.Integer, db.ForeignKey('level.id'), primary_key=True)
)





# Models

class Title(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title_id = db.Column(db.Integer, db.ForeignKey('title.id'), nullable=True)
    title = db.relationship('Title', foreign_keys=[title_id])
    surname = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(40), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', back_populates='users')
    
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    department = db.relationship('Department', back_populates='users')
    
    role = db.Column(db.String(30), nullable=True)

    is_manager = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    session_count = db.Column(db.Integer, default=0)
    # Relationship with Session via the user_session association table
    sessions = db.relationship('Session', secondary='user_session')

    @property
    def is_superuser(self):
        return self.id == 1 or self.is_admin


class SessionNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(20), nullable=False, unique=True)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    session_number_id = db.Column(db.Integer, db.ForeignKey('session_number.id'), nullable=False)
    academic_year_id = db.Column(db.Integer, db.ForeignKey('academic_year.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'), nullable=False)
    exam_type_id = db.Column(db.Integer, db.ForeignKey('exam_type.id'), nullable=False)

    # Relationships
    session_number = db.relationship('SessionNumber', backref='sessions')
    academic_year = db.relationship('AcademicYear', backref='sessions')
    semester = db.relationship('Semester', backref='sessions')
    exam_type = db.relationship('ExamType', backref='sessions')


class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'))
    level = db.relationship('Level', backref='exams')
    
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    session = db.relationship('Session', backref='exams')

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
    year = db.Column(db.String(20), unique=True, nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_year = db.Column(db.Integer, nullable=False)


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
    # A Venue can be associated with multiple Sessions via the session_venue association table
    sessions = db.relationship('Session', secondary='session_venue')


class GraduateType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    initials = db.Column(db.String(10), nullable=True)


class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    year_group = db.Column(db.String(20), nullable=False)
    level = db.Column(db.String(20), nullable=False)
       

class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    initials = db.Column(db.String(20), nullable=True)


class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    initials = db.Column(db.String(20), nullable=True)

    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=False)
    # Relationships
    college = db.relationship('College', backref='faculties')


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    initials = db.Column(db.String(20), nullable=True)
    
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=True)
    # Faculty Relationship
    faculty = db.relationship('Faculty', backref='departments')
    # User Relationship
    users = db.relationship('User', back_populates='department', lazy='dynamic') # lazy='dynamic' # optional, makes .users a query you can further filter


class Programme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    initials = db.Column(db.String(20), nullable=True)

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    # Relationships
    department = db.relationship('Department', backref='programmes')


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(50), unique=True)
    title = db.Column(db.String(150))

    programme_id = db.Column(db.Integer, db.ForeignKey('programme.id'), nullable=True)
    # Relationships
    programme = db.relationship('Programme', backref='courses')



class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    users = db.relationship('User', back_populates='category')
    allowance = db.relationship('Allowance', back_populates='category', uselist=False)

    @property
    def rate(self):
        """Returns the allowance rate for this category, or 0 if no allowance is set"""
        return self.allowance.rate if self.allowance else 0.0

    def __repr__(self):
        return f'<Category {self.name}>'



class Allowance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Float, nullable=False)  # Rate per session

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', back_populates='allowance')



class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='attendances')

    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    session = db.relationship('Session', backref='attendances')

    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    venue = db.relationship('Venue', backref='attendances')
    
    timestamp = db.Column(db.DateTime, nullable=False)


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    exam = db.relationship('Exam', backref=db.backref('schedules', lazy=True))
    staff = db.relationship('User', secondary=schedule_staff, lazy='subquery',
                            backref=db.backref('assigned_schedules', lazy=True))


class Biometric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Use a distinct backref name to avoid conflict with Attendance
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    session = db.relationship('Session', backref='biometric_entries')
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='biometric_entries')
    
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    venue = db.relationship('Venue', backref='biometrics')




