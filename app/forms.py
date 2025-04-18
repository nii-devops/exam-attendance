from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField, PasswordField, EmailField, SelectMultipleField, 
                     DateField, TimeField, HiddenField)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from app.models import *
from app.data import titles



"""
def category_query():
    # Returns a query object for all categories
    return Category.query

def department_query():
    # Returns a query object for all departments
    return Department.query
    
def exam_query():
    return Exam.query

def staff_query():
    # return User.query.filter(User.role == 'Biometric Staff (IT)')
    return User.query.filter(User.role == 'Biometric Staff (IT)') # Or simply return all users for now
"""



staff_category = (
    ("Senior Staff", "Senior Staff"),
    ("PhD Candidate", "PhD Candidate"),
    ("Senior Member (Academic)", "Senior Member (Academic)"),
    ("Senior Member (Administrative)", "Senior Member (Administrative)")
    )




class RegisterForm(FlaskForm):
    title = QuerySelectField(
        'Title',
        query_factory=lambda: Title.query.all(),
        get_label='title', # Assumes your Category model has a 'name' attribute
        allow_blank=True, # Optional: add a blank choice
        blank_text='-- Select Title --',
        validators=[DataRequired()]
        )
    surname = StringField('Surname', validators=[DataRequired()])
    first_name = StringField('First Name(s)', validators=[DataRequired()])
    email = EmailField('Email',)
    # Use QuerySelectField to populate choices from the Category model
    category = QuerySelectField(
        'Staff Category',
        query_factory=lambda: Category.query.all(),
        get_label='name', # Assumes your Category model has a 'name' attribute
        allow_blank=True, # Optional: add a blank choice
        blank_text='-- Select Category --',
        validators=[DataRequired()]
        )
    # Update department field similarly (assuming a Department model)
    department = QuerySelectField(
        'Department',
        query_factory=lambda: Department.query.all(),
        get_label='name', # Assumes your Department model has a 'name' attribute
        allow_blank=True,
        blank_text='-- Select Department --',
        validators=[DataRequired()]
        )
    phone = StringField('Phone', )
    password = PasswordField('Password', validators=[DataRequired()])
    password_2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')]
    )
    submit = SubmitField('Register') # Changed submit label for clarity


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class TitleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Submit')



class ExcelFileForm(FlaskForm):
    filename = SelectField('Rank ID', choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit')


class PasswordResetForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')]
    )
    submit = SubmitField('Reset Password') # Changed submit label for clarity



class UserForm(FlaskForm):
    title = QuerySelectField(
        'Title',
        query_factory=lambda: Title.query.all(),
        get_label='title', # Assumes your Category model has a 'name' attribute
        allow_blank=True, # Optional: add a blank choice
        blank_text='-- Select Title --',
        validators=[DataRequired()]
        )
    surname = StringField('Surname', validators=[DataRequired()])
    first_name = StringField('First Name(s)', validators=[DataRequired()])
    category = QuerySelectField(
        'Staff Category',
        query_factory=lambda: Category.query.all(),
        get_label='name', # Assumes your Category model has a 'name' attribute
        allow_blank=True, # Optional: add a blank choice
        blank_text='-- Select Category --',
        validators=[DataRequired()]
        )
    # Update department field similarly (assuming a Department model)
    department = QuerySelectField(
        'Department',
        query_factory=lambda: Department.query.all(),
        get_label='name', # Assumes your Department model has a 'name' attribute
        allow_blank=True,
        blank_text='-- Select Department --',
        validators=[DataRequired()]
        )
    
    phone = StringField('Phone No. (Optional)', )
    submit = SubmitField('Add User')



class CategoryForm(FlaskForm):
    name = StringField('Staff Category', validators=[DataRequired()])
    submit = SubmitField('Create')


class DepartmentForm(FlaskForm):
    name = StringField('Department Name', validators=[DataRequired()])
    submit = SubmitField('Create')



class ExamForm(FlaskForm):
    title = StringField('Exam Title', validators=[DataRequired()])
    #date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    session = QuerySelectField(
        'Session',
        query_factory=lambda: ExamSession.query.all(),
        get_label=lambda s: f'{s.name} - {s.start_time}',
        allow_blank=False,
        render_kw={'size': 6}
    )
    course = QuerySelectField(
        'Course',
        query_factory=lambda: Course.query.order_by(Course.course_code).all(),
        get_label=lambda c: f"{c.course_code} - {c.title}",
        allow_blank=False,
        render_kw={'size': 6}
    )
    programmes = QuerySelectMultipleField(
        'Programmes',
        query_factory=lambda: Programme.query.order_by(Programme.name).all(),
        get_label=lambda p: f"{p.name} - Year {p.year_group}",
        render_kw={'size': 6}
    )
    venues = QuerySelectMultipleField(
        'Venues',
        query_factory=lambda: Venue.query.order_by(Venue.name).all(),
        get_label='name',
        render_kw={'size': 6}
    )
    submit = SubmitField('Schedule Exam')




