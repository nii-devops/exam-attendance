from flask import Blueprint, Flask, render_template, redirect, url_for, flash, get_flashed_messages, request, session, jsonify
#from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, time
from app.forms import *
from app.models import *
from app.data import *
from app import db
from flask_bootstrap import Bootstrap5
from sqlalchemy import func, or_

import os
import pandas as pd





bp = Blueprint('main', __name__)


UPLOAD_FOLDER = 'app/static/uploads'





# Routes

@bp.route('/')
def home():
    return render_template('home.html', title='Home')



@bp.route('/attendance', methods=['GET', 'POST'])
def attendance():
    users = User.query.order_by(User.surname, User.first_name).all()
    titles = Title.query.all()
    return render_template('attendance_report.html', users=users, titles=titles)



@bp.route('/attendance/', methods=['GET', 'POST'])
def view_attendance():
    users = User.query.order_by(User.surname, User.first_name).all()
    titles = Title.query.all()
    return render_template('attendance_report.html', users=users, titles=titles)


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
def register_user():
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
    session = Session.query.get_or_404(session_id)
    attendances = Attendance.query.filter_by(session_id=session_id).all()
    return render_template('report.html', session=session, attendances=attendances)



@bp.route('/get-date-session', methods=['GET', 'POST'])
def get_date_session():
    form = DateSessionForm()
    if form.validate_on_submit():
        # Process form data here if needed
        return redirect(url_for('main.staff_attendance'))
    return render_template('narrow_form.html', title='Get Date Session', heading='Select Date and Session', form=form)


@bp.route('/exam/create-exam', methods=['GET', 'POST'])
def create_exam():
    form = ExamForm()
    if form.validate_on_submit():
        exam = Exam(
            title=form.title.data,
            #date=form.date.data,
            session_id=form.session.data.id,
            course_id=form.course.data.id
        )
        # Since QuerySelectMultipleField returns objects, no need to query again
        for programme in form.programmes.data:
            exam.programmes.append(programme)
        for venue in form.venues.data:
            exam.venues.append(venue)
            
        db.session.add(exam)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('create_exam.html', form=form, title='Schedule Exam', heading='Create Exam')



@bp.route('/exams/view', methods=['GET', 'POST'])
def view_exams():
    exams = Exam.query.all()
    return render_template('view_exams.html', title='View Exams', heading='View Exams', exams=exams)



@bp.route('/exam/edit/<int:exam_id>', methods=['GET', 'POST'])
def edit_exam(exam_id):
    form = ExamForm()
    exam = Exam.query.get_or_404(exam_id)
    if not exam:
        flash('Exam not found!', 'info')
        return redirect(url_for('main.view_exams'))
    
    # Populate form with data
    form.title.data = exam.title
    form.date.data = exam.date
    form.session.data = exam.session_id
    form.course.data = exam.course_id

    if form.validate_on_submit():
        exam = Exam(
            title=form.title.data,
            date=form.date.data,
            session_id=form.session.data,
            course_id=form.course.data
        )
        for programme_id in form.programmes.data:
            programme = Programme.query.get(programme_id)
            exam.programmes.append(programme)
        for venue_id in form.venues.data:
            venue = Venue.query.get(venue_id)
            exam.venues.append(venue)
        db.session.add(exam)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('form.html', title='Create Schedule', heading='Create Schedule', form=form)



@bp.route('/exam/delete/<int:exam_id>', methods=['GET', 'POST'])
def delete_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    if not exam:
        flash('Exam not found!', 'info')
        return redirect(url_for('main.view_exams'))
    db.session.delete(exam)
    db.session.commit()
    return redirect(url_for('main.view_exams'))



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





@bp.route('/user/create-title', methods=['GET', 'POST'])
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
    return render_template('login.html', title='Create Title', heading='Create Title', form=form)



@bp.route('/user/create', methods=['GET', 'POST'])
def create_user():
    form=UserForm()
    if form.validate_on_submit():
        pass
    return render_template('add_user.html', title='Create User', heading='Create User', form=form)


