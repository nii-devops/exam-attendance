
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField, PasswordField, EmailField, SelectMultipleField, 
                     DateField, TimeField, HiddenField, FieldList, FormField, FloatField, IntegerField)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from app.models import *
from app.data import titles
from flask import request
from sqlalchemy import desc




##############################
# ### MODEL QUERIES #########

def category_query():
    # Returns a query object for all categories
    return Category.query

def department_query():
    # Returns a query object for all departments
    return Department.query

def exam_query():
    return Exam.query

def biometric_staff_query():
    # return User.query.filter(User.role == 'Biometric Staff (IT)')
    return User.query.filter(User.role == 'Biometric Staff (IT)') # Or simply return all users for now

def session_query():
    return Session.query.all()



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



class AcademicYearForm(FlaskForm):
    year = StringField('Academic Year', validators=[DataRequired()], render_kw={'placeholder': 'Format: 2020/2021 Academic Year'})
    start_year = IntegerField('Start Year', validators=[DataRequired()])
    end_year = IntegerField('End Year', validators=[DataRequired()])
    submit = SubmitField('Submit')



class DateForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Submit')



class DateSessionForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], render_kw={'id': 'date'})

    session = QuerySelectField(
        'Session',
        query_factory=session_query,
        get_label=lambda s: f"{s.date} - {s.start_time}",
        allow_blank=False,
        validators=[DataRequired()],
        render_kw={'id': 'session', 'size': 3}
    )
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



class AdminUserForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder': 'e.g. Dr.'})
    surname = StringField('Surname', validators=[DataRequired()])
    first_name = StringField('First Name(s)', validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    phone = StringField('Phone No. (Optional)', )
    department = StringField('Department', )
    category = StringField('Staff Category', validators=[DataRequired()], render_kw={'placeholder': 'e.g. Senior Member (Administrative)'}) 
    password = PasswordField('Password', validators=[DataRequired()])
    password_2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder': 'Passwords must match'})
    submit = SubmitField('Submit')



class CategoryForm(FlaskForm):
    name = StringField('Staff Category', validators=[DataRequired()])
    submit = SubmitField('Create')



class DepartmentForm(FlaskForm):
    name = StringField('Department Name', validators=[DataRequired()])
    submit = SubmitField('Create')



class ProgrammeForm(FlaskForm):
    name = StringField('Programme Name', validators=[DataRequired()])
    department = QuerySelectField(
        'Department',
        query_factory=lambda: Department.query.order_by(Department.id).all(),
        get_label='name',
        validators=[DataRequired()],
        allow_blank=False,
        render_kw={'size': 5}
    )
    submit = SubmitField('Create')



class ExamForm(FlaskForm):
    level = QuerySelectField(
        'Level',
        query_factory=lambda: Level.query.all(),
        get_label=lambda l: f"{l.year_group}",
        allow_blank=False,
        render_kw={'size': 4} # Keep size for non-Select2 fields if desired
    )

    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()], render_kw={'id': 'date_field'})

    session = QuerySelectField(
        'Session',
        query_factory=lambda: Session.query.all(), # Initial query, might be updated by JS
        get_label=lambda s: f"{s.date} - {s.start_time}",
        allow_blank=False,
        render_kw={'size': 3, 'id': 'session_field'} # Keep size for non-Select2 fields if desired
    )

    course = QuerySelectField(
        'Course',
        query_factory=lambda: Course.query.order_by(Course.course_code).all(),
        get_label=lambda c: f"{c.course_code} - {c.title}",
        allow_blank=False,
        # Remove size, add id for Select2
        render_kw={'id': 'course_field'}
    )
    programmes = QuerySelectMultipleField(
        'Programmes',
        query_factory=lambda: Programme.query.order_by(Programme.name).all(),
        get_label=lambda p: f"{p.name}",
        # Remove size, add id for Select2
        render_kw={'id': 'programmes_field'}
    )

    venues = QuerySelectMultipleField(
        'Venues',
        query_factory=lambda: Venue.query.order_by(Venue.name).all(),
        get_label='name',
        # Remove size, add id for Select2
        render_kw={'id': 'venues_field'}
    )
    submit = SubmitField('Schedule Exam')


class EditExamForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()], render_kw={'id': 'date_field'})

    session = QuerySelectField(
        'Session',
        query_factory=lambda: Session.query.all(), # Initial query, might be updated by JS
        get_label=lambda s: f"{s.date} - {s.start_time}",
        allow_blank=False,
        render_kw={'size': 3, 'id': 'session_field'} # Keep size for non-Select2 fields if desired
    )
    exam = QuerySelectField(
        'Exam',
        query_factory=lambda: Exam.query.all(), # Initial query, might be updated by JS
        get_label='course_id',
        allow_blank=False,
        render_kw={'size': 3, 'id': 'exam_field'} # Keep size for non-Select2 fields if desired
    )
    submit = SubmitField('Edit Exam')