class ExamSessionForm(FlaskForm):
    name = StringField('Session Name', validators=[DataRequired()])
    
    day_id = QuerySelectField(
        'Day',
        query_factory=lambda: Day.query.order_by(Day.id).all(),
        get_label='name',
        allow_blank=False,
        render_kw={'size': 5}
    )

    date = DateField("Date")

    start_time = TimeField(
        'Start Time',
        validators=[DataRequired()],
        format='%H:%M'
    )

    end_time = TimeField(
        'End Time',
        validators=[DataRequired()],
        format='%H:%M'
    )

    academic_year = QuerySelectField(
        'Academic Year',
        query_factory=lambda: AcademicYear.query.order_by(AcademicYear.id).all(),
        get_label='year',
        validators=[DataRequired()],
        allow_blank=False,
        render_kw={'size': 3}
    )

    semester = QuerySelectField(
        'Semester',
        query_factory=lambda: Semester.query.order_by(Semester.id).all(),
        get_label='semester',
        validators=[DataRequired()],
        allow_blank=False,
        render_kw={'size': 3}
    )

    exam_type = QuerySelectField(
        'Exam Type',
        query_factory=lambda: ExamType.query.order_by(ExamType.id).all(),
        get_label='exam_type',
        validators=[DataRequired()],
        allow_blank=False,
        render_kw={'size': 3}
    )

    submit = SubmitField('Create/Update Session')

    # Keep your custom validator
    def validate_end_time(self, field):
        if self.start_time.data and field.data:
            if field.data <= self.start_time.data:
                raise ValidationError('End time must be after start time.')




class ScheduleForm(FlaskForm):
    """Form for creating or editing a Schedule."""
    exam = QuerySelectField(
        'Exam',
        query_factory=lambda: Exam.query.all(),
        get_label='title', # Display the exam title in the dropdown
        allow_blank=False, # Require an exam to be selected
        description='Select the exam for this schedule.'
    )
    staff = QuerySelectMultipleField(
        'Assign Staff',
        query_factory=lambda: User.query.filter(User.role == 'Biometric Staff - IT').all(),
        get_label=lambda user: f"{user.first_name} {user.surname}", # Display user's full name
        allow_blank=True, # Allow schedules with no staff initially assigned
        description='Select one or more staff members to assign.'
    )

    submit = SubmitField('Save Schedule')