@bp.route('/users/create', methods=['GET', 'POST'])
def create_users():
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
        title_str = row['title']
        surname = row['surname'].strip()
        first_name = row['first_name'].strip()
        department_str = row['department'].strip()
        staff_category_str = row['category'].strip()
        role = row["role"]

        # Skip creating user if already exists
        if User.query.filter_by(surname=surname.upper(), first_name=first_name).first():
            #flash(f"User {first_name} {surname} already exists!", "warning")
            continue

        # Get Category
        category = Category.query.filter_by(name=staff_category_str).first()
        if not category:
            #flash('Category does not exist', 'warning')
            continue

        # Get Department
        department = Department.query.filter_by(name=department_str).first()
        if not department:
            #flash('Department does not exist', 'warning')
            continue

        title_obj = Title.query.filter_by(title=title_str).first()
        if title_obj:
            new_user = User(
                title_id=title_obj.id,
                surname=surname.upper(),
                first_name=first_name,
                department_id=department.id,
                category_id=category.id,
                role=role
            )

        else:
            # Create user without a title
            new_user = User(
                #title_id=None,
                surname=surname.upper(),
                first_name=first_name,
                department_id=department.id,
                category_id=category.id,
                role=role
            )
        
        db.session.add(new_user)

    # Commit all changes after processing the file
    db.session.commit()
    flash("Users created successfully!", "success")
    return redirect(url_for('main.home'))
  




@bp.route('/session/create', methods=['GET', 'POST'])
def create_session():
    form = SessionForm()
    if form.validate_on_submit():
        name = form.name.data
        date = form.date.data
        academic_year_id = form.academic_year.data.id
        semester_id = form.semester.data.id
        exam_type_id = form.exam_type.data.id
        start_time = form.start_time.data#.strftime('%H:%M')
        end_time = form.end_time.data#.strftime('%H:%M')
        print(f"{start_time} -- {end_time}")
        if not Session.query.filter_by(name=name, date=date).first():
            db.session.add(
                Session(
                    name=name, date=date, academic_year_id=academic_year_id,
                    semester_id=semester_id, exam_type_id=exam_type_id, 
                    start_time=start_time, end_time=end_time        
                )
            )
            db.session.commit()
            flash('Session created successfully.', 'success')

    return render_template('narrow_form.html', title='Create Session', heading="Create Session", form=form)



@bp.route('/session/view', methods=['GET', 'POST'])
def view_exam_session():
    form = DateForm()
    sessions = Session.query.order_by(Session.id).all()
    return render_template('narrow_form.html', title='Choose', heading="Choose Date", form=form,)



@bp.route('/sessions/daily')
def daily_exam_sessions():
    form = DateForm()
    return render_template('narrow_form.html', title='Choose', heading="Choose Date", form=form,)



@bp.route('/session/edit/<int:session_id>', methods=['GET', 'POST'])
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




#@bp.route('/venues/create', methods=['GET', 'POST'])
def create_venues():
    for i in rooms:
        if not Venue.query.filter_by(name=i).first():
            db.session.add(
                Venue(name=i)
                )
    db.session.commit()
    return 0
   



