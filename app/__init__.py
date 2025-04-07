from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app.data import staff_categories, semester_data, staff_titles
from flask_login import LoginManager
import os
from flask_bootstrap import Bootstrap5



db = SQLAlchemy()  # Define it once here


load_dotenv()

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'



# Create Staff Categories
def create_categories(data=staff_categories):
    from app.models import Category
    for i in data:
        if not Category.query.filter_by(name=i).first():
            db.session.add(
                Category(name=i)
            )
    db.session.commit()

# Create Semesters at initialization
def create_semesters(data=semester_data):
    from app.models import Semester, ExamType
    for i in data['semesters']:
        if not Semester.query.filter_by(semester=i).first():
            db.session.add(Semester(semester=i))
    for j in data['exam_types']:
        if not ExamType.query.filter_by(exam_type=j).first():
            db.session.add(ExamType(exam_type=j))
    db.session.commit()

def create_titles(data=staff_titles):
    from app.models import Title
    for i in data:
        if not Title.query.filter_by(title=i.strip()).first():
            db.session.add(
                Title(title=i.strip())
            )
    db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLITE_DB_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True

    db.init_app(app)  # Initialize it once
    login_manager.init_app(app)

    Bootstrap5(app)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    
    with app.app_context():
        db.create_all()  # Create tables if not exists
        create_categories()
        create_semesters()
        create_titles()


    return app