class CourseForm(FlaskForm):
    course_code = StringField('Course Code', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AcademicYearForm(FlaskForm):
    year = StringField('Academic Year', validators=[DataRequired()], render_kw={'placeholder': 'e.g. 2020/2021 Academic Year'})
    submit = SubmitField('Submit')



class AttendanceForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()], render_kw={'id': 'date_field'})

    # Provide a default callable for the session field
    session = QuerySelectField(
        'Session',
        query_factory=lambda: ExamSession.query.all(),
        get_label=lambda s: f"{s.name} - {s.start_time}",
        allow_blank=False,
        render_kw={'size': 6, 'id': 'session_field'}
    )

    venues = QuerySelectField(
        'Venue',
        query_factory=lambda: Venue.query.order_by(Venue.name).all(),
        get_label='name',
        render_kw={'size': 6, 'id': 'venues_field'}
    )

    staff_id = HiddenField(
        'Staff ID',
        render_kw={'id': 'staff_id_field'}
    )
    
    staff_search = StringField(
        'Staff Search',
        render_kw={
            'id': 'staff_search_field',
            'placeholder': 'Type to search staff...'
        }
    )

    submit = SubmitField(
        'Submit',
        render_kw={'id': 'submit_button'}
    )

    def __init__(self, selected_date=None, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        # Override the query_factory based on selected_date
        if selected_date:
            self.session.query_factory = lambda: ExamSession.query.filter(
                db.func.date(ExamSession.date) == selected_date
            ).all()
        else:
            self.session.query_factory = lambda: ExamSession.query.all()


class SessionFilterForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    session = QuerySelectField(
        'Session',
        query_factory=lambda: ExamSession.query.all(),
        get_label=lambda s: f"{s.name} - {s.start_time}",
        allow_blank=False,
        render_kw={'size': 6, 'id': 'session_field'}
    )
    
    academic_year = QuerySelectField(
        'Academic Year',
        query_factory=lambda: AcademicYear.query.order_by(AcademicYear.id).all(),
        get_label='year',
        validators=[DataRequired()],
        allow_blank=False,
        render_kw={'size': 3}
    )

    semester = QuerySelectField(
        'Semester',
        query_factory=lambda: Semester.query.order_by(Semester.id).all(),
        get_label='semester',
        validators=[DataRequired()],
        allow_blank=False,
        render_kw={'size': 3}
    )

    exam_type = QuerySelectField(
        'Exam Type',
        query_factory=lambda: ExamType.query.order_by(ExamType.id).all(),
        get_label='exam_type',
        validators=[DataRequired()],
        allow_blank=False,
        render_kw={'size': 3}
    )

    submit = SubmitField('Filter')


"""
class AttendanceForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()], render_kw={'id': 'date_field'})


    session = QuerySelectField(
        'Session',
        get_label=lambda s: f"{s.name} - {s.start_time}",
        allow_blank=False,
        render_kw={'size': 6, 'id': 'session_field'}
    )

    venues = QuerySelectField(
        'Venue',
        query_factory=lambda: Venue.query.order_by(Venue.name).all(),
        get_label='name',
        render_kw={'size': 6, 'id': 'venues_field'}
    )

    staff = QuerySelectField(
        'Staff',
        query_factory=lambda: User.query.order_by(User.surname).all(),
        get_label=lambda user: f"{user.first_name} {user.surname}",
        render_kw={'size': 6, 'id': 'venues_field'}
    )

    submit = SubmitField(
        'Submit',
        render_kw={'id': 'submit_button'}
    )

"""









"""


class ExamForm(FlaskForm):
    title = StringField('Exam Title', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    day = SelectField('Day', coerce=int, render_kw={'size': 6})
    session = SelectField('Session', coerce=int, render_kw={'size': 6})
    course = SelectField('Course', coerce=int, render_kw={'size': 6})
    programmes = SelectMultipleField('Programmes', coerce=int, render_kw={'size': 6})
    venues = SelectMultipleField('Venues', coerce=int, render_kw={'size': 6})
    submit = SubmitField('Schedule Exam')

    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        self.day.choices = [(d.id, d.name) for d in Day.query.all()]
        # Session choices will be updated dynamically based on day selection
        self.session.choices = [(s.id, f'{s.name} - {s.start_time}') for s in ExamSession.query.all()]
        self.course.choices = [(c.id, f"{c.course_code} - {c.title}") for c in Course.query.order_by(Course.course_code).all()]
        self.programmes.choices = [(p.id, f"{p.name} - Year {p.year_group}") for p in Programme.query.order_by(Programme.name).all()]
        self.venues.choices = [(v.id, v.name) for v in Venue.query.order_by(Venue.name).all()]




class ExamSessionForm(FlaskForm):
    name = StringField('Session Name', validators=[DataRequired()])
    day_id = SelectField('Day', coerce=int, render_kw={'size': 5})
    date = DateField("Date")
    start_time = TimeField('Start Time', validators=[DataRequired()], format='%H:%M')
    end_time = TimeField('End Time', validators=[DataRequired()], format='%H:%M')
    academic_year_id = SelectField('Academic Year', validators=[DataRequired()],coerce=int, render_kw={'size': 3})
    semester_id = SelectField('Semester', validators=[DataRequired()], coerce=int, render_kw={'size': 3})
    exam_type_id = SelectField('Exam Type', validators=[DataRequired()], coerce=int, render_kw={'size': 3})
    # Example: form.days.choices = [(d.id, d.name) for d in Day.query.all()]
    
    submit = SubmitField('Create/Update Session')

    # Add __init__ to populate choices
    def __init__(self, *args, **kwargs):
        super(ExamSessionForm, self).__init__(*args, **kwargs)
        # Populate choices from models
        self.day_id.choices = [(d.id, d.name) for d in Day.query.order_by(Day.id).all()]
        self.academic_year_id.choices = [(ay.id, ay.year) for ay in AcademicYear.query.order_by(AcademicYear.id).all()]
        self.semester_id.choices = [(sem.id, sem.semester) for sem in Semester.query.order_by(Semester.id).all()]
        self.exam_type_id.choices = [(extype.id, extype.exam_type) for extype in ExamType.query.order_by(ExamType.id).all()]
        #self.venues.choices = [(v.id, v.name) for v in Venue.query.order_by(Venue.name).all()]

    # Optional: Add custom validation
    def validate_end_time(self, field):
        if self.start_time.data and field.data:
            if field.data <= self.start_time.data:
                raise ValidationError('End time must be after start time.')


class AttendanceForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    day = SelectField('Day', coerce=int, render_kw={'size': 6})
    session = SelectField('Session', coerce=int, render_kw={'size': 6})
    course = SelectField('Course', coerce=int, render_kw={'size': 6})
    programmes = SelectMultipleField('Programmes', coerce=int, render_kw={'size': 6})
    venues = SelectMultipleField('Venues', coerce=int, render_kw={'size': 6})
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        self.day.choices = [(d.id, d.name) for d in Day.query.all()]
        # Session choices will be updated dynamically based on day selection
        self.session.choices = [(s.id, f'{s.name} - {s.start_time}') for s in ExamSession.query.all()]
        self.course.choices = [(c.id, f"{c.course_code} - {c.title}") for c in Course.query.order_by(Course.course_code).all()]
        self.programmes.choices = [(p.id, f"{p.name} - Year {p.year_group}") for p in Programme.query.order_by(Programme.name).all()]
        self.venues.choices = [(v.id, v.name) for v in Venue.query.order_by(Venue.name).all()]


"""





