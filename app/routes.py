from flask import Blueprint, Flask, render_template, redirect, url_for, flash, request, session, jsonify, abort, make_response, current_app, send_file
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
from app.forms import *
from app.models import *
from app.data import *
from app import db
from flask_bootstrap import Bootstrap5
from sqlalchemy import func, or_, case, desc, distinct
from sqlalchemy.exc import IntegrityError
import pdfkit
from io import BytesIO
import pandas as pd
import os
import pandas as pd



bp = Blueprint('main', __name__)


UPLOAD_FOLDER = 'app/static/uploads'



############################
##### PREREQUISITES #####



@bp.route('/programmes/create', methods=['GET', 'POST'])
def create_programmes():
    for i in ksb_programmes:
        if not Programme.query.filter_by(name=i['name']).first():
            db.session.add(
                Programme(
                    name=i['name'],
                    year_group=i['year']
                )
            )
    db.session.commit()
    return redirect(url_for('main.home'))
    #return 0


@bp.route('/departments/create', methods=['GET', 'POST'])
def create_departments():
    df = pd.read_excel(
        f'{UPLOAD_FOLDER}/list.xlsx',
        header=0,
        dtype={
            'title': str,
            'surname': str,
            'first_name': str,
            'department': str,
            'category': str,
            'role': str  # Ensure 'role' is read as string
        }
    )
    for index, row in df.iterrows():
        # Extract values; strip where applicable
        department_str = row['department'].strip()

        # Get Department
        if Department.query.filter_by(name=department_str).first():
            msg = flash('Departments exist!', 'danger')
            return msg    
            
        else:
            db.session.add(Department(name=department_str))
            db.session.commit()
    msg = flash('Departments created', 'success')       
    return msg     


# Initialization functions (unchanged)

#@bp.route('/graduate-type/create', methods=['GET', 'POST'])
def create_graduate_type(data=graduate_types):
    for key,val in data.items():
        val=val.strip()
        if not GraduateType.query.filter_by(name=val).first():
            db.session.add(
                GraduateType(
                    name=val,
                initials=key
                )
            )
    db.session.commit()


def create_venues():
    for i in rooms:
        if not Venue.query.filter_by(name=i).first():
            db.session.add(
                Venue(name=i)
                )
    db.session.commit()
    return 0


def create_levels(data=levels):
    for key, val in data.items():
        # Extract the single key-value pair from the nested dictionary
        year_group, level = next(iter(val.items()))
        if not Level.query.filter_by(year=key).first():
            db.session.add(
                Level(
                    year=key,
                    year_group=year_group,
                    level=level
                )
            )
    db.session.commit()


def create_categories(data=staff_categories):
    for i in data:
        if not Category.query.filter_by(name=i).first():
            db.session.add(Category(name=i))
    db.session.commit()


def create_semesters(data=semester_data):
    for i in data['semesters']:
        if not Semester.query.filter_by(semester=i).first():
            db.session.add(Semester(semester=i))
    for j in data['exam_types']:
        if not ExamType.query.filter_by(exam_type=j).first():
            db.session.add(ExamType(exam_type=j))
    db.session.commit()


def create_titles(data=staff_titles):
    for i in data:
        if not Title.query.filter_by(title=i.strip()).first():
            db.session.add(Title(title=i.strip()))
    db.session.commit()


def populate_cohss_programmes(data=cohss_programmes):
    """
    Given a nested dict of the form:
      { college_name: { faculty_name: { department_name: [programme_names] } } }
    this function will create any missing College, Faculty, Department and Programme
    objects in the database.
    """
    for college_name, faculties in data.items():
        # 1) get or create College
        college = College.query.filter_by(name=college_name).first()
        if not college:
            college = College(name=college_name)
            db.session.add(college)
            db.session.flush()  # assign college.id

        for faculty_name, departments in faculties.items():
            # 2) get or create Faculty under that College
            faculty = (
                Faculty.query
                       .filter_by(name=faculty_name, college_id=college.id)
                       .first()
            )
            if not faculty:
                faculty = Faculty(name=faculty_name, college_id=college.id)
                db.session.add(faculty)
                db.session.flush()

            for department_name, programmes in departments.items():
                # 3) get or create Department under that Faculty
                department = (
                    Department.query
                              .filter_by(name=department_name, faculty_id=faculty.id)
                              .first()
                )
                if not department:
                    department = Department(
                        name=department_name,
                        faculty_id=faculty.id
                    )
                    db.session.add(department)
                    db.session.flush()

                for prog_name in programmes:
                    # 4) get or create Programme under that Department
                    prog = (
                        Programme.query
                                 .filter_by(name=prog_name, department_id=department.id)
                                 .first()
                    )
                    if not prog:
                        prog = Programme(
                            name=prog_name,
                            department_id=department.id
                        )
                        db.session.add(prog)

    # commit everything once at the end
    db.session.commit()

@bp.route('/session-numbers/create', methods=['GET', 'POST'])
def create_session_numbers():
    for i in range(1,7):
        if not SessionNumber.query.filter_by(number=i).first():
            db.session.add(
                SessionNumber(
                    number=int(i),
                    name=f"Session {i}"
                )
            )
    db.session.commit()
    return redirect(url_for('main.home'))


@bp.route('/create-prerequisites', methods=['GET', 'POST'])
@login_required
def create_prerequisites():
    create_categories()
    create_titles()
    create_semesters()
    populate_cohss_programmes()
    create_courses()
    create_graduate_type()
    create_levels()
    #create_users()
    create_venues()
    return redirect(url_for('main.home'))



###########################
####   SESSION MANAGER ####