class AllowanceForm(FlaskForm):
    Category = QuerySelectField(
        'Staff Category',
        query_factory=lambda: Category.query.order_by(Category.id).all(),
        get_label='name',
        validators=[DataRequired()],
        allow_blank=False,
        render_kw={'size': 3}
    )
    rate = FloatField("Rate", validators=[DataRequired()], render_kw={"placeholder": "Enter an amount"})
    submit = SubmitField('Set Rate')


class SessionForm(FlaskForm):
    #name = StringField('Session Name', validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()], format='%Y-%m-%d')

    session_number = QuerySelectField(
        'Session Number',
        query_factory=lambda: SessionNumber.query.order_by(SessionNumber.id).all(),
        get_label='name',
        validators=[DataRequired()],
        allow_blank=False,
        render_kw={'size': 3}
    )

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
        query_factory=lambda: AcademicYear.query.order_by(desc(AcademicYear.id)).all(),
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
        render_kw={'size': 2}
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
    session = QuerySelectField(
        'Session',
        query_factory=lambda: Session.query.all(),
        get_label="date",
        allow_blank=False,
        description='Select the session for this schedule.'
    )

    # Define a query factory that filters venues based on the selected session
    def get_venues():
        # Default empty query if no session selected or in initial form state
        if not getattr(request, 'form', None) or 'session' not in request.form:
            return Venue.query.filter(Venue.id == None)  # Empty result
        
        session_id = int(request.form.get('session'))
        # Get all exams for this session
        exams = Exam.query.filter_by(session_id=session_id).all()
        
        # Collect venue IDs from all exams in this session
        venue_ids = set()
        for exam in exams:
            for venue in exam.venues:
                venue_ids.add(venue.id)
        
        # Query all venues with these IDs
        return Venue.query.filter(Venue.id.in_(venue_ids)).all() if venue_ids else []

    venues = QuerySelectMultipleField(
        'Venues',
        query_factory=get_venues,
        get_label='name',
        allow_blank=True,
        description='Select venue(s) for this schedule.',
        render_kw={
            'class': 'inline-field',
            'style': 'display: inline-block; width: 45%; margin-right: 5%;'
        }
    )

    staff = QuerySelectMultipleField(
        'Assign Staff',
        query_factory=lambda: User.query.filter(User.role == 'Biometric Staff - IT').all(),
        get_label=lambda user: f"{user.first_name} {user.surname}",
        allow_blank=True,
        description='Select one or more staff members to assign.',
        render_kw={
            'class': 'inline-field',
            'style': 'display: inline-block; width: 45%;'
        }
    )

    submit = SubmitField('Save Schedule')



class VenueStaffForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        # Extract the index from kwargs before calling super
        self.index = kwargs.pop('index', None)
        super(VenueStaffForm, self).__init__(*args, **kwargs)
        
        # Set dynamic labels using the index if provided
        if self.index is not None:
            self.venue.label.text = f'Venue {self.index}'
            self.staff.label.text = f'Staff {self.index}'

    venue = QuerySelectField(
        'Venue',  # Default label
        query_factory=lambda: Venue.query.all(),  # Added this line to fix the error
        get_label='name',
        allow_blank=True,
        render_kw={'class': 'form-control venue-field'}
    )
    staff = QuerySelectField(
        'Staff',  # Default label
        query_factory=lambda: User.query.filter(User.role == 'Biometric Staff - IT').all(),
        get_label=lambda user: f"{user.first_name} {user.surname}",
        allow_blank=True,
        render_kw={'class': 'form-control'}
    )



class BiometricScheduleForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], render_kw={'id': 'date'})
    session = QuerySelectField(
        'Select Session',
        query_factory=lambda: Session.query.all(),
        get_label=lambda s: f"{s.date} - {s.start_time}",  # Adjust based on the field you want to display
        allow_blank=False,
        validators=[DataRequired()],
        render_kw={'size': 3, 'id': 'session'}
    )
    submit = SubmitField('Save Schedule')



class CourseForm(FlaskForm):
    course_code = StringField('Course Code', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Submit')



class AttendanceForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()], render_kw={'id': 'date_field'})

    # Provide a default callable for the session field
    session = QuerySelectField(
        'Session',
        query_factory=lambda: Session.query.all(),
        get_label=lambda s: f"{s.session_number.name} - {s.start_time}",
        allow_blank=False,
        render_kw={'size': 3, 'id': 'session_field'}
    )


    venues = QuerySelectField(
        'Venue',
        query_factory=lambda: Venue.query.order_by(Venue.name).all(),
        get_label='name',
        render_kw={'size': 3, 'id': 'venues_field'}
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
            self.session.query_factory = lambda: Session.query.filter(
                db.func.date(Session.date) == selected_date
            ).all()
        else:
            self.session.query_factory = lambda: Session.query.all()



class SessionFilterForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    session = QuerySelectField(
        'Session',
        query_factory=lambda: Session.query.all(),
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