@bp.route('/biometric-schedule', methods=['GET', 'POST'])
def biometric_schedule():
    form = BiometricScheduleForm()
    
    # Get venues for the JavaScript dropdown population
    venues = Venue.query.all()
    venue_list = [{'id': venue.id, 'name': venue.name} for venue in venues]
    
    if form.validate_on_submit():
        # Process form data
        session_id = form.session.data.id
        
        # Delete existing assignments for this session (if updating)
        # BiometricSchedule.query.filter_by(session_id=session_id).delete()
        
        # Save each venue-staff pair
        for pair in form.venue_staff_pairs:
            if pair.form.venue.data and pair.form.staff.data:
                schedule = Biometric(
                    session_id=session_id,
                    venue_id=pair.form.venue.data.id,
                    staff_id=pair.form.staff.data.id
                )
                db.session.add(schedule)
        
        db.session.commit()
        flash('Biometric schedule saved successfully!', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('schedule_form.html', title='Create Schedule', heading='Create Schedule', form=form)




@bp.route('/year/create', methods=['GET', 'POST'])
def create_academic_year():
    form =  AcademicYearForm()
    if form.validate_on_submit():
        year = form.year.data
        if not AcademicYear.query.filter_by(year=year).first():
            year=year.upper()
            db.session.add(
                AcademicYear(year=year)
            )
            db.session.commit()
            flash('Academic year created.', 'success')
            return redirect(url_for('main.home'))
    return render_template('narrow_form.html', title='Academic year', heading='Create Academic Year', form=form)





@bp.route('/staff/take-attendance', methods=['GET', 'POST'])
def staff_attendance():
    selected_date = request.args.get('date')
    form = AttendanceForm(selected_date=selected_date)
    if form.validate_on_submit():
        date = form.date.data
        session_id = form.session.data.id
        venue_id = form.venues.data.id
        staff_id = int(form.staff_id.data)

        try:  
            # Check if attendance record already exists
            if not Attendance.query.filter_by(exam_session_id=session_id, user_id=staff_id).first():
                # Get user first
                user = User.query.filter_by(id=staff_id).first() 
                # Create new attendance record
                attendance = Attendance(
                    exam_session_id=session_id, 
                    user_id=staff_id, 
                    timestamp=datetime.utcnow(), 
                    venue_id=venue_id
                )
                # Increment session count
                user.session_count += 1
                # Add attendance record to session
                db.session.add(attendance)
                # Single commit for both changes
                db.session.commit()
                
                # Add a flash message to confirm success
                flash('Attendance recorded successfully!', 'success')
            else:
                flash('Attendance record already exists for this staff member and session.', 'warning')
                
        except ValueError as e:
            db.session.rollback()
            flash(f'Invalid value: {str(e)}', 'danger')
            print(f"ValueError: {str(e)}")
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while recording attendance: {str(e)}', 'danger')
            print(f"Exception: {str(e)}")        
    return render_template('staff_attendance.html', title='Take Attendance', heading='Attendance', form=form)






# ###########################
###### AJAX STUFF

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


# Route to get sessions for a specific date
@bp.route('/get_sessions')
def get_sessions():
    date = request.args.get('date')
    if date:
        try:
            # Convert string date to datetime object
            parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
            
            # Get sessions for the specified date
            sessions = Session.query.filter(
                db.func.date(Session.date) == parsed_date
            ).all()
            
            # Format the sessions for the dropdown
            session_list = [
                {'id': s.id, 'name': f"{s.name} - {s.start_time}"}
                for s in sessions
            ]
            return jsonify(session_list)
        except ValueError:
            # Invalid date format
            return jsonify({'error': 'Invalid date format'}), 400
    return jsonify([])




#############################
# ##### PREREQUISITES ######


#@bp.route('/programmes/create', methods=['GET', 'POST'])
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
    #return redirect(url_for('main.home'))
    return 0



#@bp.route('/departments/create', methods=['GET', 'POST'])
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
        if not Department.query.filter_by(name=department_str).first():
            db.session.add(
                Department(name=department_str))
            db.session.commit()
    #flash('Department created', 'success')
    return 0      



def create_prerequisites():
    create_programmes()
    create_departments()
    create_courses()
    create_users()
    create_venues()
    return 0



@bp.route('/sessions/create', methods=['GET', 'POST'])
def create_sessions():
    return redirect(url_for('main.home'))






"""
#@bp.route('/courses/create', methods=['GET', 'POST'])
def create_courses():
    df = pd.read_excel(f'{UPLOAD_FOLDER}/courses.xlsx', header=0)
    for idx,row in df.iterrows():
        course_code = row['code'].strip()
        title = row['title'].strip()
        # print(course_code)
        if not Course.query.filter_by(course_code=course_code).first():
            new_course = Course(
                course_code=course_code,
                title=title
            )
            db.session.add(new_course)
    db.session.commit() # Commit all new courses after the loop
    #flash('Courses created successfully from Excel file.', 'success') # Optional: Add a success message
    #return redirect(url_for('main.home'))
    return 0



"""