@bp.before_request  # Use before_request to apply to the entire app
def session_management():
    session.permanent = True  # Set the session as permanent
    session.modified = True   # Update session with each request

    # If the user is logged in, check session expiry
    if current_user.is_authenticated:
        if 'last_activity' in session:
            # Ensure last_activity is timezone-aware
            last_activity = session['last_activity'].replace(tzinfo=datetime.now().tzinfo)
            idle_time = timedelta(minutes=30)  # Idle time limit
            if datetime.now() - last_activity > idle_time:
                # If idle time exceeded, log out user and clear session
                logout_user()
                session.clear()
                return redirect(url_for('main.login'))  # Redirect to login page

        # Update last activity time if session is still active
        session['last_activity'] = datetime.now()  # This will be timezone-aware


########################
## ===== ROUTES ===== ##
########################

@bp.route('/')
def home():
    if not User.query.all():
        return redirect(url_for('main.create_admin'))
    return render_template('home.html', title='Home')


@bp.route('/admin')
def admin():
    # Get total staff count
    total_staff = len([st for st in User.query.all()])
    
    # Get all table names and their records
    inspector = db.inspect(db.engine)
    table_names = inspector.get_table_names()
    
    # Create a dictionary to store table data
    table_data = {}
    
    # Get records for each table
    for table_name in table_names:
        # Skip SQLAlchemy internal tables
        if table_name.startswith('_') or table_name.startswith('alembic'):
            continue
            
        # Get the model class for the table
        model_class = next((m for m in db.Model.__subclasses__() 
                          if m.__tablename__ == table_name), None)
        
        if model_class:
            # Query all records from the table
            records = model_class.query.all()
            table_data[table_name] = records
    
    return render_template('admin_panel.html', 
        title='Admin', 
        total_staff=total_staff,
        table_names=table_names,
        table_data=table_data
    )


@bp.route('/admin-panel')
@login_required
def admin_panel():
    # Get total staff count
    total_staff = len([st for st in User.query.all()])
    academic_years = AcademicYear.query.order_by(AcademicYear.id).all()
    ac_years = len(academic_years)
    # Get all staff first
    all_staff = User.query.all()
    
    # Sort them based on title
    def title_key(user):
        if not user.title:
            return 4, user.id   
        title_text = user.title.title  # Access the title attribute of the title object
        if 'Prof' in title_text:
            return 1, user.id
        elif 'Dr' in title_text:
            return 2, user.id
        else:
            return 3, user.id
    staff = sorted(all_staff, key=title_key)
    sessions = Session.query.order_by(Session.id).all()
    total_sessions = len(sessions)
    depts = Department.query.all()
    total_depts = len(depts)
    programmes = Programme.query.order_by(Programme.name).all()
    total_progs = len(programmes)
    return render_template('admin.html', title='Admin Panel', total_staff=total_staff, ac_years=ac_years, total_sessions=total_sessions,
                           academic_years=academic_years, staff=staff, sessions=sessions, depts=depts, total_depts=total_depts, programmes=programmes,
                           total_progs=total_progs)



# ##########################
####### USERS ##############
@bp.route('/admin/create', methods=['GET', 'POST'])
@login_required
def create_admin():
    form = AdminUserForm()
    if form.validate_on_submit():
        title      = form.title.data.strip()
        surname    = form.surname.data.upper()
        first_name = form.first_name.data.strip()
        email      = form.email.data.strip()
        phone      = form.phone.data.strip()
        department = form.department.data.strip()
        category   = form.category.data.strip()
        # ensure Department exists
        if not Department.query.filter_by(name=department).first():
            db.session.add( Department(name=department) )
            db.session.commit()

        # ensure Title exists
        if not Title.query.filter_by(title=title).first():
            db.session.add( Title(title=title) )
            db.session.commit()
        # ensure Category exists
        if not Category.query.filter_by(name=category).first():
            db.session.add( Category(name=category) )
            db.session.commit()
        # now create the User
        if not User.query.filter_by(email=email).first():
            title_id    = Title.query.filter_by(title=title).first().id
            category_id = Category.query.filter_by(name=category).first().id
            dept_id     = Department.query.filter_by(name=department).first().id

            if dept_id and title_id and category_id:
                try:
                    new_admin = User(
                        title_id      = title_id,
                        surname       = surname,
                        first_name    = first_name,
                        email         = email,
                        phone         = phone,
                        category_id   = category_id,
                        department_id = dept_id,
                        is_admin      = True,
                        is_manager    = True,
                        password      = generate_password_hash(
                            form.password.data,
                            method='scrypt',
                            salt_length=8
                        )
                    )
                    db.session.add(new_admin)
                    db.session.commit()
                    flash('Admin user created.', 'success')
                    return redirect(url_for('main.home'))
                except Exception as e:
                    db.session.rollback()
                    flash(f"Error: {e}", 'danger')
            else:
                flash('Either title, department or category does not exist', 'danger')
    return render_template('signup.html', form=form, title='Create Admin', heading='Create Admin Account')



@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(surname=form.surname.data.upper(), first_name=form.first_name.data).first():
            flash("User exists!", 'warning')
            return redirect(url_for('main.login'))
        passwd_hash = generate_password_hash(form.password.data, method='scrypt', salt_length=8)
        #print(form.category.data.id)
        is_admin = False
        if form.email.data in managers:
            is_admin = True

        new_user = User(
            title_id=form.title.data.id,
            surname=form.surname.data.upper(),
            first_name=form.first_name.data,
            email=form.email.data,
            password=passwd_hash,
            phone_number=form.phone.data,
            category_id=form.category.data.id,
            department_id=form.department.data.id,
            is_admin=is_admin
        )
        db.session.add(new_user)
        db.session.commit()
        flash(f'User {form.email.data} created.', 'success')
        return redirect(url_for('main.login'))
    return render_template('signup.html', title='Sign Up', heading='Register', form=form)



@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash(f'User with account "{form.email.data}" does not exist', 'info')
            return redirect(url_for('main.login'))
        if check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
    return render_template('signin.html', form=form, title='Login', heading='Login')



@bp.route('/logout')
@login_required
def logout():
    logout_user()  # This is enough to log the user out
    session.clear()  # Clears the session data safely
    return redirect(url_for('main.home'))



@bp.route('/user/add', methods=['GET', 'POST'])
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        surname = form.surname.data
        first_name = form.first_name.data
        if User.query.filter_by(surname=surname.upper(), first_name=first_name).first():
            flash("User exists!", 'warning')
            return redirect(url_for('main.login'))
        db.session.add(
            User(
                title_id=form.title.data.id,
                surname=surname.upper(),
                first_name=first_name,
                category_id=form.category.data.id,
                department_id=form.department.data.id
            )
        )
        #print(f"{form.category.data.id} {form.surname.data}")
        db.session.commit()
        return redirect(url_for('main.staff_attendance'))
    return render_template('login.html', form=form, title='Add User', heading='Add User')


"""
@bp.route('/user/create', methods=['GET', 'POST'])
def create_user():
    form=UserForm()
    if form.validate_on_submit():
        pass
    return render_template('add_user.html', title='Create User', heading='Create User', form=form)

"""


@bp.route('/users/create', methods=['GET', 'POST'])
def create_users():
    
    for i in staff_list:
        # Extract values; strip where applicable
        title_str = i['title']
        surname = i['surname'].strip()
        first_name = i['first_name'].strip()
        department_str = i['department'].strip()
        staff_category_str = i['category'].strip()
        role = i["role"]
        #print(f"{title_str} \n{surname} \n{first_name} \n{department_str} \n{staff_category_str}")

        # Skip creating user if already exists
        if User.query.filter_by(surname=surname.upper(), first_name=first_name).first():
            #flash(f"User {first_name} {surname} already exists!", "warning")
            continue

        # Get Category
        if not Category.query.filter_by(name=staff_category_str).first():
            db.session.add(
                Category(name=staff_category_str)
            )
            db.session.commit()

        # Get Department
        if not Department.query.filter_by(name=department_str).first():
            db.session.add(
                Department(name=department_str)
            )
            db.session.commit()

        if not Title.query.filter_by(title=title_str).first():
            db.session.add(
                Title(title=title_str)
            )
            db.session.commit()

        title_obj = Title.query.filter_by(title=title_str).first()
        dept_obj = Department.query.filter_by(name=department_str).first()
        cat_obj = Category.query.filter_by(name=staff_category_str).first()
            
        new_user = User(
            title_id=title_obj.id,
            surname=surname.upper(),
            first_name=first_name,
            department_id=dept_obj.id,
            category_id=cat_obj.id,
            role=role
        )
        db.session.add(new_user)

    # Commit all changes after processing the file
    db.session.commit()
    flash("Users created successfully!", "success")
    return redirect(url_for('main.home'))
  

@bp.route('/users/view', methods=['GET', 'POST'])
def get_users(): 
    staff = User.query.order_by(
        User.surname
        ).all()
    return render_template('all_staff.html', title='View Users', heading='Staff List', staff=staff)


@bp.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    form = UserForm()
    user = User.query.get_or_404(user_id)

    if request.method == 'GET':
        form.title.data = user.title
        form.surname.data = user.surname
        form.first_name.data = user.first_name
        form.department.data = user.department
        form.category.data = user.category

    if form.validate_on_submit():
        user.title_id = form.title.data.id
        user.surname = form.surname.data
        user.first_name = form.first_name.data
        user.department_id = form.department.data.id
        user.category_id = form.category.data.id

        db.session.commit()
        return redirect(url_for('main.get_users'))

    return render_template('add_user.html', title='Edit User', heading='Edit User', form=form)


@bp.route('/user/delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if not user:
        msg = flash('User not found!', 'danger')
        return f"Error: {msg}"
    if current_user.id == 1 or current_user.is_admin:
        try:
            db.session.delete(user)
            db.session.commit()
            msg = flash('User deleted', 'sucess')
            return f"Success: {msg}"
        except Exception as e:
            msg = flash('Error: {e}', 'danger')
            return msg
    else:
        return flash('User unauthorized to perform this action', 'info')


@bp.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    users = User.query.order_by(User.surname, User.first_name).all()
    titles = Title.query.all()
    return render_template('attendance_report.html', users=users, titles=titles)


@bp.route('/attendance/', methods=['GET', 'POST'])
def view_attendance():
    users = User.query.order_by(User.surname, User.first_name).all()
    titles = Title.query.all()
    return render_template('attendance_report.html', users=users, titles=titles)



##############################
######### DEPARTMENT #########

@bp.route('/department/add', methods=['GET', 'POST'])
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        if Department.query.filter_by(name=form.name.data).first():
            flash("Department exists!", 'info')
            return redirect(url_for('main.register'))
        db.session.add(
            Department(name=form.name.data)
        )
        db.session.commit()
        return redirect(url_for('main.register'))
    return render_template('register.html', form=form)


@bp.route('/report/')
def report():
    session_id = request.args.get('session_id')
    if not session_id:
        # Handle the error: either flash a message or abort with 404
        flash("Session ID is missing", "danger")
        return redirect(url_for('main.home'))
    session = Session.query.get_or_404(session_id)
    attendances = Attendance.query.filter_by(session_id=session_id).all()
    return render_template('report.html', session=session, attendances=attendances)


@bp.route('/academic-year/create', methods=['GET', 'POST'])
def create_academic_year():
    form = AcademicYearForm()
    if form.validate_on_submit():
        if not AcademicYear.query.filter_by(year=form.year.data).first():
            db.session.add(
                AcademicYear(year=form.year.data,
                             start_year=form.start_year.data,
                             end_year=form.end_year.data,)
            )
            db.session.commit()
            flash(f'{form.year.data} created.', 'success')
            return redirect(url_for('main.home'))
        else:
            flash(f'{form.year.data} exists!.', 'info')
            return redirect(url_for('main.home'))
    return render_template('narrow_form.html', title='Create Year', heading='Create Academic Year', form=form)



##############################
########## EXAMS ###########

@bp.route('/exam/create-exam', methods=['GET', 'POST'])
def create_exam():
    form = ExamForm()
    if form.validate_on_submit():
        level_id=form.level.data.id
        session_id=form.session.data.id
        course_id=form.course.data.id
        selected_prog_ids = [p.id for p in form.programmes.data]
        
        exam = (
            Exam.query
                .filter(Exam.course_id == course_id,
                        Exam.programmes.any(Programme.id.in_(selected_prog_ids))
                )
                .first()
        )
        if not exam:
            try:
                exam = Exam(
                    level_id=level_id,
                    session_id=session_id,
                    course_id=course_id
                )
                # Since QuerySelectMultipleField returns objects, no need to query again
                for programme in form.programmes.data:
                    exam.programmes.append(programme)
                for venue in form.venues.data:
                    exam.venues.append(venue)
                    
                db.session.add(exam)
                db.session.commit()
                flash('Exam Scheduled', 'success')
                return redirect(url_for('main.home'))
            except Exception as e:
                flash(f"Error occurred: {e}", 'danger')
                return redirect(url_for('main.home'))
    return render_template('schedule_exam.html', form=form, title='Schedule Exam', heading='Create Exam')


@bp.route('/exams/view', methods=['GET', 'POST'])
def view_exams():
    exams = Exam.query.all()
    return render_template('view_exams.html', title='View Exams', heading='View Exams', exams=exams)


@bp.route('/exam/select-date', methods=['GET', 'POST'])
def exam_date_view():
    form = DateForm()
    if form.validate_on_submit():
        date = form.date.data
        return redirect(url_for('main.view_daily_exams', date=date))
    return render_template('narrow_form.html', title='Select Date', heading='Select Date', form=form)


@bp.route('/exams/daily-view', methods=['GET'])
def view_daily_exams():
    date_str = request.args.get('date', '').strip()
    exams = []
    selected_date = None
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'warning')
            return redirect(url_for('main.view_daily_exams'))
        # Option A: join Session and filter
        exams = (
            Exam.query
                .join(Session)
                .filter(Session.date == selected_date)
                .order_by(Session.session_number_id)
                .all()
            )
    return render_template('view_exams.html', title='View Exams', heading='View Exams', exams=exams, selected_date=selected_date)


@bp.route('/exam/get-exam', methods=['GET', 'POST'])
def get_exam_to_edit():
    form = EditExamForm()
    if form.validate_on_submit():
        exam_id = form.exam.data.id
        return redirect(url_for('main.edit_exam', exam_id=exam_id))
    return render_template('edit_exam.html', title='Edit Exam', heading='Get Exam' ,form=form)


@bp.route('/exam/edit/<int:exam_id>', methods=['GET', 'POST'])
def edit_exam(exam_id):
    form = ExamForm()
    exam = Exam.query.get_or_404(exam_id)
    if not exam:
        flash('Exam not found!', 'info')
        return redirect(url_for('main.home'))
    # Populate form with data
    form.level.data = exam.level
    form.date.data = exam.session.date
    form.session.data = exam.session
    form.course.data = exam.course

    if form.validate_on_submit():
        try:
            exam.level_id = form.level.data.id
            exam.session_id = form.session.data.id
            exam.course_id = form.course.data.id

            # Clear existing many-to-many relationships
            exam.programmes.clear()
            exam.venues.clear()

            # Add updated selections
            for prog in form.programmes.data:
                exam.programmes.append(prog)
            for venue in form.venues.data:
                exam.venues.append(venue)

            db.session.add(exam)
            db.session.commit()
            flash('Exam Scheduled', 'success')
            return redirect(url_for('main.home'))
        except Exception as e:
            flash(f"Error occurred: {e}", 'danger')
            return redirect(url_for('main.home'))
    return render_template('schedule_exam.html', title='Create Schedule', heading='Create Schedule', form=form)



@bp.route('/exam/delete/<int:exam_id>', methods=['GET', 'POST'])
def delete_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    if not exam:
        msg = flash('Exam not found!', 'info')
        return f"Error: {msg}"
    try:
        # clear out old programmes & venues
        exam.programmes.clear()
        exam.venues.clear()
        # delete exam instance
        db.session.delete(exam)
        db.session.commit()
        flash('Exam deleted!', 'success')
        return redirect(url_for('main.home'))
    except Exception as e:
        flash(f"Error occurred: {e}", 'danger')
        return redirect(url_for('main.home'))


#############################
########## COURSES ##########

@bp.route('/course/create', methods=['GET', 'POST'])
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        course_code = form.course_code.data.strip()
        title = form.title.data.strip().upper()
        if not Course.query.filter_by(course_code=course_code).first():
            db.session.add(
                Course(
                    course_code=course_code,
                    title=title
                )
            )
        db.session.commit()
        flash(f"{course_code} successfully created.", 'success')
        return redirect(url_for('main.create_exam'))
    return render_template('login.html', title='Create Course', heading='Create Course', form=form)


@bp.route('/course/edit/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    # 1. Fetch the course or 404
    course = Course.query.get_or_404(course_id)

    # 2. Instantiate the form, pre-populating from the model
    form = CourseForm(obj=course)

    if form.validate_on_submit():
        # Strip/uppercase incoming values
        new_code = form.course_code.data.strip()
        new_title = form.title.data.strip().upper()

        # 3. Ensure no other course already uses this code
        duplicate = Course.query.filter(
            Course.course_code == new_code,
            #Course.id != course.id
        ).first()
        if duplicate:
            flash(f"Course code {new_code} is already in use.", 'warning')
        else:
            # Update and commit
            course.course_code = new_code
            course.title       = new_title
            db.session.commit()
            flash(f"{new_code} successfully updated.", 'success')
            return redirect(url_for('main.create_exam'))
    return render_template('login.html', title='Create Course', heading='Create Course', form=form)
    

@bp.route('/course/delete/<int:course_id>', methods=['GET', 'POST'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    try:
        db.session.delete(course)
        db.session.commit()
        msg = flash('Course deleted successfully', 'success')
        return f"{msg}"
    except Exception as e:
       return f"Error occurred: {e}"


@bp.route('/courses/create', methods=['GET', 'POST'])
def create_courses():
    data = cohss_courses
    for key,val in data.items():
        course_code = key.strip()
        title = val.strip()
        # print(course_code)
        if not Course.query.filter_by(course_code=course_code).first():
            new_course = Course(
                course_code=course_code,
                title=title
            )
            db.session.add(new_course)

    db.session.commit() # Commit all new courses after the loop
    flash('CoHSS courses created successfully.', 'success') # Optional: Add a success message
    return redirect(url_for('main.home'))


#############################
########## TITLES ##########

@bp.route('/user-title/create', methods=['GET', 'POST'])
@login_required
def create_title():
    form = TitleForm()
    if form.validate_on_submit():
        title = form.title.data
        if not Title.query.filter_by(title=title).first():
            db.session.add(
                Title(title=title)
            )
            db.session.commit()
            flash('Title created.', 'success')
            return redirect(url_for('main.home'))
    return render_template('narrow_form.html', title='Create Title', heading='Create Title', form=form)


@bp.route('/user-title/edit/<int:title_id>', methods=['GET', 'POST'])
@login_required
def edit_title(title_id):
    title = Title.query.get_or_404(title_id)
    form = TitleForm()
    if form.validate_on_submit():
        title.title = form.title.data
        db.session.commit()
        flash('Changes saved.', 'success')
        return redirect(url_for('main.home'))
    return render_template('narrow_form.html', title='Create Title', heading='Create Title', form=form)


@bp.route('/user-title/delete/<int:title_id>', methods=['POST'])
@login_required
def delete_title(title_id):
    # This will abort(404) if not found
    title = Title.query.get_or_404(title_id)
    try:
        db.session.delete(title)
        db.session.commit()
        flash('Title deleted.', 'success')

    except IntegrityError:
        db.session.rollback()
        flash('Cannot delete this title because it is still in use.', 'warning')

    except Exception as e:
        db.session.rollback()
        flash(f'Unexpected error: {e}', 'danger')

    # Always redirect after a POST
    return 0 # redirect(url_for('main.home'))


################################
########## SESSION #############

@bp.route('/session/create', methods=['GET', 'POST'])
def create_session():
    form = SessionForm()
    if form.validate_on_submit():
        session_number_id = form.session_number.data.id
        date = form.date.data
        academic_year_id = form.academic_year.data.id
        semester_id = form.semester.data.id
        exam_type_id = form.exam_type.data.id
        start_time = form.start_time.data#.strftime('%H:%M')
        end_time = form.end_time.data#.strftime('%H:%M')
        print(f"{start_time} -- {end_time}")
        if not Session.query.filter_by(session_number_id=session_number_id, date=date).first():
            db.session.add(
                Session(
                    session_number_id=session_number_id, date=date, academic_year_id=academic_year_id,
                    semester_id=semester_id, exam_type_id=exam_type_id, 
                    start_time=start_time, end_time=end_time        
                )
            )
            db.session.commit()
            flash('Session created successfully.', 'success')

    return render_template('narrow_form.html', title='Create Session', heading="Create Session", form=form)


@bp.route('/sessions/create', methods=['GET', 'POST'])
def create_sessions():
    return redirect(url_for('main.home'))


@bp.route('/session/view', methods=['GET', 'POST'])
def view_exam_session():
    form = DateForm()
    sessions = Session.query.order_by(Session.id).all()
    return render_template('narrow_form.html', title='Choose', heading="Choose Date", form=form,)


@bp.route('/session/delete/<int:session_id>', methods=['GET', 'POST'])
@login_required
def delete_exam_session(session_id):
    session = Session.query.get(session_id)
    if current_user.id == 1 or current_user.is_admin:
        try:
            db.session.delete(session)
            db.session.commit()
            msg = flash('Session deleted', 'success')
            return f"{msg}"
        except Exception as e:
            flash(f'An error occuured: {e}', 'danger')
            return redirect(url_for('main.home'))
    else:
        flash(f'User unauthorized to perform this action', 'danger')
        return redirect(url_for('main.home'))


@bp.route('/sessions/daily')
def daily_exam_sessions():
    form = DateForm()
    return render_template('narrow_form.html', title='Choose', heading="Choose Date", form=form,)


@bp.route('/session/edit/<int:session_id>', methods=['GET', 'POST'])
@login_required
def edit_session(session_id):
    session = Session.query.get(session_id)
    form = Session()
    form.data.data = session.data
    form.start_time.data = session.start_time
    form.end_time.data = session.end_time
    if form.validate_on_submit():
        name = form.name.data
        date = form.date.data
        academic_year_id = form.academic_year.data.id
        semester_id = form.semester.data.id
        exam_type_id = form.exam_type.data.id
        start_time = form.start_time.data
        end_time = form.end_time.data
        if not Session.query.filter_by(name=name, date=date).first():
            db.session.add(
                Session(
                    name=name, date=date, academic_year_id=academic_year_id,
                    semester_id=semester_id , exam_type_id=exam_type_id, start_time=start_time, end_time=end_time        
                )
            )
            db.session.commit()
            flash('Session created successfully.', 'success')
            #return redirect(url_for('main.home'))
    return render_template('login.html', title='Create Session', heading="Create Session", form=form)


@bp.route('/session/delete/<int:session_id>', methods=['GET', 'POST'])
@login_required
def delete_session(session_id):
    session = Session.query.get_or_404(session_id)
    if session and (current_user.id == 1 or current_user.is_admin==True):
        try:
            db.session.delete(session)
            db.session.commit()
            flash('Session deleted.', 'success')
        except Exception as e:
            flash(f"Error occurred: {e}", 'danger')
            return redirect()
    return flash('Success', 'success')


@bp.route('/get-date-session', methods=['GET', 'POST'])
def get_date_session():
    form = DateSessionForm()
    if form.validate_on_submit():
        date = form.date.data
        session = form.session.data
        # Process form data here if needed
        return redirect(url_for('main.biometric_schedule', date=date, session_id=session.id))
    return render_template('narrow_form.html', title='Get Date Session', heading='Select Date and Session', form=form)



# --- Helper Endpoint to Get Venues for a Session ---
@bp.route('/get-venues-for-session/<int:session_id>')
def get_venues_for_session(session_id):
    """
    Returns JSON list of unique venues linked to exams within a specific session.
    """
    # Query unique Venues associated with Exams in the given Session
    venues_query = db.session.query(Venue.id, Venue.name)\
        .join(Exam.venues)\
        .filter(Exam.session_id == session_id)\
        .distinct()\
        .order_by(Venue.name) # Order venues alphabetically

    venues = venues_query.all()
    venue_list = [{'id': v_id, 'name': v_name} for v_id, v_name in venues]

    return jsonify(venues=venue_list)



# #################################
###### ATTENDANCE & SCHEDULE ######

@bp.route('/biometric-schedule', methods=['GET', 'POST'])
@login_required
def biometric_schedule():
    form = BiometricScheduleForm()
    if form.validate_on_submit():
        session_id = form.session.data.id
        staff_keys = [key for key in request.form if key.startswith('staff_')]
        for key in staff_keys:
            index = key.split('_')[1]
            staff_id = request.form.get(key)
            venue_id = request.form.get(f'venue_{index}')
            if staff_id and venue_id:
                biometric = Biometric(session_id=session_id, user_id=staff_id, venue_id=venue_id)
                db.session.add(biometric)
        db.session.commit()
        flash('Biometric schedule saved successfully.')
        return redirect(url_for('main.biometric_schedule'))
    return render_template('schedule_staff.html', title='Biometric Schedule', heading='Create Biometric Schedule', form=form)


@bp.route('/schedule/get-session', methods=['GET', 'POST'])
def get_schedule_sessions():
    form = DateSessionForm()
    if form.validate_on_submit():
        session_id = form.session.data.id
        return redirect(url_for('main.view_schedule', session_id=session_id))
    return render_template('narrow_form.html', title='Get Session', heading='Get Session', form=form)


@bp.route('/schedule/view/<int:session_id>', methods=['GET', 'POST'])
def view_schedule(session_id):
    session = Session.query.get_or_404(session_id)
    if not session:
        flash('Session not found.', 'info')
        return redirect(url_for('main.get_schedule_sessions'))
    schedule = Biometric.query.filter_by(session_id=session.id).all()
    return render_template('view_schedule.html', schedule=schedule, date=session.date, session=session, heading=f"Schedule for {session.date} - {session.session_number.name}")


@bp.route('/staff/take-attendance', methods=['GET', 'POST'])
@login_required
def staff_attendance():
    selected_date = request.args.get('date')
    form = AttendanceForm(selected_date=selected_date)

    # Detect AJAX
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    # Handle POST
    if request.method == 'POST':
        # If form validates, record attendance
        if form.validate_on_submit():
            date       = form.date.data
            session_id = form.session.data.id
            venue_id   = form.venues.data.id
            staff_id   = int(form.staff_id.data)

            try:
                exists = Attendance.query.filter_by(
                    session_id=session_id,
                    user_id=staff_id
                ).first()

                if not exists:
                    user = User.query.get(staff_id)
                    attendance = Attendance(
                        session_id=session_id,
                        user_id=staff_id,
                        timestamp=datetime.utcnow(),
                        venue_id=venue_id
                    )
                    user.session_count += 1
                    db.session.add(attendance)
                    db.session.commit()

                    msg, status = 'Attendance recorded successfully!', 'success'
                else:
                    msg, status = 'Attendance record already exists.', 'warning'

            except Exception as e:
                db.session.rollback()
                msg, status = f'Error: {e}', 'danger'

            # AJAX → JSON response
            if is_ajax:
                return jsonify({ 'status': status, 'message': msg }), 200

            # Non-AJAX → flash + redirect
            flash(msg, status)
            return redirect(
                url_for('main.staff_attendance',
                        date=date.strftime('%Y-%m-%d'))
            )

        else:
            # POST but validation failed
            if is_ajax:
                # you can include form.errors if you like
                return jsonify({
                    'status': 'danger',
                    'message': 'Validation error',
                    'errors': form.errors
                }), 400

    # GET (or non‐AJAX POST that fell through) → render form
    return render_template(
        'staff_attendance.html',
        title='Take Attendance',
        heading='Attendance',
        form=form
    )



@bp.route('/attendance/transfer', methods=['GET', 'POST'])
@login_required
def transfer_attendance():
    form = AttendanceTransferForm()
    if form.validate_on_submit():
        # get IDs from the hidden fields
        transfer_id  = int(form.transfer_staff_id.data)
        receive_id   = int(form.receiving_staff_id.data)

        # 1) Move each attendance row
        attendances = Attendance.query.filter_by(user_id=transfer_id).all()
        for att in attendances:
            # create new for the receiving user
            new_att = Attendance(
                user_id   = receive_id,
                session_id= att.session_id,
                venue_id  = att.venue_id,
                timestamp = att.timestamp
            )
            db.session.add(new_att)
            # delete the old record
            db.session.delete(att)

        # 2) Delete the “transfer” user altogether
        user_to_remove = User.query.get(transfer_id)
        if user_to_remove:
            db.session.delete(user_to_remove)

        # 3) Commit once
        db.session.commit()
        flash('Attendance records moved and user deleted successfully.', 'success')
        return redirect(url_for('main.attendance_summary'))  # or wherever makes sense

    return render_template(
        'attendance_transfer.html',
        title='Transfer Attendance',
        form=form
    )


@bp.route('/attendance/broadsheet')
@login_required
def attendance_broadsheet():
    # 1) Parse the date filter as before
    date_str = request.args.get('date')
    selected_date = None
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = None

    # 2) Get all sessions for that date (distinct)
    sessions_q = Session.query
    if selected_date:
        sessions_q = sessions_q.filter(Session.date == selected_date)
    sessions = sessions_q.order_by(Session.date).all()

    # 3) Fetch all attendance records for that same date
    attend_q = Attendance.query.join(Session)
    if selected_date:
        attend_q = attend_q.filter(Session.date == selected_date)
    attendance = attend_q.all()

    # 4) Fetch staff
    staff = User.query.outerjoin(Attendance).order_by(User.surname).all()

    return render_template(
        'broadsheet.html',
        title='Attendance Broadsheet',
        heading='Attendance Broadsheet',
        sessions=sessions,        # <-- pass this in
        attendance=attendance,
        staff=staff
    )



@bp.route('/attendance/broadsheet/download-excel')
@login_required
def download_broadsheet_excel():
    # 1) Parse date filter
    date_str = request.args.get('date')
    selected_date = None
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = None

    # 2) Fetch all sessions for that date (so we get *all* columns)
    session_query = Session.query
    if selected_date:
        session_query = session_query.filter(Session.date == selected_date)
    session_query = session_query.order_by(Session.start_time)
    sessions = session_query.all()

    # Build our session columns list: [(id, label), ...]
    session_cols = [
        (s.id, f"{s.date} | {s.session_number.name}")
        for s in sessions
    ]

    # 3) Fetch all attendance for that date
    att_q = Attendance.query.join(Session)
    if selected_date:
        att_q = att_q.filter(Session.date == selected_date)
    attendance = att_q.all()

    # 4) Build header row
    headers = ['#', 'Staff', 'Department', 'Category'] + [label for (_, label) in session_cols]

    # 5) Fetch staff in your desired order
    staff = User.query.outerjoin(Attendance).order_by(User.surname).all()

    # 6) Build the table rows
    rows = []
    for idx, user in enumerate(staff, start=1):
        row = [
            idx,
            f"{user.first_name} {user.surname}",
            user.department.name if user.department else '',
            user.category.name if user.category else ''
        ]
        # one column per session
        for sid, _ in session_cols:
            # check if there's an attendance record for this user & session
            present = any(
                att.session_id == sid and att.user_id == user.id
                for att in attendance
            )
            row.append('Present' if present else 'Absent')
        rows.append(row)

    # 7) Write to Excel
    df = pd.DataFrame(rows, columns=headers)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Attendance')
    output.seek(0)

    # 8) Send as attachment
    filename = f"attendance_broadsheet_{date_str or 'all'}.xlsx"
    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


@bp.route('/attendance/summary')
@login_required
def attendance_summary():
    # 1) Reset all user counts
    for u in User.query:
        u.session_count = 0
    # 2) Count distinct sessions per user in one go
    rows = (
        db.session.query(
            Attendance.user_id,
            func.count(distinct(Attendance.session_id)).label('cnt')
        )
        .group_by(Attendance.user_id)
        .all()
    )
    # 3) Apply those counts back to each User
    for user_id, cnt in rows:
        user = User.query.get(user_id)
        if user:
            user.session_count = cnt

    db.session.commit()

    latest_session = Session.query.order_by(desc(Session.id)).first()

    # 4) Render your summary
    staff = User.query.order_by(User.surname).all()
    return render_template(
        'attendance_report.html',
        title='Attendance Summary',
        staff=staff,
        session=latest_session
    )


@bp.route('/attendance/summary/it-staff')
@login_required
def it_staff_summary():
    # 1) Reset all user counts
    for u in User.query:
        u.session_count = 0
    # 2) Count distinct sessions per user in one go
    rows = (
        db.session.query(
            Attendance.user_id,
            func.count(distinct(Attendance.session_id)).label('cnt')
        )
        .group_by(Attendance.user_id)
        .all()
    )
    # 3) Apply those counts back to each User
    for user_id, cnt in rows:
        user = User.query.get(user_id)
        if user:
            user.session_count = cnt

    db.session.commit()

    latest_session = Session.query.order_by(desc(Session.id)).first()

    # 4) Render your summary
    staff = User.query.filter_by(role='Biometric Staff - IT').order_by(desc(User.session_count)).all()
    return render_template(
        'attendance_report.html',
        title='Attendance Summary',
        staff=staff,
        session=latest_session
    )


@bp.route('/session-count/clear', methods=['GET', 'POST'])
@login_required
def clear_count():
    if not User.query.all():
        flash('No sessions to clear', 'info')
        return redirect(url_for('main.home'))
    for user in User.query.all():
        user.session_count = 0
    db.session.commit()
    flash('Sessions reset successfully.', 'success')
    return redirect(url_for('main.home'))



# ######################
###### PROGRAMMES ######

@bp.route('/programme/create', methods=['GET', 'POST'])
@login_required
def create_programme():
    form = ProgrammeForm()
    if form.validate_on_submit():
        name = form.name.data
        dept_id = form.department.data.id
        if not Programme.query.filter_by(name=name).first():
            try:
                db.session.add(
                    Programme(
                        name=name, department_id=dept_id
                    )
                )
                db.session.commit()
                flash('Programme created.', 'success')
                return redirect(url_for('main.home'))
            except Exception as e:
                flash(f"Error occurred: {e}", 'danger')
                return redirect(url_for('main.home'))
    return render_template('narrow_form.html', form=form, title='Create Programme', heading='Create Programme')



# ##################################
###### DOWNLOAD PAGE CONTENT ######

@bp.route('/download-schedule.pdf/<int:session_id>')
def download_schedule_pdf(session_id):
    date_str = request.args.get('date')
    sess = Session.query.get_or_404(session_id)
    schedule_query = Biometric.query.join(Session)
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            schedule_query = schedule_query.filter(Session.date == selected_date)
        except ValueError:
            pass
    schedule = schedule_query.all()

    # Render the table-only template
    html = render_template(
        'schedule_pdf.html',
        schedule=schedule,
        heading=f"Schedule for {date_str or 'All Dates'}"
    )
    # === Windows-specific wkhtmltopdf config ===
    wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    # Generate PDF
    pdf = pdfkit.from_string(html, False, configuration=config)
    # Send as download
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    filename = f"schedule_{date_str or 'all'}.pdf"
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    return response


@bp.route('/report-summary.pdf/<int:session_id>')
def download_summary_pdf(session_id):
    session = Session.query.get_or_404(session_id)
    staff = User.query.order_by(User.surname).all()
    # Render the table-only template
    html = render_template(
        'download_summary_pdf.html',
        staff=staff,
        heading=f"ATTENDANCE REPORT FOR {session.semester.semester.upper()} | {session.academic_year.year.upper()}"
    )

    # === Windows-specific wkhtmltopdf config ===
    wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    # Generate PDF
    pdf = pdfkit.from_string(html, False, configuration=config)
    # Send as download
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    filename = f"Summary_Report_{session.semester.semester}.pdf"
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    return response


# ########################
###### STATIC PAGES ######

@bp.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html', title='Privacy Policy', heading='Privacy Policy')




# #######################
###### AJAX STUFF #######

# Route to search staff members
@bp.route('/search_staff')
def search_staff():
    query = request.args.get('q', '')
    if query:
        # Split the query into parts for more flexible searching
        parts = query.split()
        
        # Create search conditions for both first name and surname
        conditions = []
        for part in parts:
            search_term = f'%{part}%'
            conditions.append(User.first_name.ilike(search_term))
            conditions.append(User.surname.ilike(search_term))
        
        # Query with any condition matching (using OR)
        staff = User.query.filter(
            or_(*conditions)
        ).order_by(User.surname, User.first_name).limit(10).all()
        
        # Format results for autocomplete
        staff_list = [
            {'id': s.id, 'name': f"{s.surname}, {s.first_name}"}
            for s in staff
        ]
        return jsonify(staff_list)
    return jsonify([])


@bp.route('/get_sessions', methods=['GET'])
def get_sessions():
    date_str = request.args.get('date')
    if not date_str:
        return jsonify([]), 200
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    sessions = (Session.query
                      .filter(Session.date == selected_date)
                      .order_by(Session.start_time)
                      .all())
    sessions_data = []
    for s in sessions:
        sessions_data.append({
            'id': s.id,
            'date': s.date.strftime('%Y-%m-%d'),
            'start_time': s.start_time.strftime('%H:%M') if s.start_time else ''
        })
    return jsonify(sessions_data), 200


@bp.route('/get_exams', methods=['GET'])
def get_exams():
    session_id = request.args.get('session_id')
    if not session_id:
        return jsonify([]), 200

    exams = Exam.query.filter(Exam.session_id == session_id).all()
    exams_data = []
    for ex in exams:
        exams_data.append({
            'id': ex.id,
            'label': f"{ex.course.course_code} - {ex.course.title}"
        })
    return jsonify(exams_data), 200




@bp.route('/get_venues', methods=['GET'])
def get_venues():
    session_id = request.args.get('session_id')
    venues = db.session.query(Venue).join(exam_venue).join(Exam).filter(Exam.session_id == session_id).distinct().all()
    return jsonify([{'id': v.id, 'name': v.name} for v in venues])



@bp.route('/get_staff', methods=['GET'])
def get_staff():
    staff = User.query.filter_by(role='Biometric Staff - IT').all()
    return jsonify([{'id': u.id, 'name': f"{u.first_name} {u.surname}"} for u in staff])



